import sys, json, requests, os

def main():
    base_url = os.getenv("API_BASE_URL", "https://gaidc.seraphimpower.com.cn")
    # 这里简化写死，实际可以从 env 读取
    url = f"{base_url}/api/v1/auth/login"
    payload = {"username": "admin", "password": "admin123"}
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # 假设 Token 在 data['data']['token']
            token = data.get('data', {}).get('token') or data.get('access_token')
            if token:
                print(json.dumps({"status": "success", "token": token}))
            else:
                print(json.dumps({"status": "error", "msg": "未找到Token字段"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "msg": resp.text}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "msg": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()