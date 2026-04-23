#!/bin/sh
set -e

resolve_url() {
    url="$1"
    # 提取域名部分（如 host.docker.internal）
    host=$(printf '%s' "$url" | sed -n 's#.*://\([^/:]*\).*#\1#p')
    if [ -z "$host" ]; then
        printf '%s' "$url"
        return
    fi
    # 从 /etc/hosts 解析（--add-host 写入的位置）
    ip=$(awk -v h="$host" '$2 == h {print $1; exit}' /etc/hosts)
    if [ -n "$ip" ]; then
        printf '%s' "$url" | sed "s/$host/$ip/"
    else
        printf '%s' "$url"
    fi
}

if [ -n "$BOT_API_BASE" ]; then
    RESOLVED=$(resolve_url "$BOT_API_BASE")
    cat > /etc/nginx/conf.d/default.conf <<EOF
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass ${RESOLVED}/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_buffering off;
        proxy_cache off;
    }

    location /raw {
        autoindex on;
        charset utf-8;
        source_charset utf-8;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|apng)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    sed -i "s#window\.BOT_API_BASE || '.*'#window.BOT_API_BASE || '/api'#g" /usr/share/nginx/html/index.html
else
    cat > /etc/nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /raw {
        autoindex on;
        charset utf-8;
        source_charset utf-8;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|apng)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }
}
EOF
fi

exec "$@"
