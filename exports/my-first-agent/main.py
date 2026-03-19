import requests
import json

# ===================== 火山方舟配置（严格匹配官网） =====================
class VolcArkDoubaoConfig:
    # 1. 火山方舟核心配置（替换为你的真实信息）
    API_KEY = "7fc03e54-05c9-472c-ada1-0772ff255db5"  # 从火山方舟控制台获取的API Key
    BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"  # 官网指定的OpenAI兼容地址
    MODEL = "Doubao-Seed-2.0-pro"  # 火山方舟控制台显示的模型名（如ark-code-latest/doubao-pro）
    
    # 2. 生成参数（火山方舟支持的参数）
    TEMPERATURE = 0.7    # 随机性 0-1
    MAX_TOKENS = 2000    # 最大回复长度
    TOP_P = 0.9          # 采样阈值
    STREAM = False       # 关闭流式输出
    
    # 3. 上下文配置
    SYSTEM_PROMPT = "你是一个专业的AI助手，基于豆包模型提供回答"
    CONTEXT_MAX_LENGTH = 10  # 最大保留10轮对话

# ===================== 火山方舟豆包Agent核心类 =====================
class VolcArkDoubaoAgent:
    def __init__(self):
        self.config = VolcArkDoubaoConfig()
        # 初始化上下文（符合OpenAI协议格式，火山方舟兼容）
        self.context = [{"role": "system", "content": self.config.SYSTEM_PROMPT}]

    def _trim_context(self):
        """裁剪上下文，避免超长触发火山方舟限制"""
        if len(self.context) > self.config.CONTEXT_MAX_LENGTH + 1:
            self.context = [self.context[0]] + self.context[-self.config.CONTEXT_MAX_LENGTH:]

    def call_volc_ark_api(self, user_input):
        """调用火山方舟兼容OpenAI协议的豆包API"""
        # 1. 添加用户输入到上下文
        self.context.append({"role": "user", "content": user_input})
        self._trim_context()

        # 2. 构造请求头（火山方舟鉴权：Bearer + API Key）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.API_KEY}"
        }

        # 3. 构造请求体（严格遵循OpenAI协议，火山方舟兼容）
        payload = {
            "model": self.config.MODEL,  # 必须和火山方舟控制台的模型名一致
            "messages": self.context,
            "temperature": self.config.TEMPERATURE,
            "max_tokens": self.config.MAX_TOKENS,
            "top_p": self.config.TOP_P,
            "stream": self.config.STREAM
        }

        try:
            # 4. 发送POST请求（火山方舟的OpenAI兼容地址）
            response = requests.post(
                url=f"{self.config.BASE_URL}/chat/completions",  # 补全chat/completions路径
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False),
                timeout=30
            )
            # 5. 检查HTTP状态码
            response.raise_for_status()
            result = response.json()

            # 6. 提取回复并加入上下文
            assistant_reply = result["choices"][0]["message"]["content"]
            self.context.append({"role": "assistant", "content": assistant_reply})

            return assistant_reply

        except requests.exceptions.RequestException as e:
            print(f"火山方舟API调用失败：{str(e)}")
            # 失败时清理本次用户输入
            if len(self.context) > 1 and self.context[-1]["role"] == "user":
                self.context.pop()
            # 打印详细错误信息用于排查
            if hasattr(e, 'response') and e.response is not None:
                print(f"错误响应状态码：{e.response.status_code}")
                print(f"错误响应内容：{e.response.text}")
            return None

# ===================== 测试运行 =====================
if __name__ == "__main__":
    agent = VolcArkDoubaoAgent()
    print("火山方舟-豆包Agent已启动（OpenAI兼容版），输入'退出'结束对话")
    while True:
        user_input = input("\n你：")
        if user_input.strip() == "退出":
            print("Agent已退出")
            break
        reply = agent.call_volc_ark_api(user_input)
        if reply:
            print(f"豆包：{reply}")
        else:
            print("豆包：抱歉，我暂时无法回答你的问题")