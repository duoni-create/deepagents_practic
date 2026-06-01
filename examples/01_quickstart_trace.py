from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic import build_course_agent, load_settings


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return str(content)


def _short(text: str, limit: int = 1200) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n... [已截断]"


def _stream_part(chunk: Any) -> tuple[tuple[str, ...], str, Any]:
    """Normalize LangGraph v1/v2 stream chunks into (namespace, mode, data)."""
    if isinstance(chunk, dict) and "type" in chunk:
        return tuple(chunk.get("ns") or ()), chunk["type"], chunk.get("data")
    if isinstance(chunk, tuple) and len(chunk) == 3:
        namespace, mode, data = chunk
        return tuple(namespace or ()), str(mode), data
    if isinstance(chunk, tuple) and len(chunk) == 2:
        first, second = chunk
        if isinstance(first, tuple):
            return tuple(first), "unknown", second
        return (), str(first), second
    return (), "unknown", chunk


def _iter_messages(value: Any):
    if hasattr(value, "content") and value.__class__.__name__.endswith("Message"):
        yield value
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from _iter_messages(item)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_messages(item)


def _print_tool_result(message: Any, tool_call_to_subagent: dict[str, tuple[str, str]], printed_results: set[str]) -> None:
    tool_call_id = getattr(message, "tool_call_id", "")
    if not tool_call_id or tool_call_id in printed_results:
        return
    printed_results.add(tool_call_id)
    content = _short(_content_text(message.content))
    if tool_call_id in tool_call_to_subagent:
        subagent_type, _ = tool_call_to_subagent[tool_call_id]
        print(f"\n[subagent.result] {subagent_type}")
        print(content)
        return
    print("\n[tool.result]")
    print(content)


def _print_tool_call(call: dict[str, Any]) -> None:
    name = call.get("name", "")
    if name == "task":
        return
    args = call.get("args") or {}
    print(f"\n[tool.call] {name}")
    if args:
        print(_short(str(args), 600))


def main() -> None:
    settings = load_settings()
    agent = build_course_agent(settings)
    task = sys.argv[1] if len(sys.argv) > 1 else f"为《{settings.course_topic}》设计 3 个学习目标"
    payload = {"messages": [{"role": "user", "content": task}]}
    tool_call_to_subagent: dict[str, tuple[str, str]] = {}
    printed_results: set[str] = set()

    print(f"[user] {task}")
    print("\n--- trace: main agent / subagents ---")

    if agent.__class__.__name__ == "MockDeepAgent":
        print("[trace] 当前是离线 Mock Agent，下面是模拟的结构化事件。")
        if hasattr(agent, "stream_events"):
            for event in agent.stream_events(payload):
                print(event)
        else:
            for event in agent.stream(payload, stream_mode="updates"):
                print(event)
        return

    for chunk in agent.stream(
        payload,
        config={"recursion_limit": 40},
        stream_mode=["tasks", "updates"],
        subgraphs=True,
        version="v2",
    ):
        namespace, mode, data = _stream_part(chunk)

        if mode == "tasks" and isinstance(data, dict):
            name = data.get("name")
            if "result" not in data:
                print(f"\n[task.start] ns={namespace or 'root'} node={name}")
                for call in data.get("input") or []:
                    if not isinstance(call, dict) or call.get("name") != "task":
                        continue
                    args = call.get("args") or {}
                    tool_call_id = call.get("id", "")
                    subagent_type = args.get("subagent_type", "")
                    description = args.get("description", "")
                    if tool_call_id:
                        tool_call_to_subagent[tool_call_id] = (subagent_type, description)
                    print(f"[subagent.call] {subagent_type}")
                    print(_short(str(description), 600))
            else:
                status = "failed" if data.get("error") else "done"
                print(f"\n[task.end] ns={namespace or 'root'} node={name} status={status}")
            continue

        if mode != "updates":
            continue

        for message in _iter_messages(data):
            for call in getattr(message, "tool_calls", None) or []:
                if call.get("name") != "task":
                    _print_tool_call(call)
                    continue
                args = call.get("args") or {}
                tool_call_id = call.get("id", "")
                subagent_type = args.get("subagent_type", "")
                description = args.get("description", "")
                if tool_call_id:
                    tool_call_to_subagent[tool_call_id] = (subagent_type, description)
                print(f"\n[subagent.call] {subagent_type}")
                print(_short(str(description), 600))

            if message.__class__.__name__ != "ToolMessage":
                continue
            _print_tool_result(message, tool_call_to_subagent, printed_results)


if __name__ == "__main__":
    main()
