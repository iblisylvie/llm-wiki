"""ADK FastAPI 入口：本地可用 `uvicorn main:app`；Docker 默认使用官方 `adk web`（API + Dev UI 同端口）。"""
from __future__ import annotations

import os
from pathlib import Path

import adk_sqlite_patch  # noqa: F401 — 加载 .env + SQLite 会话竞态补丁
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

ROOT = Path(__file__).resolve().parent
# 与 `adk web .` 一致：本目录下仅应包含智能体子目录（如 xinfeng_agent），勿把 data 等放在根目录以免被当成 agent
AGENTS_DIR = ROOT


def create_app() -> FastAPI:
    adk_dir = ROOT / ".adk"
    adk_dir.mkdir(parents=True, exist_ok=True)
    session_uri = os.environ.get(
        "ADK_SESSION_SERVICE_URI",
        f"sqlite+aiosqlite:///{adk_dir}/sessions.db",
    )
    allow_raw = os.environ.get("ADK_ALLOW_ORIGINS", "*")
    allow_origins = [x.strip() for x in allow_raw.split(",") if x.strip()]
    web = os.environ.get("ADK_SERVE_WEB", "true").lower() in (
        "1",
        "true",
        "yes",
    )

    return get_fast_api_app(
        agents_dir=str(AGENTS_DIR),
        session_service_uri=session_uri,
        allow_origins=allow_origins,
        web=web,
        a2a=False,
    )


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("ADK_API_HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=port)
