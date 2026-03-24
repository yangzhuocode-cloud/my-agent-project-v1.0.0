#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI 兼容 API Agent
"""

import sys
import io

# ===================== 跨平台编码兼容性 =====================
# 确保标准输出使用 UTF-8 编码，避免 Windows 系统 GBK 编码问题
# 参考: docs/adr/004-cross-platform-encoding.md
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import json
import time
import re

# ===================== 通用 API 配置（OpenAI 兼容） =====================
class APIModelConfig:
    # 1. API 核心配置（替换为你的真实信息）
    API_KEY = "your-api-key-here"  # 从 API 提供商控制台获取的 API Key
    BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"  # API 端点地址
    MODEL = "your-model-name"  # 模型名称
    
    # 2. 生成参数
    TEMPERATURE = 0.7    # 随机性 0-1
    MAX_TOKENS = 2000    # 最大回复长度
    TOP_P = 0.9          # 采样阈值
    STREAM = False       # 关闭流式输出
    
    # 3. 上下文配置（基于 token 限制）
    SYSTEM_PROMPT = "你是一个专业的AI助手"
    MODEL_MAX_TOKENS = 256000  # 256k 上下文窗口（256k = 256,000 tokens）
    CONTEXT_SAFETY_RATIO = 0.80  # 保留 80% 给历史，20% 给新回复
    MAX_CONTEXT_TOKENS = int(MODEL_MAX_TOKENS * CONTEXT_SAFETY_RATIO)  # 204,800 tokens
    TRIM_THRESHOLD = 0.80  # 达到 80% 时触发裁剪
    TRIM_TARGET = 0.60  # 裁剪到 60%

# ===================== 消息优先级定义 =====================
class MessagePriority:
    CRITICAL = 10   # 永不删除（System、任务）
    HIGH = 8        # 尽量保留（新错误、文件操作）
    MEDIUM = 5      # 可压缩（成功操作）
    LOW = 2         # 可删除（思考过程）

# ===================== 通用 Agent 核心类 =====================
class APIModelAgent:
    def __init__(self):
        self.config = APIModelConfig()
        # 分层上下文存储结构
        self.context = {
            # 第1层：永久保留（不参与裁剪）
            "permanent": {
                "system": self.config.SYSTEM_PROMPT,
                "task": ""  # 用户原始任务（可选）
            },
            # 第2层：重要信息（压缩保留）
            "important": {
                "errors": [],      # 错误历史（去重）
                "milestones": []   # 里程碑事件
            },
            # 第3层：滚动窗口（完整保留最近N条）
            "recent": []
        }
        self.error_signatures = []  # 用于错误去重

    
    def set_task(self, task):
        """设置用户原始任务"""
        self.context["permanent"]["task"] = task
    
    def _is_error(self, content):
        """判断是否是错误信息"""
        error_keywords = ["错误", "失败", "Error", "Exception", "Traceback", "Failed", "无法"]
        return any(kw in content for kw in error_keywords)
    
    def _is_file_operation(self, content):
        """判断是否是文件操作"""
        file_keywords = ["创建文件", "修改文件", "删除文件", "写入", "保存", "创建了", "修改了"]
        return any(kw in content for kw in file_keywords)
    
    def _get_error_signature(self, error_text):
        """生成错误签名用于去重"""
        # 提取错误类型
        error_type_match = re.search(r'(\w+Error|\w+Exception)', error_text)
        error_type = error_type_match.group(1) if error_type_match else ""
        
        # 提取关键信息（忽略行号）
        normalized = re.sub(r'line \d+', '', error_text)
        normalized = re.sub(r'\d{4}-\d{2}-\d{2}', '', normalized)
        
        # 提取引号中的内容
        key_info = re.findall(r"'([^']*)'", normalized)
        
        # 生成签名
        signature = f"{error_type}:{':'.join(key_info)}"
        return signature
    
    def _is_duplicate_error(self, error_text):
        """判断是否是重复错误"""
        new_signature = self._get_error_signature(error_text)
        
        # 检查错误历史
        for error_record in self.context["important"]["errors"]:
            if error_record["signature"] == new_signature:
                # 更新重复次数
                error_record["count"] += 1
                error_record["last_seen"] = time.time()
                return True
        
        # 新错误，添加到历史
        self.context["important"]["errors"].append({
            "signature": new_signature,
            "message": error_text[:200],
            "timestamp": time.time(),
            "count": 1
        })
        
        # 限制错误历史大小
        if len(self.context["important"]["errors"]) > 20:
            self.context["important"]["errors"].pop(0)
        
        return False
    
    def _calculate_priority(self, content, role):
        """计算消息优先级"""
        # 规则1：System prompt - 永不删除
        if role == "system":
            return MessagePriority.CRITICAL
        
        # 规则2：原始任务 - 永不删除
        if content.startswith("任务："):
            return MessagePriority.CRITICAL
        
        # 规则3：错误信息 - 高优先级
        if self._is_error(content):
            if self._is_duplicate_error(content):
                return MessagePriority.MEDIUM  # 重复错误降低优先级
            return MessagePriority.HIGH
        
        # 规则4：文件操作 - 高优先级
        if self._is_file_operation(content):
            return MessagePriority.HIGH
        
        # 规则5：成功操作 - 中优先级
        if "成功" in content or "完成" in content:
            return MessagePriority.MEDIUM
        
        # 规则6：思考过程 - 低优先级
        if any(kw in content for kw in ["让我想想", "分析", "考虑"]):
            return MessagePriority.LOW
        
        # 默认优先级
        return MessagePriority.MEDIUM
    
    def add_message(self, role, content):
        """添加消息并自动标记优先级"""
        message = {
            "role": role,
            "content": content,
            "priority": self._calculate_priority(content, role),
            "timestamp": time.time()
        }
        self.context["recent"].append(message)
    
    def _format_error_summary(self):
        """格式化错误历史为摘要"""
        errors = self.context["important"]["errors"]
        if not errors:
            return ""
        
        summary_lines = ["历史错误记录："]
        for error in errors[-5:]:  # 只显示最近5个
            if error["count"] > 1:
                summary_lines.append(f"- {error['signature']} (出现 {error['count']} 次)")
            else:
                summary_lines.append(f"- {error['message'][:100]}")
        
        return "\n".join(summary_lines)
    
    def build_api_messages(self):
        """构建发送给 API 的消息列表"""
        messages = []
        
        # 1. 添加 system prompt
        messages.append({
            "role": "system",
            "content": self.context["permanent"]["system"]
        })
        
        # 2. 添加任务描述（如果有）
        if self.context["permanent"]["task"]:
            messages.append({
                "role": "user",
                "content": f"任务：{self.context['permanent']['task']}"
            })
        
        # 3. 添加错误历史摘要（如果有）
        if self.context["important"]["errors"]:
            error_summary = self._format_error_summary()
            messages.append({
                "role": "assistant",
                "content": error_summary
            })
        
        # 4. 添加里程碑摘要（如果有）
        if self.context["important"]["milestones"]:
            milestone_summary = "\n".join([f"- {m}" for m in self.context["important"]["milestones"]])
            messages.append({
                "role": "assistant",
                "content": f"已完成的操作：\n{milestone_summary}"
            })
        
        # 5. 添加最近的对话
        for msg in self.context["recent"]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
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
    
    def _estimate_permanent_tokens(self):
        """估算永久层 token"""
        system_tokens = len(self.context["permanent"]["system"]) * 1.2
        task_tokens = len(self.context["permanent"]["task"]) * 1.2
        return int(system_tokens + task_tokens)
    
    def _estimate_important_tokens(self):
        """估算重要信息层 token"""
        error_summary = self._format_error_summary()
        milestone_summary = "\n".join(self.context["important"]["milestones"])
        total_chars = len(error_summary) + len(milestone_summary)
        return int(total_chars * 1.2)
    
    def _estimate_messages_tokens(self, messages):
        """估算消息列表 token"""
        total_chars = sum(len(m["content"]) for m in messages)
        return int(total_chars * 1.2)
    
    def _estimate_current_tokens(self):
        """估算当前总 token 数"""
        total = self._estimate_permanent_tokens()
        total += self._estimate_important_tokens()
        total += self._estimate_messages_tokens(self.context["recent"])
        return total
    
    def _compress_message(self, message):
        """压缩消息内容"""
        content = message["content"]
        
        if self._is_error(content):
            compressed = f"[错误] {content[:150]}..."
        elif self._is_file_operation(content):
            compressed = f"[文件操作] {content[:100]}..."
        elif "成功" in content:
            compressed = f"[成功] {content[:80]}..."
        else:
            compressed = f"[操作] {content[:50]}..."
        
        return {
            **message,
            "content": compressed,
            "compressed": True
        }
    
    def _smart_trim(self):
        """智能裁剪上下文"""
        # 1. 永久层不参与裁剪
        
        # 2. 保留最近 N 轮对话（完整）
        recent_keep_count = 6  # 3轮对话 = 6条消息
        if len(self.context["recent"]) <= recent_keep_count:
            return  # 消息太少，不需要裁剪
        
        must_keep = self.context["recent"][-recent_keep_count:]
        
        # 3. 对更早的消息按优先级排序
        older = self.context["recent"][:-recent_keep_count]
        older.sort(key=lambda x: x["priority"], reverse=True)
        
        # 4. 计算可用空间
        target_tokens = int(self.config.MAX_CONTEXT_TOKENS * self.config.TRIM_TARGET)
        current_tokens = self._estimate_permanent_tokens()
        current_tokens += self._estimate_important_tokens()
        current_tokens += self._estimate_messages_tokens(must_keep)
        
        # 5. 从旧消息中选择高优先级的，直到填满空间
        selected = []
        for msg in older:
            msg_tokens = self._estimate_messages_tokens([msg])
            if current_tokens + msg_tokens <= target_tokens:
                selected.append(msg)
                current_tokens += msg_tokens
            elif msg["priority"] >= MessagePriority.HIGH:
                # 高优先级消息，压缩后保留
                compressed = self._compress_message(msg)
                compressed_tokens = self._estimate_messages_tokens([compressed])
                if current_tokens + compressed_tokens <= target_tokens:
                    selected.append(compressed)
                    current_tokens += compressed_tokens
        
        # 6. 重新组装（按时间顺序）
        selected.sort(key=lambda x: x["timestamp"])
        self.context["recent"] = selected + must_keep
        
        removed_count = len(older) - len(selected)
        print(f"✂️ 裁剪了 {removed_count} 条消息")
    
    def _check_and_trim(self):
        """检查并触发裁剪"""
        current_tokens = self._estimate_current_tokens()
        usage_ratio = current_tokens / self.config.MAX_CONTEXT_TOKENS
        
        # 达到阈值时触发裁剪
        if usage_ratio >= self.config.TRIM_THRESHOLD:
            print(f"⚠️ Token 使用率达到 {usage_ratio:.1%}，触发智能裁剪")
            self._smart_trim()
    
    def _trim_context(self):
        """基于 token 数裁剪上下文（兼容旧接口）"""
        self._check_and_trim()
    
    def test_connection(self):
        """
        测试 API 连接配置
        
        采用方案 1（最小化测试）+ 方案 3（模型列表验证）组合
        参考: docs/adr/005-api-connection-test.md
        
        Returns:
            dict: 测试结果
        """
        print("=" * 60)
        print("API 连接测试")
        print("=" * 60)
        
        # 阶段 1: 尝试模型列表验证（OpenAI 协议）
        model_test = self._try_verify_model()
        
        if model_test["supported"]:
            # 支持 OpenAI 协议
            if not model_test["success"]:
                # 模型不可用，提前返回错误
                self._print_test_result(model_test)
                return model_test
            else:
                print(model_test["message"])
        else:
            # 不支持 OpenAI 协议
            print("⚠️  当前 API 不支持 OpenAI 标准协议的模型列表接口")
            print("    将跳过模型验证，直接测试对话功能")
            print()
        
        # 阶段 2: 最小化对话测试（必须）
        chat_test = self._test_chat_completion()
        self._print_test_result(chat_test)
        
        return chat_test
    
    def _try_verify_model(self):
        """尝试验证模型（OpenAI 协议）"""
        try:
            response = requests.get(
                f"{self.config.BASE_URL}/models",
                headers={"Authorization": f"Bearer {self.config.API_KEY}"},
                timeout=10
            )
            
            if response.status_code == 200:
                # 支持 OpenAI 协议
                data = response.json()
                available_models = [m["id"] for m in data.get("data", [])]
                
                if self.config.MODEL in available_models:
                    return {
                        "supported": True,
                        "success": True,
                        "message": f"✅ 模型 '{self.config.MODEL}' 可用",
                        "available_models": available_models
                    }
                else:
                    return {
                        "supported": True,
                        "success": False,
                        "error": f"❌ 模型 '{self.config.MODEL}' 不在可用列表中",
                        "available_models": available_models,
                        "suggestion": f"可用模型: {', '.join(available_models[:5])}"
                    }
            else:
                # 不支持或认证失败
                return {"supported": False}
        
        except Exception:
            # 不支持 OpenAI 协议
            return {"supported": False}
    
    def _test_chat_completion(self):
        """测试对话接口（最小化测试）"""
        try:
            payload = {
                "model": self.config.MODEL,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                f"{self.config.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                tokens_used = result.get("usage", {}).get("total_tokens", "未知")
                
                return {
                    "success": True,
                    "message": "✅ API 连接测试成功",
                    "model": self.config.MODEL,
                    "response_preview": reply,
                    "tokens_used": tokens_used
                }
            else:
                return {
                    "success": False,
                    "error": f"❌ HTTP {response.status_code}",
                    "details": response.text[:200]
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "❌ 请求超时",
                "suggestion": "请检查网络连接或 Base URL 是否正确"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "❌ 无法连接到服务器",
                "suggestion": "请检查 Base URL 是否正确"
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"❌ 响应格式错误: 缺少字段 {str(e)}",
                "suggestion": "API 可能不兼容 OpenAI 协议"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"❌ 测试失败: {str(e)}"
            }
    
    def _print_test_result(self, result):
        """打印测试结果"""
        if result["success"]:
            print(result["message"])
            if "response_preview" in result:
                print(f"    模型: {result['model']}")
                print(f"    回复预览: {result['response_preview']}")
                print(f"    Token 消耗: {result['tokens_used']}")
        else:
            print(result["error"])
            if "suggestion" in result:
                print(f"    建议: {result['suggestion']}")
            if "available_models" in result:
                models_str = ', '.join(result['available_models'][:5])
                if len(result['available_models']) > 5:
                    models_str += f" (共 {len(result['available_models'])} 个)"
                print(f"    可用模型: {models_str}")
            if "details" in result:
                print(f"    详情: {result['details']}")
        
        print("=" * 60)

    def call_api(self, user_input):
        """调用 OpenAI 兼容 API"""
        # 1. 添加用户输入到上下文
        self.add_message("user", user_input)
        
        # 2. 检查并裁剪
        self._check_and_trim()
        
        # 3. 构建 API 消息
        api_messages = self.build_api_messages()
        
        # 4. 显示估算值
        estimated_tokens = self._estimate_tokens(api_messages)
        estimated_percent = (estimated_tokens / self.config.MODEL_MAX_TOKENS) * 100
        print(f"[发送中] 上下文: ~{estimated_percent:.1f}% (~{estimated_tokens} tokens, 估算)")

        # 5. 构造请求头（API 鉴权：Bearer + API Key）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.API_KEY}"
        }

        # 6. 构造请求体（遵循 OpenAI 协议）
        payload = {
            "model": self.config.MODEL,
            "messages": api_messages,
            "temperature": self.config.TEMPERATURE,
            "max_tokens": self.config.MAX_TOKENS,
            "top_p": self.config.TOP_P,
            "stream": self.config.STREAM
        }

        try:
            # 7. 发送POST请求
            response = requests.post(
                url=f"{self.config.BASE_URL}/chat/completions",
                headers=headers,
                json=payload,  # 使用 json 参数自动处理序列化
                timeout=30
            )
            # 8. 检查HTTP状态码
            response.raise_for_status()
            result = response.json()

            # 9. 提取回复并加入上下文
            assistant_reply = result["choices"][0]["message"]["content"]
            self.add_message("assistant", assistant_reply)
            
            # 10. 显示真实 token 使用情况
            usage = result.get("usage", {})
            if usage and "prompt_tokens" in usage:
                actual_prompt = usage.get("prompt_tokens", 0)
                actual_completion = usage.get("completion_tokens", 0)
                actual_total = usage.get("total_tokens", 0)
                actual_percent = (actual_prompt / self.config.MODEL_MAX_TOKENS) * 100
                
                print(f"[真实值] 上下文: {actual_percent:.1f}% ({actual_prompt}/{self.config.MODEL_MAX_TOKENS} tokens)")
                print(f"         本次回复: {actual_completion} tokens | 总消耗: {actual_total} tokens")
            else:
                # 降级策略
                fallback_tokens = self._estimate_current_tokens()
                fallback_percent = (fallback_tokens / self.config.MODEL_MAX_TOKENS) * 100
                
                print(f"⚠️  [警告] 当前模型 API 未返回 usage 信息（非标准 OpenAI 协议）")
                print(f"[降级值] 上下文: {fallback_percent:.1f}% (~{fallback_tokens} tokens, 估算)")

            return assistant_reply

        except requests.exceptions.RequestException as e:
            print(f"API 调用失败：{str(e)}")
            # 失败时清理本次用户输入
            if len(self.context["recent"]) > 0 and self.context["recent"][-1]["role"] == "user":
                self.context["recent"].pop()
            # 打印详细错误信息
            if hasattr(e, 'response') and e.response is not None:
                print(f"错误响应状态码：{e.response.status_code}")
                print(f"错误响应内容：{e.response.text}")
            return None

# ===================== 测试运行 =====================
if __name__ == "__main__":
    agent = APIModelAgent()
    print("API Agent 已启动（OpenAI 兼容版），输入'退出'结束对话")
    while True:
        user_input = input("\n你：")
        if user_input.strip() == "退出":
            print("Agent已退出")
            break
        reply = agent.call_api(user_input)
        if reply:
            print(f"Agent：{reply}")
        else:
            print("Agent：抱歉，我暂时无法回答你的问题")