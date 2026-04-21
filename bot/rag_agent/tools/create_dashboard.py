import requests
import json
import sys


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
    

def do_request(token, data):
    """使用 Token 和 dashboard json 发起 POST 请求"""
    url = f"{BASE_URL}/api/v1/dashboard/configs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"[API] 正在请求: {url}")
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
        print(f"[API] 状态码: {resp.status_code}")

        if resp.status_code == 409:
            return {"status": "error", "code": 409, "msg": f"{resp.text[:200]}"}
        
        if resp.status_code == 200:
            return resp.json()
        
        if resp.status_code == 401:
            return {"status": "error", "msg": "认证失败 (401)，Token 可能已过期"}
        
        return {"status": "error", "msg": f"API 错误 ({resp.status_code}): {resp.text[:200]}"}
            
    except Exception as e:
        return {"status": "error", "msg": f"请求异常: {str(e)}"}
    

def create_dashboard(data: str):
    '''
    在api—skill生成dashboard json格式字符串后，调用此工具创建dashboard

    Args：
        data（str）：依据api-skill生成的符合规范的dashboard json格式字符串
    '''


    # 1. 自动登录
    print("[LOGIC] 未提供 Token，执行自动登录...")
    token = do_login()
    if not token:
        print(json.dumps({"status": "error", "msg": "自动登录失败，无法继续"}))
        sys.exit(1)
    

    # 2. 发起请求
    data = json.loads(data)
    result = do_request(token, data)
    
    # 3. 处理 401 重试逻辑 (最多重试一次)
    if result.get("msg") == "认证失败 (401)，Token 可能已过期":
        print("[LOGIC] 检测到 401，尝试重新登录并重试...")
        token = do_login()
        result = do_request(token, data)


    # 5. 输出最终结果
    print(json.dumps(result))