import sys
import json
import requests
import argparse
import os

# ================= 配置区域 =================
BASE_URL = "https://gaidc.seraphimpower.com.cn"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
USERNAME = "admin"
PASSWORD = "admin123"
# ===========================================

def do_login():
    """执行登录并返回 Token"""
    print(f"[AUTH] 正在尝试登录: {LOGIN_URL}")
    try:
        payload = {"username": USERNAME, "password": PASSWORD}
        # 这里的 verify=False 是为了适应自签名证书环境
        resp = requests.post(LOGIN_URL, json=payload, timeout=10, verify=False)
        
        if resp.status_code == 200:
            data = resp.json()
            # 尝试多种常见的 Token 字段位置
            token = data.get("access_token") or \
                    data.get("token") or \
                    data.get("data", {}).get("access_token") or \
                    data.get("data", {}).get("token")
            
            if token:
                print(f"[AUTH] 登录成功，获取 Token: {token[:10]}...")
                return token
            else:
                print(f"[AUTH] 登录失败：响应中未找到 Token 字段。原始响应: {data}")
                return None
        else:
            print(f"[AUTH] 登录失败：HTTP {resp.status_code} - {resp.text}")
            return None
    except Exception as e:
        print(f"[AUTH] 登录异常: {str(e)}")
        return None

def do_request(path, token):
    """使用 Token 发起 GET 请求"""
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"[API] 正在请求: {url}")
    
    try:
        resp = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"[API] 状态码: {resp.status_code}")
        
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            return {"status": "error", "msg": "认证失败 (401)，Token 可能已过期"}
        else:
            return {"status": "error", "msg": f"API 错误 ({resp.status_code}): {resp.text[:200]}"}
            
    except Exception as e:
        return {"status": "error", "msg": f"请求异常: {str(e)}"}

def main():
    # 1. 解析参数 (兼容 ADK 的 stdin 模式和 命令行的 argparse 模式)
    input_data = ""
    
    try:
        input_data = sys.stdin.read()
        params = json.loads(input_data)
        path = params.get('path')
        token = params.get('token')
    except:
        path, token = None, None

    if not path:
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', type=str, required=False)
        args = parser.parse_args()
        path= args.path

    if not path:
        print(json.dumps({"status": "error", "msg": "缺少必要参数: path"}))
        sys.exit(1)

    # 2. 智能 Token 处理逻辑
    current_token = token
    
    # 如果没有传 Token，或者传了但请求返回 401，则自动登录
    if not current_token:
        print("[LOGIC] 未提供 Token，执行自动登录...")
        current_token = do_login()
        if not current_token:
            print(json.dumps({"status": "error", "msg": "自动登录失败，无法继续"}))
            sys.exit(1)
    
    # 3. 发起请求
    result = do_request(path, current_token)
    result = do_request(path, current_token)
    
    # 4. 处理 401 重试逻辑 (最多重试一次)
    if result.get("msg") == "认证失败 (401)，Token 可能已过期":
        print("[LOGIC] 检测到 401，尝试重新登录并重试...")
        new_token = do_login()
        if new_token:
            result = do_request(path, new_token)
        else:
            result = {"status": "error", "msg": "Token 过期且重新登录失败"}

    # 5. 输出最终结果
    print(json.dumps(result))

if __name__ == "__main__":
    main()