"""HTML/CSS/JS templates for the generated site."""

SITE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Wiki</title>
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
</body>
</html>
"""
