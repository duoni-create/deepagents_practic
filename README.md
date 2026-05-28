# deepagents_practic

这是配套课程讲义的 Deep Agents Python 实战工程。默认 `USE_REAL_DEEPAGENTS=false`，所有示例会走离线模拟执行，便于课堂无网络时演示流程；安装依赖并改成 `true` 后，会使用 `.env` 中配置的 DeepSeek OpenAI-compatible 接口。

## 快速运行

```bash
python -m compileall src examples tests
python examples/01_quickstart.py
python examples/06_core_capabilities.py
python examples/07_backends.py
python examples/08_async_subagents.py
python examples/09_permissions.py
python examples/10_memory.py
python examples/11_skills.py
python examples/12_sandboxes.py
python examples/13_interpreters.py
python examples/14_profiles.py
python src/deepagents_practic/course_builder_project.py
PYTHONPATH=src python -m ecommerce.report_agent_project
```

## 切换真实模型

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 修改 .env: USE_REAL_DEEPAGENTS=true
python examples/01_quickstart.py
```

## 目录说明

- `src/deepagents_practic/config.py`：读取 `.env`，集中管理模型、Base URL、课程主题等变量。
- `src/deepagents_practic/agent_factory.py`：创建真实 Deep Agents 或离线模拟 Agent。
- `src/deepagents_practic/core_capabilities.py`：截图中 Core capabilities 的结构化讲解卡片，覆盖 Overview、Models、Context engineering、Backends、Subagents、Async subagents、HITL、Permissions、Memory、Skills、Sandboxes、Interpreters、Profiles、Event streaming、Streaming。
- `src/deepagents_practic/tools.py`：课堂示例工具函数。
- `examples/`：每个知识点对应一份示例代码。
- `examples/06_core_capabilities.py`：核心能力总索引，逐项打印概念和代码落点。
- `examples/07_backends.py`：Backends 闭环示例，模拟状态后端、本地文件后端和组合路由。
- `examples/08_async_subagents.py`：Async subagents 闭环示例，用 `asyncio.gather` 并行委派并汇总结果。
- `examples/09_permissions.py`：Permissions 闭环示例，实际判断路径读写、deny 规则和 HITL 审批。
- `examples/10_memory.py`：Memory 闭环示例，保存允许记住的信息并拒绝敏感信息。
- `examples/11_skills.py`：Skills 闭环示例，把课程研发方法论封装成可复用技能对象。
- `examples/12_sandboxes.py`：Sandboxes 闭环示例，在临时目录中模拟隔离写文件并阻止越界路径。
- `examples/13_interpreters.py`：Interpreters 闭环示例，用确定性计算聚合课时、实验覆盖率和修订标记。
- `examples/14_profiles.py`：Profiles 闭环示例，为不同模型供应商生成差异化配置。
- `src/deepagents_practic/course_builder_project.py`：中型综合项目，串联工具、子代理、结构化课程产出。
- `src/ecommerce/`：企业电商数据报表 Agent 独立项目包，包含工具、Agent、项目编排和离线数据。
- `src/ecommerce/report_agent_project.py`：企业电商数据报表 Agent 综合项目入口。
- `src/ecommerce/data/ecommerce_metrics.json`：企业电商经营指标离线样例。
