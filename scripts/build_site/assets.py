"""HTML/CSS/JS templates for the generated site."""

SITE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Wiki</title>
    <script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"></script>
    <style>
        :root {
            --bg-light: #f5f5f7;
            --bg-dark: #000000;
            --text-primary: #1d1d1f;
            --text-secondary: rgba(0, 0, 0, 0.8);
            --text-tertiary: rgba(0, 0, 0, 0.48);
            --apple-blue: #0071e3;
            --link-blue: #0066cc;
            --link-blue-dark: #2997ff;
            --nav-bg: rgba(0, 0, 0, 0.8);
            --border-light: rgba(0, 0, 0, 0.1);
            --code-bg: #f0f0f2;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 15px;
            line-height: 1.47;
            color: var(--text-primary);
            background: var(--bg-light);
            -webkit-font-smoothing: antialiased;
        }

        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 48px;
            background: var(--nav-bg);
            backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
        }

        .top-nav .logo {
            color: #fff;
            font-size: 17px;
            font-weight: 600;
            letter-spacing: -0.3px;
            text-decoration: none;
        }

        .layout {
            display: grid;
            grid-template-columns: 280px 1fr 260px;
            height: 100vh;
            padding-top: 48px;
            transition: grid-template-columns 0.25s ease;
        }

        .layout.bot-open {
            grid-template-columns: 280px 1fr 260px;
        }

        .sidebar-left {
            position: fixed;
            top: 48px;
            left: 0;
            width: 280px;
            height: calc(100vh - 48px);
            overflow-y: auto;
            border-right: 1px solid var(--border-light);
            background: #fff;
            padding: 20px 0;
        }

        .nav-section {
            margin-bottom: 16px;
        }

        .nav-section-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-tertiary);
            padding: 8px 16px;
        }

        .nav-folder-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-primary);
            padding: 6px 16px;
            margin-top: 4px;
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            transition: color 0.15s;
        }

        .nav-folder-title::before {
            content: "";
            display: inline-block;
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid var(--text-tertiary);
            margin-right: 6px;
            transition: transform 0.2s;
        }

        .nav-folder-title.collapsed::before {
            transform: rotate(-90deg);
        }

        .nav-folder-title:hover {
            color: var(--apple-blue);
        }

        .nav-folder-children {
            overflow: hidden;
            transition: max-height 0.2s ease-out;
        }

        .nav-folder-children.collapsed {
            display: none;
        }

        .nav-link {
            display: block;
            font-size: 13px;
            color: var(--text-secondary);
            text-decoration: none;
            padding: 5px 16px;
            border-radius: 0;
            transition: background 0.15s, color 0.15s;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .nav-link:hover {
            color: var(--apple-blue);
            background: rgba(0, 113, 227, 0.06);
        }

        .nav-link.active {
            color: var(--apple-blue);
            background: rgba(0, 113, 227, 0.1);
            font-weight: 500;
        }

        .main {
            grid-column: 2;
            min-height: calc(100vh - 48px);
            padding: 24px;
            align-self: start;
        }

        .content {
            background: #fff;
            border-radius: 12px;
            padding: 28px;
            box-shadow: rgba(0, 0, 0, 0.08) 0px 4px 20px 0px;
            width: 100%;
            margin: 0 auto;
        }

        .content h1 {
            font-size: 36px;
            font-weight: 600;
            line-height: 1.1;
            letter-spacing: -0.5px;
            margin-bottom: 24px;
            color: var(--text-primary);
        }

        .content h2 {
            font-size: 24px;
            font-weight: 600;
            line-height: 1.2;
            letter-spacing: -0.3px;
            margin-top: 40px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-light);
        }

        .content h3 {
            font-size: 19px;
            font-weight: 600;
            line-height: 1.25;
            margin-top: 28px;
            margin-bottom: 12px;
        }

        .content h4 {
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        .content p {
            margin-bottom: 14px;
            color: var(--text-secondary);
        }

        .content a {
            color: var(--link-blue);
            text-decoration: none;
        }

        .content a:hover {
            text-decoration: underline;
        }

        .content ul, .content ol {
            margin-bottom: 14px;
            padding-left: 24px;
        }

        .content li {
            margin-bottom: 6px;
        }

        .content code {
            font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
            font-size: 13px;
            background: var(--code-bg);
            padding: 2px 6px;
            border-radius: 4px;
            color: #d73a49;
        }

        .content pre {
            background: #1d1d1f;
            color: #f5f5f7;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 16px;
        }

        .content pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }

        .content blockquote {
            border-left: 4px solid var(--apple-blue);
            padding-left: 16px;
            margin: 16px 0;
            color: var(--text-tertiary);
            font-style: italic;
        }

        .content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 16px;
            font-size: 14px;
        }

        .content th, .content td {
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-light);
        }

        .content th {
            font-weight: 600;
            background: #fafafc;
        }

        .content img {
            max-width: 100%;
            border-radius: 8px;
            margin: 16px 0;
        }

        .download-card {
            text-align: center;
            padding: 64px 32px;
        }

        .download-card h1 {
            font-size: 28px;
            margin-bottom: 12px;
        }

        .download-card .meta {
            color: var(--text-tertiary);
            margin-bottom: 32px;
            font-size: 14px;
        }

        .download-card .meta code {
            color: var(--text-secondary);
            background: var(--code-bg);
        }

        .btn-primary, .content .btn-primary {
            display: inline-block;
            background: var(--apple-blue);
            color: #fff;
            padding: 10px 22px;
            border-radius: 980px;
            font-size: 15px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(0, 113, 227, 0.3);
        }

        .btn-primary:hover, .content .btn-primary:hover {
            opacity: 0.95;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(0, 113, 227, 0.4);
            transform: translateY(-1px);
        }

        .sidebar-right {
            position: fixed;
            top: 48px;
            right: 0;
            width: 260px;
            height: calc(100vh - 48px);
            overflow-y: auto;
            border-left: 1px solid var(--border-light);
            background: #fff;
            padding: 24px 0;
        }

        .toc-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-tertiary);
            padding: 0 20px 12px;
        }

        .toc-link {
            display: block;
            font-size: 12px;
            color: var(--text-secondary);
            text-decoration: none;
            padding: 5px 20px;
            border-left: 2px solid transparent;
            transition: all 0.15s;
        }

        .toc-link:hover {
            color: var(--apple-blue);
        }

        .toc-link.active {
            color: var(--apple-blue);
            border-left-color: var(--apple-blue);
            background: rgba(0, 113, 227, 0.06);
        }

        .toc-link.level-2 { padding-left: 32px; }
        .toc-link.level-3 { padding-left: 44px; }
        .toc-link.level-4 { padding-left: 56px; }

        .empty-state {
            text-align: center;
            padding: 120px 24px;
            color: var(--text-tertiary);
            min-height: calc(100vh - 48px - 48px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .empty-state h2 {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 12px;
        }

        @media (min-width: 900px) {
            .main { padding: 32px; }
            .content { padding: 40px; }
        }

        @media (min-width: 1200px) {
            .layout {
                grid-template-columns: 280px 1fr 260px;
            }
            .sidebar-left { width: 280px; }
            .sidebar-right { width: 260px; }
            .main { padding: 40px 48px; }
            .content { padding: 48px 56px; max-width: 1400px; }
        }

        @media (max-width: 900px) {
            .layout {
                display: block;
            }
            .sidebar-left, .sidebar-right {
                position: relative;
                width: 100%;
                height: auto;
                top: 0;
                border: none;
                border-bottom: 1px solid var(--border-light);
            }
            .sidebar-right {
                display: none;
            }
            .main {
                padding: 16px;
            }
            .content {
                padding: 24px;
            }
        }

        .chat-bot {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 2000;
            font-family: inherit;
        }

        .chat-bot-toggle {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            border: none;
            background: #fff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            transition: transform 0.2s;
        }

        .chat-bot-toggle:hover {
            transform: scale(1.05);
        }

        .chat-bot-toggle img {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            object-fit: cover;
        }

        .chat-bot.open .chat-bot-toggle {
            display: none;
        }

        .sidebar-bot {
            position: fixed;
            top: 48px;
            right: 0;
            width: 260px;
            height: calc(100vh - 48px);
            background: #fff;
            border-left: 1px solid var(--border-light);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 1999;
        }

        .layout.bot-open .sidebar-bot {
            display: flex;
        }

        .layout.bot-open .sidebar-right {
            display: none;
        }

        .chat-bot-header {
            height: 52px;
            padding: 0 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-light);
            flex-shrink: 0;
        }

        .chat-bot-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .chat-bot-close {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: none;
            background: transparent;
            color: var(--text-tertiary);
            font-size: 20px;
            line-height: 1;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-bot-close:hover {
            background: rgba(0, 0, 0, 0.05);
            color: var(--text-primary);
        }

        .chat-bot-messages {
            flex: 1;
            overflow-y: auto;
            padding: 0;
            display: flex;
            flex-direction: column;
        }

        .chat-bot-message {
            display: flex;
        }

        .chat-bot-message.bot {
            justify-content: flex-start;
        }

        .chat-bot-message.user {
            justify-content: flex-end;
        }

        .chat-bot-bubble {
            max-width: 80%;
            padding: 10px 14px;
            border-radius: 14px;
            font-size: 14px;
            line-height: 1.45;
            word-break: break-word;
        }

        .chat-bot-message.bot .chat-bot-bubble {
            background: #f2f2f7;
            color: var(--text-primary);
            border-bottom-left-radius: 4px;
        }

        .chat-bot-message.user .chat-bot-bubble {
            background: var(--apple-blue);
            color: #fff;
            border-bottom-right-radius: 4px;
        }

        .chat-bot-footer {
            padding: 12px 16px;
            border-top: 1px solid var(--border-light);
            display: flex;
            gap: 8px;
            align-items: center;
            flex-shrink: 0;
        }

        .chat-bot-input {
            flex: 1;
            height: 36px;
            padding: 0 12px;
            border: 1px solid var(--border-light);
            border-radius: 980px;
            font-size: 14px;
            outline: none;
        }

        .chat-bot-input:focus {
            border-color: var(--apple-blue);
        }

        .chat-bot-send {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: none;
            background: var(--apple-blue);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
            padding: 0;
        }

        .chat-bot-send svg {
            flex-shrink: 0;
            display: block;
        }

        .chat-bot-send:hover {
            opacity: 0.9;
        }

        .chat-bot-send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .chat-user-query {
            position: sticky;
            top: 0;
            z-index: 10;
            background: #f5f5f7;
            padding: 14px 18px;
            margin: 0 12px;
            border-radius: 16px;
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-primary);
            word-break: break-word;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }

        .chat-agent-response {
            padding: 12px 20px 28px;
            font-size: 14px;
            line-height: 1.65;
            color: var(--text-primary);
            word-break: break-word;
        }

        .chat-agent-response.markdown > *:first-child {
            margin-top: 0;
        }

        .chat-agent-response.markdown p {
            margin: 0 0 10px;
        }

        .chat-agent-response.markdown p:last-child {
            margin-bottom: 0;
        }

        .chat-agent-response.markdown ul,
        .chat-agent-response.markdown ol {
            margin: 0 0 10px 20px;
            padding: 0;
        }

        .chat-agent-response.markdown li {
            margin-bottom: 4px;
        }

        .chat-agent-response.markdown code {
            background: var(--code-bg);
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, monospace;
        }

        .chat-agent-response.markdown pre {
            background: var(--code-bg);
            padding: 12px 14px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
        }

        .chat-agent-response.markdown pre code {
            background: none;
            padding: 0;
            font-size: 12px;
        }

        .chat-agent-response.markdown blockquote {
            border-left: 3px solid var(--border-light);
            margin: 10px 0;
            padding-left: 12px;
            color: var(--text-secondary);
        }

        .chat-agent-response.markdown strong {
            font-weight: 600;
        }

        .chat-agent-response.markdown a {
            color: var(--apple-blue);
            text-decoration: none;
        }

        .chat-agent-response.markdown a:hover {
            text-decoration: underline;
        }

        .chat-agent-response .chat-tool-tags {
            margin-bottom: 10px;
        }

        .chat-event-bubble.error {
            background: #fff0f0;
            border: 1px solid #ffcdd2;
            color: #c62828;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 14px;
            margin: 8px 0;
        }

        .chat-event {
            display: flex;
            gap: 10px;
            align-items: flex-start;
        }

        .chat-event-meta {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            flex-shrink: 0;
            width: 36px;
        }

        .chat-event-num {
            font-size: 11px;
            color: var(--text-tertiary);
            font-weight: 600;
            font-family: -apple-system, monospace;
        }

        .chat-event-avatar {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: #34c759;
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            flex-shrink: 0;
        }

        .chat-event-avatar.user {
            background: #0071e3;
        }

        .chat-event-body {
            flex: 1;
            min-width: 0;
        }

        .chat-event-bubble {
            background: #f2f2f7;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 14px;
            line-height: 1.55;
            word-break: break-word;
            color: var(--text-primary);
        }

        .chat-event-bubble.markdown p {
            margin: 0 0 8px;
        }

        .chat-event-bubble.markdown p:last-child {
            margin-bottom: 0;
        }

        .chat-event-bubble.markdown h1,
        .chat-event-bubble.markdown h2,
        .chat-event-bubble.markdown h3,
        .chat-event-bubble.markdown h4 {
            margin: 12px 0 6px;
            font-size: 15px;
            font-weight: 600;
        }

        .chat-event-bubble.markdown ul,
        .chat-event-bubble.markdown ol {
            margin: 0 0 8px 18px;
            padding: 0;
        }

        .chat-event-bubble.markdown li {
            margin-bottom: 2px;
        }

        .chat-event-bubble.markdown code {
            background: var(--code-bg);
            padding: 1px 4px;
            border-radius: 4px;
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, monospace;
        }

        .chat-event-bubble.markdown pre {
            background: var(--code-bg);
            padding: 10px 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 8px 0;
        }

        .chat-event-bubble.markdown pre code {
            background: none;
            padding: 0;
            font-size: 12px;
        }

        .chat-event-bubble.markdown blockquote {
            border-left: 3px solid var(--border-light);
            margin: 8px 0;
            padding-left: 10px;
            color: var(--text-secondary);
        }

        .chat-event-bubble.markdown strong {
            font-weight: 600;
        }

        .chat-event-bubble.markdown a {
            color: var(--apple-blue);
            text-decoration: none;
        }

        .chat-event-bubble.markdown a:hover {
            text-decoration: underline;
        }

        .chat-tool-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .chat-tool-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 6px;
            background: #fff;
            border: 1px solid var(--border-light);
            font-size: 13px;
            color: var(--text-primary);
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }

        .chat-tool-tag .tool-icon {
            font-size: 12px;
        }

        .chat-event-state {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 6px;
            background: #fff;
            border: 1px solid var(--border-light);
            font-size: 13px;
            color: var(--text-primary);
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }

        .chat-event-state .state-icon {
            font-size: 12px;
        }

        .chat-event-row + .chat-event-row {
            margin-top: 12px;
        }

        @media (max-width: 900px) {
            .layout.bot-open {
                grid-template-columns: 280px 1fr 0px;
            }
            .sidebar-bot {
                width: 100%;
                border-left: none;
            }
        }

        @media (max-width: 420px) {
            .chat-bot {
                right: 16px;
                bottom: 16px;
            }
        }
    </style>
</head>
<body>
    <nav class="top-nav">
        <a class="logo" href="#/">LLM Wiki</a>
        <div class="search"></div>
    </nav>

    <div class="layout">
        <aside class="sidebar-left">
            {{nav_html}}
        </aside>

        <main class="main">
            <div class="content" id="content">
                <div class="empty-state">
                    <h2>知识库</h2>
                    <p>请在左侧导航栏选择一篇文章查看</p>
                </div>
            </div>
        </main>

        <aside class="sidebar-bot">
            <div class="chat-bot-header">
                <span class="chat-bot-title">AI 助手</span>
                <button class="chat-bot-close" aria-label="关闭">×</button>
            </div>
            <div class="chat-bot-messages">
                <div class="chat-agent-response markdown">你好！我是 Wiki 助手，有什么可以帮你的吗？</div>
            </div>
            <div class="chat-bot-footer">
                <input type="text" class="chat-bot-input" placeholder="输入消息…">
                <button class="chat-bot-send" aria-label="发送">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
            </div>
        </aside>

        <aside class="sidebar-right">
            <div class="toc-title">本页目录</div>
            <div id="toc"></div>
        </aside>
    </div>

    <script>
        const pages = {{pages_json}};

        function renderToc(toc) {
            if (!toc || toc.length === 0) {
                return '<div style="padding: 0 20px; color: var(--text-tertiary); font-size: 12px;">无目录</div>';
            }
            let html = '';
            function walk(items, level=1) {
                for (const item of items) {
                    const id = item.id || '';
                    html += `<a class="toc-link level-${level}" href="#${id}" data-id="${id}">${item.name}</a>`;
                    if (item.children && item.children.length) {
                        walk(item.children, level + 1);
                    }
                }
            }
            walk(toc);
            return html;
        }

        function slugify(text) {
            return text.toLowerCase().replace(/[^\\w\\s-]/g, '').replace(/\\s+/g, '-');
        }

        function addHeadingIds(html) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6');
            headings.forEach(h => {
                if (!h.id) {
                    h.id = slugify(h.textContent || '');
                }
            });
            return doc.body.innerHTML;
        }

        function expandActiveFolders() {
            document.querySelectorAll('.nav-link.active').forEach(link => {
                let el = link.parentElement;
                while (el) {
                    if (el.classList.contains('nav-folder-children') && el.classList.contains('collapsed')) {
                        el.classList.remove('collapsed');
                        const title = el.previousElementSibling;
                        if (title && title.classList.contains('nav-folder-title')) {
                            title.classList.remove('collapsed');
                        }
                    }
                    el = el.parentElement;
                }
            });
        }

        let currentPageKey = '';

        function loadPage(key) {
            const page = pages[key];
            if (!page) return;
            currentPageKey = key;

            document.title = page.title + ' | LLM Wiki';
            const contentEl = document.getElementById('content');
            contentEl.innerHTML = addHeadingIds(page.html);

            const tocEl = document.getElementById('toc');
            tocEl.innerHTML = renderToc(page.toc);

            // Rewrite TOC links to preserve page key
            tocEl.querySelectorAll('a.toc-link').forEach(a => {
                const id = a.getAttribute('data-id');
                if (id) a.setAttribute('href', '#/' + key + '#' + id);
            });

            document.querySelectorAll('.nav-link').forEach(a => a.classList.remove('active'));
            const activeLink = document.querySelector(`.nav-link[data-key="${key}"]`);
            if (activeLink) activeLink.classList.add('active');

            expandActiveFolders();

            function resolveRelPath(base, href) {
                const parts = base.split('/').filter(p => p);
                const hrefParts = href.split('/').filter(p => p);
                parts.pop();
                for (const part of hrefParts) {
                    if (part === '..') {
                        parts.pop();
                    } else if (part !== '.') {
                        parts.push(part);
                    }
                }
                return parts.join('/');
            }

            contentEl.querySelectorAll('a').forEach(a => {
                const href = a.getAttribute('href');
                if (!href) return;
                if (href.startsWith('../../raw/')) {
                    const rawPath = href.replace('../../raw/', '');
                    if (pages[rawPath]) {
                        const newHref = '#/' + rawPath;
                        a.setAttribute('href', newHref);
                        a.addEventListener('click', e => {
                            e.preventDefault();
                            window.location.hash = newHref;
                        });
                    } else {
                        a.setAttribute('href', '../raw/' + rawPath);
                        a.setAttribute('target', '_blank');
                    }
                } else if (!href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:') && href.endsWith('.md')) {
                    const resolved = resolveRelPath(page.rel_path || '', href);
                    const newHref = '#/wiki/' + resolved;
                    a.setAttribute('href', newHref);
                    a.addEventListener('click', e => {
                        e.preventDefault();
                        window.location.hash = newHref;
                    });
                }
            });
        }

        function route() {
            const hash = decodeURIComponent(window.location.hash || '#/');

            // Page route: #/some/page.md
            if (hash.startsWith('#/')) {
                let key = hash.replace('#/', '');
                const anchorIdx = key.indexOf('#');
                let anchor = '';
                if (anchorIdx >= 0) {
                    anchor = key.substring(anchorIdx + 1);
                    key = key.substring(0, anchorIdx);
                }
                if (key && pages[key]) {
                    loadPage(key);
                    if (anchor) {
                        setTimeout(() => {
                            const el = document.getElementById(anchor);
                            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }, 0);
                    }
                    return;
                }
            }

            // Anchor-only hash change (e.g. #3d) while viewing a page: let browser scroll
            if (hash.startsWith('#') && !hash.startsWith('#/') && currentPageKey) {
                return;
            }

            // Default empty state
            document.getElementById('content').innerHTML = `
                <div class="empty-state">
                    <h2>知识库</h2>
                    <p>请在左侧导航栏选择一篇文章查看</p>
                </div>
            `;
            document.getElementById('toc').innerHTML = '';
            document.title = 'LLM Wiki';
            document.querySelectorAll('.nav-link').forEach(a => a.classList.remove('active'));
        }

        window.addEventListener('hashchange', route);
        document.addEventListener('DOMContentLoaded', () => {
            route();
            document.querySelectorAll('.nav-folder-title').forEach(title => {
                title.addEventListener('click', () => {
                    title.classList.toggle('collapsed');
                    const children = title.nextElementSibling;
                    if (children && children.classList.contains('nav-folder-children')) {
                        children.classList.toggle('collapsed');
                    }
                });
            });
        });

        document.addEventListener('scroll', () => {
            const headings = document.querySelectorAll('.content [id]');
            let current = '';
            headings.forEach(h => {
                const rect = h.getBoundingClientRect();
                if (rect.top < 120) {
                    current = h.id;
                }
            });
            document.querySelectorAll('.toc-link').forEach(a => a.classList.remove('active'));
            if (current) {
                const active = document.querySelector(`.toc-link[data-id="${current}"]`);
                if (active) active.classList.add('active');
            }
        }, { passive: true });
    </script>

    <div class="chat-bot">
        <button class="chat-bot-toggle" aria-label="打开对话">
            <img src="assets/llm-wiki-bot-icon-v2.png" alt="Bot" width="56" height="56">
        </button>
    </div>

    <script>
        (function() {
            const layout = document.querySelector('.layout');
            const bot = document.querySelector('.chat-bot');
            const toggle = document.querySelector('.chat-bot-toggle');
            const closeBtn = document.querySelector('.chat-bot-close');
            const input = document.querySelector('.chat-bot-input');
            const send = document.querySelector('.chat-bot-send');
            const messages = document.querySelector('.chat-bot-messages');

            const API_BASE = window.BOT_API_BASE || 'http://js3.blockelite.cn:20286';
            const APP_NAME = 'rag_agent';
            const USER_ID = 'wiki-visitor-' + Math.random().toString(36).slice(2, 8);

            let sessionId = null;
            let isLoading = false;
            let eventCounter = 0;
            let uiEntries = [];

            function toggleDialog() {
                bot.classList.toggle('open');
                layout.classList.toggle('bot-open');
            }
            toggle.addEventListener('click', toggleDialog);
            closeBtn.addEventListener('click', toggleDialog);

            function md(text) {
                if (!text) return '';
                return marked.parse(text, { breaks: true, gfm: true });
            }

            function getAvatar(role) {
                if (role === 'user') return '👤';
                return '🤖';
            }

            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }

            function createEventRow(role, innerHtml) {
                eventCounter++;
                const row = document.createElement('div');
                row.className = 'chat-event chat-event-row';
                const avatarCls = role === 'user' ? 'chat-event-avatar user' : 'chat-event-avatar';
                row.innerHTML =
                    '<div class="chat-event-meta">' +
                        '<span class="chat-event-num">#' + eventCounter + '</span>' +
                        '<span class="' + avatarCls + '">' + getAvatar(role) + '</span>' +
                    '</div>' +
                    '<div class="chat-event-body">' + innerHtml + '</div>';
                messages.appendChild(row);
                messages.scrollTop = messages.scrollHeight;
                return row;
            }

            function createTextBubble(role, html) {
                const div = document.createElement('div');
                if (role === 'user') {
                    div.className = 'chat-user-query markdown';
                } else {
                    div.className = 'chat-agent-response markdown';
                }
                div.innerHTML = html;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
                return div;
            }

            function buildEntryFromEvent(event) {
                const role = event.author === 'user' ? 'user' : 'bot';
                let text = '';
                let functionCalls = [];
                let functionResponses = [];
                let stateDelta = null;
                let artifactDelta = null;
                let error = null;

                if (event.content && event.content.parts) {
                    for (const p of event.content.parts) {
                        if (p.text != null && p.text !== '') text += p.text;
                        if (p.functionCall) functionCalls.push(p.functionCall);
                        if (p.functionResponse) functionResponses.push(p.functionResponse);
                    }
                }

                if (event.actions) {
                    if (event.actions.stateDelta && Object.keys(event.actions.stateDelta).length) {
                        stateDelta = event.actions.stateDelta;
                    }
                    if (event.actions.artifactDelta && Object.keys(event.actions.artifactDelta).length) {
                        artifactDelta = event.actions.artifactDelta;
                    }
                }

                if (event.errorMessage || event.errorCode) {
                    error = { code: event.errorCode, message: event.errorMessage };
                }

                return {
                    role, text, functionCalls, functionResponses,
                    stateDelta, artifactDelta, error,
                    eventId: event.id,
                    partial: !!event.partial,
                    event: event,
                    el: null,
                    eventCounter: 0
                };
            }

            function renderEntryHtml(entry) {
                let html = '';

                if (entry.functionCalls && entry.functionCalls.length) {
                    const tags = entry.functionCalls.map(function(fc) {
                        const name = fc.name || 'tool';
                        return '<span class="chat-tool-tag"><span class="tool-icon">⚡</span>' + name + '</span>';
                    }).join('');
                    html += '<div class="chat-tool-tags">' + tags + '</div>';
                }

                if (entry.functionResponses && entry.functionResponses.length) {
                    const tags = entry.functionResponses.map(function(fr) {
                        const name = fr.name || 'result';
                        return '<span class="chat-tool-tag"><span class="tool-icon">📤</span>' + name + '</span>';
                    }).join('');
                    html += '<div class="chat-tool-tags">' + tags + '</div>';
                }

                if (entry.stateDelta) {
                    html += '<div class="chat-tool-tags"><span class="chat-event-state"><span class="state-icon">🔧</span>State</span></div>';
                }

                if (entry.artifactDelta) {
                    html += '<div class="chat-tool-tags"><span class="chat-event-state"><span class="state-icon">📎</span>Artifact</span></div>';
                }

                if (entry.error) {
                    html += '<div class="chat-event-bubble error"><p>⚠️ ' + escapeHtml(entry.error.message || 'Unknown error') + '</p></div>';
                }

                if (entry.text) {
                    html += md(entry.text);
                }

                return html;
            }

            function updateEntryDom(entry) {
                if (!entry.el) return;
                if (entry.role === 'user') {
                    entry.el.innerHTML = md(entry.text || '');
                } else {
                    entry.el.innerHTML = renderEntryHtml(entry);
                }
                messages.scrollTop = messages.scrollHeight;
            }

            function createEntryDom(entry) {
                const div = document.createElement('div');
                if (entry.role === 'user') {
                    div.className = 'chat-user-query markdown';
                    div.innerHTML = md(entry.text || '');
                } else {
                    div.className = 'chat-agent-response markdown';
                    div.innerHTML = renderEntryHtml(entry);
                }
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
                entry.el = div;
            }

            function mergeEntry(target, source) {
                target.text += source.text;
                if (source.functionCalls.length) {
                    target.functionCalls = target.functionCalls.concat(source.functionCalls);
                }
                if (source.functionResponses.length) {
                    target.functionResponses = target.functionResponses.concat(source.functionResponses);
                }
                if (source.stateDelta) target.stateDelta = source.stateDelta;
                if (source.artifactDelta) target.artifactDelta = source.artifactDelta;
                if (source.error) target.error = source.error;
                target.eventId = source.eventId;
                target.event = source.event;
            }

            function appendEvent(event) {
                const newEntry = buildEntryFromEvent(event);

                if (event.partial) {
                    if (uiEntries.length > 0) {
                        const last = uiEntries[uiEntries.length - 1];
                        if (last.partial && last.role === newEntry.role) {
                            mergeEntry(last, newEntry);
                            updateEntryDom(last);
                            return;
                        }
                    }
                    uiEntries.push(newEntry);
                    createEntryDom(newEntry);
                } else {
                    let idx = -1;
                    if (event.id) {
                        idx = uiEntries.findIndex(function(e) { return e.eventId === event.id; });
                    }
                    if (idx < 0 && uiEntries.length > 0) {
                        const last = uiEntries[uiEntries.length - 1];
                        if (last.partial && last.role === newEntry.role) {
                            idx = uiEntries.length - 1;
                        }
                    }

                    if (idx >= 0) {
                        const oldEntry = uiEntries[idx];
                        if (newEntry.text || newEntry.functionCalls.length || newEntry.functionResponses.length) {
                            newEntry.el = oldEntry.el;
                            newEntry.eventCounter = oldEntry.eventCounter;
                            uiEntries[idx] = newEntry;
                            updateEntryDom(newEntry);
                        } else {
                            oldEntry.partial = false;
                            oldEntry.eventId = newEntry.eventId;
                            if (newEntry.stateDelta) oldEntry.stateDelta = newEntry.stateDelta;
                            if (newEntry.artifactDelta) oldEntry.artifactDelta = newEntry.artifactDelta;
                            if (newEntry.error) oldEntry.error = newEntry.error;
                            updateEntryDom(oldEntry);
                        }
                    } else {
                        uiEntries.push(newEntry);
                        createEntryDom(newEntry);
                    }
                }
            }

            async function ensureSession() {
                if (sessionId) return sessionId;
                const res = await fetch(`${API_BASE}/apps/${APP_NAME}/users/${USER_ID}/sessions`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: '{}'
                });
                if (!res.ok) throw new Error('创建会话失败：' + res.status);
                const session = await res.json();
                sessionId = session.id;
                return sessionId;
            }

            async function handleSend() {
                const text = input.value.trim();
                if (!text || isLoading) return;
                createTextBubble('user', md(text));
                input.value = '';

                isLoading = true;
                send.disabled = true;
                input.disabled = true;

                try {
                    const sid = await ensureSession();
                    const res = await fetch(`${API_BASE}/run_sse`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            app_name: APP_NAME,
                            user_id: USER_ID,
                            session_id: sid,
                            new_message: { role: 'user', parts: [{ text: text }] },
                            streaming: true
                        })
                    });
                    if (!res.ok) {
                        const errText = await res.text();
                        throw new Error('请求失败：' + errText);
                    }

                    const reader = res.body.getReader();
                    const dec = new TextDecoder();
                    let buf = '';
                    for (;;) {
                        const { value, done } = await reader.read();
                        if (done) break;
                        buf += dec.decode(value, { stream: true });
                        let idx;
                        while ((idx = buf.indexOf('\\n\\n')) >= 0) {
                            const block = buf.slice(0, idx);
                            buf = buf.slice(idx + 2);
                            const line = block.split('\\n').find(function(l) { return l.startsWith('data:'); });
                            if (!line) continue;
                            const json = line.slice(5).trim();
                            if (!json) continue;
                            const ev = JSON.parse(json);
                            if (ev.error) throw new Error(ev.error);
                            appendEvent(ev);
                        }
                    }
                } catch (err) {
                    createTextBubble('model', '<p>抱歉，服务暂时不可用：' + err.message + '</p>');
                } finally {
                    isLoading = false;
                    send.disabled = false;
                    input.disabled = false;
                    input.focus();
                }
            }

            send.addEventListener('click', handleSend);
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') handleSend();
            });
        })();
    </script>
</body>
</html>
"""
