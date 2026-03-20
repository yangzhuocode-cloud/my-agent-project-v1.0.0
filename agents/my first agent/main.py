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
    
    # 3. 上下文配置（基于 token 限制）
    SYSTEM_PROMPT = "你是一个专业的AI助手，基于豆包模型提供回答"
    MODEL_MAX_TOKENS = 256000  # 256k 上下文窗口（256k = 256,000 tokens）
    CONTEXT_SAFETY_RATIO = 0.80  # 保留 80% 给历史，20% 给新回复
    MAX_CONTEXT_TOKENS = int(MODEL_MAX_TOKENS * CONTEXT_SAFETY_RATIO)  # 204,800 tokens

# ===================== 火山方舟豆包Agent核心类 =====================
class VolcArkDoubaoAgent:
    def __init__(self):
        self.config = VolcArkDoubaoConfig()
        # 初始化上下文（符合OpenAI协议格式，火山方舟兼容）
        self.context = [{"role": "system", "content": self.config.SYSTEM_PROMPT}]

    def _estimate_tokens(self, messages):
        """粗略估算 token 数（中英文混合）"""
        total_tokens = 0
        for msg in messages:
            content = msg["content"]
            # 统计中文字符
            chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            # 统计其他字符（英文、数字、符号等）
            other_chars = len(content) - chinese_chars
            
            # 中文: 1 字 ≈ 1.8 tokens
            # 英文: 1 字符 ≈ 0.25 tokens (约 4 字符 = 1 token)
            total_tokens += chinese_chars * 1.8 + other_chars * 0.25
        
        return int(total_tokens)
    
    def _trim_context(self):
        """基于 token 数裁剪上下文，避免超长触发火山方舟限制"""
        current_tokens = self._estimate_tokens(self.context)
        
        # 如果超过限制，从最旧的对话开始删除（保留 system prompt）
        while current_tokens > self.config.MAX_CONTEXT_TOKENS and len(self.context) > 1:
            # 删除第二条消息（第一条是 system prompt）
            self.context.pop(1)
            current_tokens = self._estimate_tokens(self.context)
    


    def call_volc_ark_api(self, user_input):
        """调用火山方舟兼容OpenAI协议的豆包API"""
        # 1. 添加用户输入到上下文
        self.context.append({"role": "user", "content": user_input})
        
        # 2. 【发送前】基于估算裁剪 + 显示估算值
        self._trim_context()
        estimated_tokens = self._estimate_tokens(self.context)
        estimated_percent = (estimated_tokens / self.config.MODEL_MAX_TOKENS) * 100
        print(f"[发送中] 上下文: ~{estimated_percent:.1f}% (~{estimated_tokens} tokens, 估算)")

        # 3. 构造请求头（火山方舟鉴权：Bearer + API Key）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.API_KEY}"
        }

        # 4. 构造请求体（严格遵循OpenAI协议，火山方舟兼容）
        payload = {
            "model": self.config.MODEL,  # 必须和火山方舟控制台的模型名一致
            "messages": self.context,
            "temperature": self.config.TEMPERATURE,
            "max_tokens": self.config.MAX_TOKENS,
            "top_p": self.config.TOP_P,
            "stream": self.config.STREAM
        }

        try:
            # 5. 发送POST请求（火山方舟的OpenAI兼容地址）
            response = requests.post(
                url=f"{self.config.BASE_URL}/chat/completions",  # 补全chat/completions路径
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False),
                timeout=30
            )
            # 6. 检查HTTP状态码
            response.raise_for_status()
            result = response.json()

            # 7. 提取回复并加入上下文
            assistant_reply = result["choices"][0]["message"]["content"]
            self.context.append({"role": "assistant", "content": assistant_reply})
            
            # 8. 【收到后】显示真实 token 使用情况（带降级策略）
            usage = result.get("usage", {})
            if usage and "prompt_tokens" in usage:
                # 成功获取 OpenAI 协议的 usage 信息
                actual_prompt = usage.get("prompt_tokens", 0)
                actual_completion = usage.get("completion_tokens", 0)
                actual_total = usage.get("total_tokens", 0)
                actual_percent = (actual_prompt / self.config.MODEL_MAX_TOKENS) * 100
                
                print(f"[真实值] 上下文: {actual_percent:.1f}% ({actual_prompt}/{self.config.MODEL_MAX_TOKENS} tokens)")
                print(f"         本次回复: {actual_completion} tokens | 总消耗: {actual_total} tokens")
            else:
                # 降级策略：API 未返回 usage（非标准 OpenAI 协议）
                fallback_tokens = self._estimate_tokens(self.context)
                fallback_percent = (fallback_tokens / self.config.MODEL_MAX_TOKENS) * 100
                
                print(f"⚠️  [警告] 当前模型 API 未返回 usage 信息（非标准 OpenAI 协议）")
                print(f"[降级值] 上下文: {fallback_percent:.1f}% (~{fallback_tokens} tokens, 估算)")
                print(f"         本项目依赖 OpenAI 协议的 usage 字段，非兼容协议可能导致 token 统计不准确")

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