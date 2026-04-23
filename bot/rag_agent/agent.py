"""智能体定义：skills 子目录列表见 skill_subdirs。"""
import os
import pathlib

from dotenv import load_dotenv
from .tools.wiki_tools import search_wiki, read_wiki_page

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

from google.adk import Agent
from google.adk.code_executors.unsafe_local_code_executor import UnsafeLocalCodeExecutor
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.skill_toolset import SkillToolset

from .skill_loader import load_skill_from_dir

skills_dir = pathlib.Path(__file__).resolve().parent / "skills"
# 显式列出技能子目录，增删技能时只改此处
skill_subdirs = [
    "rag-skill",
]
loaded_skills = [load_skill_from_dir(skills_dir / name, base_dir=_REPO_ROOT) for name in skill_subdirs]


def _skill_toolset_and_agent_executor():
    """新版 ADK 可把 code_executor 交给 SkillToolset；1.25.x 只能挂在 Agent 上。"""
    executor = UnsafeLocalCodeExecutor()
    try:
        return SkillToolset(skills=loaded_skills, code_executor=executor), None
    except TypeError:
        return SkillToolset(skills=loaded_skills), executor


my_skill_toolset, _code_executor_for_agent = _skill_toolset_and_agent_executor()


def _dashscope_api_key() -> str:
    key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "未设置环境变量 DASHSCOPE_API_KEY，无法调用 DashScope 兼容接口。"
        )
    return key


_agent_kw: dict = {
    "name": os.environ.get("LLM_WIKI_AGENT_NAME", "Wiki助手"),
    "model": LiteLlm(
        model=os.environ.get("LLM_WIKI_MODEL", "openai/qwen-plus"),
        api_base=os.environ.get("LLM_WIKI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        api_key=_dashscope_api_key(),
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    ),
    "description": os.environ.get(
        "LLM_WIKI_AGENT_DESCRIPTION",
        (
            "一个可以用中文回答问题并使用专业技能的Agent助手，严格遵守以下铁律： "
            "“无技能调用，不生成答案”——无论问题多简单、多熟悉，只要属于技能覆盖范围，必先 load_skill，再行动。"
        ),
    ),
    "instruction": os.environ.get("LLM_WIKI_AGENT_INSTRUCTION", "你是助手；涉及技能覆盖的问题必须先 load_skill 再回答。"),
    "tools": [my_skill_toolset, search_wiki, read_wiki_page],
}
if _code_executor_for_agent is not None:
    _agent_kw["code_executor"] = _code_executor_for_agent

root_agent = Agent(**_agent_kw)
