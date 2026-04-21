# 1. 在主机环境中启动
PORT=8804 ADK_API_HOST=0.0.0.0  python main.py

# 2. 在Docker环境中启动
## 2.1 构建镜像（在项目根目录执行）                       
docker build -t llm-wiki-bot .                    
                                                          
## 2.2 运行容器                                           
docker run -d \                                         
    -p 8804:8080 \                                        
    -v /root/llm-wiki/wiki:/wiki \                        
    -v /root/llm-wiki/site:/site \                        
    -e DASHSCOPE_API_KEY=你的API密钥 \                    
    --name llm-wiki-bot \                                 
    llm-wiki-bot

# 3. 获取API接口定义

