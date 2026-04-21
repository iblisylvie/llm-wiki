FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

WORKDIR /app

# 部分依赖可能需要本地编译；若镜像体积敏感且构建失败再装回 build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# 与 main.py 中会话目录 .adk 一致；先建目录再 chown，避免运行时权限问题
# site-packages .pth：任意 `adk` 进程启动时预加载 adk_sqlite_patch（.env + SQLite 会话锁）
RUN mkdir -p /app/.adk \
    && useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app \
    && printf '%s\n' '/app' 'import adk_sqlite_patch' > /usr/local/lib/python3.12/site-packages/xinfeng_adk.pth

USER appuser

# 默认与下方 CMD 一致；启动容器可用 -e 覆盖 host/port
ENV ADK_API_HOST=0.0.0.0 \
    PORT=8080

EXPOSE 8080

# 官方 `adk web`：同一进程同时提供 REST/SSE API 与 ADK Dev UI（/dev-ui/）
CMD ["sh", "-c", "exec adk web --host \"${ADK_API_HOST:-0.0.0.0}\" --port \"${PORT:-8080}\" --session_service_uri \"${ADK_SESSION_SERVICE_URI:-sqlite+aiosqlite:////app/.adk/sessions.db}\" --allow_origins \"${ADK_ALLOW_ORIGINS:-*}\" --no-reload /app"]
