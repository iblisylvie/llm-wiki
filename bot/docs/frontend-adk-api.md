# 前端调用 ADK HTTP API 说明

本文档说明浏览器或任意 HTTP 客户端如何调用 ADK 服务暴露的接口，与本仓库智能体 **`xinfeng_agent`** 进行多轮问答。

**镜像默认命令为 `adk web`**：同一端口、同一进程内同时提供：

- **HTTP API**：`/run`、`/run_sse`、`/apps/.../sessions` 等（与仅启动 `adk api_server` 时一致）；
- **网页调试界面（Dev UI）**：根路径会重定向到 **`/dev-ui/`**，可在浏览器里手动测智能体。

若只需纯 API、不需要静态页，可自行将容器启动命令改为 `adk api_server`（参数与 `adk web` 相近）。

## 基础信息

| 项 | 说明 |
|----|------|
| 默认基地址 | `http://<主机>:<端口>`，例如 `http://localhost:8080` |
| 协议 | HTTP/JSON；流式接口为 **SSE**（`text/event-stream`） |
| 智能体应用名 `app_name` | 与目录名一致，一般为 **`xinfeng_agent`** |
| CORS | 镜像默认 `ADK_ALLOW_ORIGINS=*`；生产环境建议改为具体前端域名 |

> 服务启动后，可在浏览器打开 **`/docs`** 查看 FastAPI 自动生成的 OpenAPI（若部署未关闭文档）。  
> 浏览器打开 **`/`** 或 **`/dev-ui/`** 使用 ADK 自带 Web 调试界面（与自建前端调用的 API 为同一服务）。

## 调用顺序（推荐）

1. **（可选）** `GET /list-apps` — 确认可用的 `app_name`。
2. **`POST /apps/{app_name}/users/{user_id}/sessions`** — 创建会话，得到 `session_id`。
3. **`POST /run`**（一次性返回全部事件）或 **`POST /run_sse`**（流式）— 发送用户消息并获取模型与工具事件。

同一用户多轮对话时：**复用同一个 `session_id`**，每次只换 `new_message` 内容。

---

## 1. 健康检查与版本

```http
GET /health
GET /version
```

## 2. 列出应用

```http
GET /list-apps
```

响应为应用名数组，例如：`["xinfeng_agent"]`。

---

## 3. 创建会话

```http
POST /apps/xinfeng_agent/users/{user_id}/sessions
Content-Type: application/json
```

**请求体（可空）**：不传或传 `{}` 即可；服务端会生成 `session_id`。

可选字段（与 ADK `CreateSessionRequest` 一致）：

```json
{
  "session_id": "可选-自定义会话ID",
  "state": {},
  "events": []
}
```

**响应**：`Session` 对象 JSON，其中 **`id` 即为 `session_id`**，后续 `/run` 必传。

---

## 4. 运行智能体（非流式）

```http
POST /run
Content-Type: application/json
```

**请求体**（字段名为服务端 Pydantic 模型字段，一般为 **snake_case**）：

```json
{
  "app_name": "xinfeng_agent",
  "user_id": "demo-user-001",
  "session_id": "<上一步返回的 session.id>",
  "new_message": {
    "role": "user",
    "parts": [
      { "text": "你好，请介绍一下你自己。" }
    ]
  },
  "streaming": false,
  "state_delta": null,
  "invocation_id": null
}
```

- **`new_message`**：与 Google GenAI `Content` 一致；纯文本至少包含 **`parts[].text`**。
- **响应**：`Event` 数组的 JSON。模型回复、工具调用等均以事件形式返回，需在前端按需解析（例如查找模型文本、函数调用等）。

---

## 5. 运行智能体（流式 SSE，推荐用于聊天 UI）

```http
POST /run_sse
Content-Type: application/json
```

请求体与 `/run` 相同，但通常将 **`streaming` 设为 `true`**，以便服务端按流式模式产生事件：

```json
{
  "app_name": "xinfeng_agent",
  "user_id": "demo-user-001",
  "session_id": "<session_id>",
  "new_message": {
    "role": "user",
    "parts": [{ "text": "用户问题" }]
  },
  "streaming": true
}
```

**响应**：`Content-Type: text/event-stream`。  
每条消息为一行：`data: <JSON>\n\n`，`<JSON>` 为单个 **`Event`** 对象序列化结果。  
若流中出现 `{"error": "..."}`，表示服务端异常。

浏览器可用 **`fetch` + `ReadableStream`** 或 **`EventSource`**（注意：`EventSource` 仅支持 GET，对 POST 的 SSE 需自行用 `fetch` 解析 `data:` 行）。

---

## 6. 前端示例（`fetch` + 非流式 `/run`）

```javascript
const BASE = "http://localhost:8080"; // 按实际部署修改
const APP_NAME = "xinfeng_agent";
const USER_ID = "web-user-1";

async function chat(userText) {
  const sRes = await fetch(
    `${BASE}/apps/${APP_NAME}/users/${USER_ID}/sessions`,
    { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" }
  );
  if (!sRes.ok) throw new Error(await sRes.text());
  const session = await sRes.json();
  const sessionId = session.id;

  const runRes = await fetch(`${BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_name: APP_NAME,
      user_id: USER_ID,
      session_id: sessionId,
      new_message: {
        role: "user",
        parts: [{ text: userText }],
      },
      streaming: false,
    }),
  });
  if (!runRes.ok) throw new Error(await runRes.text());
  const events = await runRes.json();
  return { sessionId, events };
}
```

多轮对话：**第一次**创建会话并保存 `sessionId`；**之后**跳过创建，直接对同一 `sessionId` 调用 `/run` 或 `/run_sse`。

---

## 7. 流式示例（`fetch` 读取 SSE 文本流）

```javascript
async function chatStream(userText, sessionId, onEvent) {
  const res = await fetch(`${BASE}/run_sse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_name: APP_NAME,
      user_id: USER_ID,
      session_id: sessionId,
      new_message: { role: "user", parts: [{ text: userText }] },
      streaming: true,
    }),
  });
  if (!res.ok || !res.body) throw new Error(await res.text());

  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf("\n\n")) >= 0) {
      const block = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      const line = block.split("\n").find((l) => l.startsWith("data:"));
      if (!line) continue;
      const json = line.slice(5).trim();
      const ev = JSON.parse(json);
      if (ev.error) throw new Error(ev.error);
      onEvent(ev);
    }
  }
}
```

---

## 8. 跨域（浏览器）

若前端与 API **不同源**，需服务端允许 CORS。镜像可通过环境变量配置，例如：

```bash
-e ADK_ALLOW_ORIGINS=https://你的前端域名
```

开发阶段可用 `*`（默认），生产请收紧。

---

## 9. 反向代理与路径前缀

若在网关后以子路径挂载（例如 `/api`），ADK 支持 `--url_prefix`；需在**构建/启动参数**中配置，前端请求路径需加上相同前缀。本仓库默认镜像 **无前缀**，基路径为 `/`。

---

## 10. 与 curl 自测

```bash
BASE=http://localhost:8080
APP=xinfeng_agent
USER=u1

SID=$(curl -sS -X POST "$BASE/apps/$APP/users/$USER/sessions" \
  -H "Content-Type: application/json" -d '{}' | jq -r .id)

curl -sS -X POST "$BASE/run" -H "Content-Type: application/json" -d "{
  \"app_name\": \"$APP\",
  \"user_id\": \"$USER\",
  \"session_id\": \"$SID\",
  \"new_message\": {\"role\": \"user\", \"parts\": [{\"text\": \"你好\"}]},
  \"streaming\": false
}" | jq .
```

---
