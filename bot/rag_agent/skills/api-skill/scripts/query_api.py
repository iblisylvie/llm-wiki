import sys
import json
import requests
import argparse

def main():
    input_data = ""
    
    # 1. 尝试从标准输入（stdin）读取数据 (ADK 模式)
    # check_eof=False 防止在没有输入时立即报错
    if not sys.stdin.isatty(): 
        try:
            input_data = sys.stdin.read()
            params = json.loads(input_data)
            path = params.get('path')
            token = params.get('token')
            print(f"[DEBUG] ADK模式: 从 stdin 读取到参数")
        except json.JSONDecodeError as e:
            print(f"[DEBUG] ADK模式失败: {str(e)}，尝试命令行模式...")
            path = None
            token = None
    else:
        path = None
        token = None

    # 2. 如果 stdin 读取失败（或者没有数据），则尝试解析命令行参数 (CLI 模式)
    if not path or not token:
        print(f"[DEBUG] CLI模式: 解析命令行参数")
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', type=str, required=False, help='API Path')
        parser.add_argument('--token', type=str, required=False, help='Auth Token')
        args = parser.parse_args()
        
        # 如果命令行也没传，就报错
        if not args.path or not args.token:
            print(json.dumps({"status": "error", "msg": "缺少参数: 请通过 stdin 或 --path/--token 传参"}))
            sys.exit(1)
            
        path = args.path
        token = args.token

    # 3. 核心请求逻辑 (保持不变)
    base_url = "https://gaidc.seraphimpower.com.cn"
    url = f"{base_url}{path}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"[DEBUG] 请求 URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"[DEBUG] HTTP 状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # 直接打印 JSON 结果
                result = response.json()
                print(json.dumps(result))
            except json.JSONDecodeError:
                print(json.dumps({"status": "error", "msg": "响应不是合法JSON"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "msg": f"HTTP {response.status_code}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"status": "error", "msg": f"请求异常: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()