from __future__ import annotations

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"


# 中文说明：读取本地电商经营指标 JSON，模拟从数仓或 BI 服务获取数据。
def load_ecommerce_metrics() -> str:
    """读取企业电商经营指标样例，模拟数仓或 BI 指标服务返回的数据。"""
    metrics_path = DATA_DIR / "ecommerce_metrics.json"
    return metrics_path.read_text(encoding="utf-8")


# 中文说明：定义电商报表 Agent 的用户、业务场景、报表模块和非功能要求。
def define_ecommerce_report_requirements() -> dict[str, object]:
    """输出企业电商数据报表 Agent 的功能需求清单。"""
    return {
        "users": ["经营负责人", "渠道运营", "类目运营", "财务分析", "供应链计划"],
        "core_scenarios": [
            "每天 9 点自动生成经营日报",
            "按渠道、类目、商品、地区维度解释 GMV 和订单变化",
            "识别退款率、转化率、缺货风险等异常",
            "把自然语言问题转成指标查询和报表摘要",
            "在发布前触发人工审批，避免错误报表自动推送",
        ],
        "report_modules": ["经营总览", "渠道分析", "类目分析", "异常预警", "行动建议", "数据口径说明"],
        "non_functional": ["权限隔离", "指标口径可追溯", "日报 5 分钟内生成", "关键动作可审计", "支持灰度上线"],
    }


# 中文说明：生成电商报表 Agent 的分层架构，包括数据源、工具层、Agent 层和治理层。
def design_ecommerce_report_architecture() -> dict[str, object]:
    """输出企业电商数据报表 Agent 的架构设计。"""
    return {
        "input_layer": ["数据仓库", "订单系统", "商品系统", "广告投放", "库存系统"],
        "tool_layer": ["指标查询工具", "异常检测工具", "报表生成工具", "图表配置工具", "消息推送工具"],
        "agent_layer": {
            "main_agent": "report-orchestrator",
            "subagents": [
                {"name": "metric-agent", "responsibility": "查询指标、校验口径、输出结构化数据"},
                {"name": "insight-agent", "responsibility": "解释变化、定位异常、生成经营洞察"},
                {"name": "visual-agent", "responsibility": "选择图表、组织版式、生成报表结构"},
                {"name": "release-agent", "responsibility": "检查权限、审批状态、上线步骤和回滚方案"},
            ],
        },
        "governance_layer": ["权限策略", "HITL 审批", "事件流观察", "质量评分", "发布审计"],
        "output_layer": ["HTML 报表", "Markdown 摘要", "管理层日报", "企业微信/邮件推送"],
    }


# 中文说明：输出代码开发规格，说明每个文件负责什么以及开发步骤怎么拆。
def generate_ecommerce_report_spec() -> dict[str, object]:
    """输出报表 Agent 的代码开发规格，便于课堂拆任务。"""
    return {
        "modules": [
            {"file": "src/ecommerce/tools05.py", "work": "实现指标读取、需求定义、架构设计、上线计划和质量检查工具"},
            {"file": "src/ecommerce/agent.py", "work": "实现报表 Agent 的离线运行、工具注册和事件流"},
            {"file": "src/ecommerce/project.py", "work": "串联需求、架构、开发、上线四个阶段"},
            {"file": "src/ecommerce/report_agent_project.py", "work": "提供独立项目运行入口"},
            {"file": "src/ecommerce/data/ecommerce_metrics.json", "work": "提供离线经营指标样例"},
            {"file": "../img/ecommerce_report_agent_architecture.svg", "work": "提供架构设计图"},
        ],
        "agent_contract": {
            "input": "报表周期、目标用户、关注指标、发布渠道",
            "output": "需求清单、架构方案、报表模块、上线计划、风险检查",
            "quality_bar": ["指标口径清楚", "异常解释可追溯", "敏感推送需审批", "上线可回滚"],
        },
        "development_steps": [
            "先跑离线指标样例，验证报表字段",
            "实现工具函数并保证返回结构化 dict",
            "配置 report-orchestrator 和 metric/insight/visual/release 子代理",
            "增加流式事件，展示查询、分析、生成、审批、发布进度",
            "用质量检查工具验证功能完整性和上线风险",
        ],
    }


# 中文说明：设计报表 Agent 从联调、校验、灰度到正式上线和回滚的发布流程。
def plan_ecommerce_report_launch() -> dict[str, object]:
    """输出企业电商数据报表 Agent 的上线流程。"""
    return {
        "release_stages": [
            {"stage": "开发联调", "checks": ["离线数据可跑", "指标字段完整", "报表结构稳定"]},
            {"stage": "数据校验", "checks": ["与 BI 口径对账", "异常预警人工抽查", "权限路径检查"]},
            {"stage": "灰度发布", "checks": ["仅推送给运营小组", "开启 HITL", "记录 event streaming"]},
            {"stage": "正式上线", "checks": ["定时任务启用", "失败告警启用", "回滚入口确认"]},
            {"stage": "运营复盘", "checks": ["日报采纳率", "误报漏报", "人工修订原因"]},
        ],
        "hitl_policy": {
            "auto_generate": ["草稿报表", "内部指标解释", "异常候选清单"],
            "requires_approval": ["发送管理层日报", "对外发布数据", "修改指标口径", "触发高优先级告警"],
        },
        "rollback": ["关闭定时推送", "切回 BI 固定报表", "保留日志和输入数据", "通知业务方报表暂停"],
    }


# 中文说明：检查项目输出是否覆盖架构、需求、代码、上线四类关键内容并评分。
def check_ecommerce_report_project(payload: str) -> dict[str, object]:
    """检查企业电商报表 Agent 项目是否覆盖需求、架构、开发和上线。"""
    required = {
        "架构": ["架构", "agent", "子代理"],
        "需求": ["需求", "用户", "场景"],
        "代码": ["代码", "工具", "数据"],
        "上线": ["上线", "灰度", "审批"],
    }
    missing = [name for name, words in required.items() if not all(word.lower() in payload.lower() for word in words)]
    score = 100 - len(missing) * 15
    return {"score": max(score, 0), "missing": missing, "raw_length": len(payload)}


# 中文说明：把电商项目中的 dict/list 格式化成易读 JSON 字符串。
def pretty_json(data: object) -> str:
    """让课堂输出更易读。"""
    return json.dumps(data, ensure_ascii=False, indent=2)
