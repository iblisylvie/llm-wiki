"""在导入 ADK DatabaseSessionService 之后、首次 create_session 之前安装补丁。

用于 `adk web` / `adk api_server` 入口（不经过 main.py）：通过 site-packages 下 .pth 在解释器启动时 import 本模块。
本地 `uvicorn main:app` 时由 main 显式 import，无需 .pth。
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env")


def apply_sqlite_session_create_lock() -> None:
    from google.adk.sessions.database_session_service import DatabaseSessionService

    if getattr(DatabaseSessionService, "_xinfeng_create_session_patched", False):
        return
    _orig = DatabaseSessionService.create_session
    _meta = asyncio.Lock()
    _locks: dict[str, asyncio.Lock] = {}

    async def _wrapped(
        self,
        *,
        app_name: str,
        user_id: str,
        state=None,
        session_id=None,
    ):
        async with _meta:
            if app_name not in _locks:
                _locks[app_name] = asyncio.Lock()
            lock = _locks[app_name]
        async with lock:
            return await _orig(
                self,
                app_name=app_name,
                user_id=user_id,
                state=state,
                session_id=session_id,
            )

    DatabaseSessionService.create_session = _wrapped  # type: ignore[method-assign]
    DatabaseSessionService._xinfeng_create_session_patched = True


apply_sqlite_session_create_lock()
