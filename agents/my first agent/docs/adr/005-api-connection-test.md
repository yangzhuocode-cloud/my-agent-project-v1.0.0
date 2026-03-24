# ADR-005: API 连接测试方案

## 状态
已接受

## 背景

在 Agent 开发和使用过程中，用户需要配置 API 密钥、Base URL 和模型名称。如果配置错误，会导致运行时错误，影响用户体验。

### 常见配置问题

1. **API 密钥错误**
   - 密钥过期
   - 密钥格式错误
   - 权限不足

2. **Base URL 错误**
   - URL 拼写错误
   - 协议错误（http vs https）
   - 端点路径错误

3. **模型名称错误**
   - 模型名拼写错误
   - 模型不存在
   - 账户无权访问该模型

### 用户需求

用户希望在正式使用前，能够快速验证配置是否正确，类似于其他 AI 工具（Cursor、ChatGPT Web UI 等）提供的"测试连接"功能。

### 设计目标

1. **快速验证**：几秒内完成测试
2. **成本低**：消耗最少的 token
3. **信息明确**：清晰的成功/失败提示
4. **兼容性好**：支持 OpenAI 协议和非标准协议


## 备选方案

### 方案 1: 最小化测试请求 ✅

**原理**：发送一个最简单的对话请求，验证基本连通性

**实现**：
```python
def test_connection(api_key, base_url, model):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5  # 限制回复长度
    }
    
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=10
    )
    
    return response.status_code == 200
```

**优点**：
- 成本低（< 10 tokens）
- 速度快（几秒内完成）
- 实现简单
- 验证实际对话功能
- 适用于所有 API

**缺点**：
- 无法提前发现模型名错误
- 错误信息可能不够明确

**适用场景**：
- 所有 API（包括非 OpenAI 协议）
- 快速验证
- 成本敏感场景

---

### 方案 2: 健康检查端点

**原理**：调用专门的健康检查接口

**实现**：
```python
def test_health(api_key, base_url):
    response = requests.get(
        f"{base_url}/health",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=5
    )
    return response.status_code == 200
```

**优点**：
- 不消耗 token
- 速度最快
- 专门用于测试

**缺点**：
- 不是所有 API 都提供
- 无法验证实际对话功能
- 无法验证模型配置

**适用场景**：
- 支持健康检查的 API
- 频繁测试场景

**为什么不选**：大多数 API 不提供健康检查端点

---

### 方案 3: 模型列表验证 ✅

**原理**：先获取可用模型列表，验证配置的模型是否存在

**实现**：
```python
def verify_model(api_key, base_url, model):
    # 步骤 1: 获取模型列表
    response = requests.get(
        f"{base_url}/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        available_models = [m["id"] for m in data.get("data", [])]
        
        # 步骤 2: 验证模型是否存在
        if model in available_models:
            return True, available_models
        else:
            return False, available_models
    else:
        # API 不支持模型列表
        return None, []
```

**优点**：
- 提前发现模型名错误
- 提供可用模型列表
- 友好的错误提示
- 不消耗对话 token

**缺点**：
- 需要额外请求
- 不是所有 API 都支持（非 OpenAI 协议）
- 无法验证实际对话功能

**适用场景**：
- OpenAI 兼容协议的 API
- 用户首次配置
- 需要友好提示的场景

---

### 方案 4: 分级测试

**原理**：从简单到复杂，逐步验证

**实现**：
```python
def comprehensive_test(api_key, base_url, model):
    tests = []
    
    # 测试 1: URL 连通性
    tests.append(test_url_connectivity(base_url))
    
    # 测试 2: API 密钥认证
    tests.append(test_authentication(api_key, base_url))
    
    # 测试 3: 模型可用性
    tests.append(test_model_availability(api_key, base_url, model))
    
    # 测试 4: 对话功能
    tests.append(test_chat_completion(api_key, base_url, model))
    
    return tests
```

**优点**：
- 全面验证各个环节
- 详细的诊断信息
- 能定位具体问题

**缺点**：
- 耗时较长
- 消耗更多 token
- 实现复杂
- 用户等待时间长

**适用场景**：
- 调试和诊断
- 企业级应用
- 需要详细报告的场景

**为什么不选**：过于复杂，用户体验不佳


## 决策

我们采用 **方案 1（最小化测试）+ 方案 3（模型列表验证）** 的组合方案，并实现智能降级。

### 核心策略

```python
def test_api_config(api_key, base_url, model):
    """测试 API 配置"""
    
    # 阶段 1: 尝试模型列表验证（OpenAI 协议）
    model_test = try_verify_model(api_key, base_url, model)
    
    if model_test["supported"]:
        # 支持 OpenAI 协议
        if not model_test["success"]:
            # 模型不可用，提前返回错误
            return model_test
    else:
        # 不支持 OpenAI 协议，提示用户
        print("⚠️ 当前 API 不支持 OpenAI 标准协议的模型列表接口")
    
    # 阶段 2: 最小化对话测试（必须）
    chat_test = test_chat_completion(api_key, base_url, model)
    
    return chat_test
```

### 决策依据

1. **兼容性优先**
   - 方案 1 适用于所有 API
   - 方案 3 只适用于 OpenAI 协议
   - 组合方案兼顾两者

2. **用户体验**
   - 支持 OpenAI 协议：提前发现模型错误，提供可用模型列表
   - 不支持 OpenAI 协议：降级到最小化测试，提示用户

3. **成本控制**
   - 模型列表验证不消耗对话 token
   - 最小化测试只消耗 < 10 tokens
   - 总成本 < 10 tokens

4. **速度**
   - 模型列表验证：1-2 秒
   - 最小化测试：2-3 秒
   - 总耗时：< 5 秒

5. **业界实践**
   - Cursor、Continue.dev：方案 1
   - ChatGPT Web UI、Open WebUI：方案 1 + 方案 3
   - LangChain：方案 1
   - Dify、FastGPT：方案 4（分级测试）

### 实现细节

#### 1. 模型列表验证（可选）

```python
def try_verify_model(api_key, base_url, model):
    """尝试验证模型（OpenAI 协议）"""
    try:
        response = requests.get(
            f"{base_url}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        
        if response.status_code == 200:
            # 支持 OpenAI 协议
            data = response.json()
            available_models = [m["id"] for m in data.get("data", [])]
            
            if model in available_models:
                return {
                    "supported": True,
                    "success": True,
                    "message": f"✅ 模型 '{model}' 可用",
                    "available_models": available_models
                }
            else:
                return {
                    "supported": True,
                    "success": False,
                    "error": f"❌ 模型 '{model}' 不在可用列表中",
                    "available_models": available_models,
                    "suggestion": f"可用模型: {', '.join(available_models[:5])}"
                }
        else:
            # 不支持或认证失败
            return {"supported": False}
    
    except Exception:
        # 不支持 OpenAI 协议
        return {"supported": False}
```

#### 2. 最小化对话测试（必须）

```python
def test_chat_completion(api_key, base_url, model):
    """测试对话接口"""
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 5
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "message": "✅ API 连接测试成功",
                "model": model,
                "response_preview": reply,
                "tokens_used": result.get("usage", {}).get("total_tokens", "未知")
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
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ 测试失败: {str(e)}"
        }
```

#### 3. 用户提示

```python
def print_test_result(result):
    """打印测试结果"""
    print("=" * 60)
    print("API 连接测试")
    print("=" * 60)
    
    if result.get("supported") == False:
        print("⚠️  当前 API 不支持 OpenAI 标准协议的模型列表接口")
        print("    将跳过模型验证，直接测试对话功能")
        print()
    
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
            print(f"    可用模型: {', '.join(result['available_models'][:5])}")
    
    print("=" * 60)
```


## 后果

### 正面影响

1. **用户体验提升**
   - 配置错误能立即发现
   - 清晰的错误提示
   - 提供可用模型列表（OpenAI 协议）

2. **降低支持成本**
   - 用户自助排查问题
   - 减少配置错误导致的咨询

3. **兼容性好**
   - 支持 OpenAI 协议（优先）
   - 支持非标准协议（降级）
   - 适用于各种 API 提供商

4. **成本低**
   - 模型验证不消耗对话 token
   - 对话测试只消耗 < 10 tokens
   - 总成本可忽略

5. **速度快**
   - 总耗时 < 5 秒
   - 用户等待时间短

### 负面影响

1. **额外请求**
   - 需要 1-2 次额外请求
   - 但耗时和成本都很低

2. **代码复杂度**
   - 需要处理降级逻辑
   - 需要处理各种异常

3. **维护成本**
   - 需要适配不同 API 的返回格式
   - 需要更新错误提示

### 技术债务

1. 需要测试各种 API 提供商的兼容性
2. 需要处理更多边缘情况
3. 需要文档说明使用方法

## 使用示例

### 示例 1: OpenAI 兼容 API

```python
from main import APIModelAgent

# 创建 Agent
agent = APIModelAgent()
```

# 测试连接
result = agent.test_connection()

# 输出：
# ============================================================
# API 连接测试
# ============================================================
# ✅ 模型 'Doubao-Seed-2.0-pro' 可用
# ✅ API 连接测试成功
#     模型: Doubao-Seed-2.0-pro
#     回复预览: Hi!
#     Token 消耗: 8
# ============================================================
```

### 示例 2: 非 OpenAI 协议

```python
# 测试连接
result = agent.test_connection()

# 输出：
# ============================================================
# API 连接测试
# ============================================================
# ⚠️  当前 API 不支持 OpenAI 标准协议的模型列表接口
#     将跳过模型验证，直接测试对话功能
#
# ✅ API 连接测试成功
#     模型: custom-model
#     回复预览: Hello!
#     Token 消耗: 未知
# ============================================================
```

### 示例 3: 配置错误

```python
# 模型名错误
result = agent.test_connection()

# 输出：
# ============================================================
# API 连接测试
# ============================================================
# ❌ 模型 'gpt-4-turbo' 不在可用列表中
#     建议: 可用模型: gpt-4, gpt-3.5-turbo, gpt-4o
# ============================================================
```

## 验证标准

- ✅ 支持 OpenAI 协议的 API 能正确验证模型
- ✅ 不支持 OpenAI 协议的 API 能降级到最小化测试
- ✅ 配置错误能提供清晰的错误提示
- ✅ 总耗时 < 5 秒
- ✅ Token 消耗 < 10
- ✅ 各种异常都能正确处理

## 参考资料

### 业界实践

1. **Cursor**
   - 使用最小化测试
   - 不验证模型列表

2. **ChatGPT Web UI / Open WebUI**
   - 先获取模型列表
   - 再测试对话

3. **LangChain**
   - 直接调用，捕获异常
   - 不做预先验证

4. **Dify / FastGPT**
   - 分级测试
   - 详细的诊断信息

### OpenAI API 文档

- [List models](https://platform.openai.com/docs/api-reference/models/list)
- [Create chat completion](https://platform.openai.com/docs/api-reference/chat/create)

### 项目内部文档

- [ADR-001: OpenAI 协议兼容](./001-openai-protocol.md)
- [ADR-004: 跨平台编码兼容性](./004-cross-platform-encoding.md)
- [上下文管理策略](../context-management.md)

## 更新历史

- 2026-03-21: 初始版本，采用方案 1 + 方案 3 组合

---

**注意**：本方案已在兼容 OpenAI 协议的 API 测试通过。对于其他 API 提供商，如果不支持 `/models` 接口，会自动降级到最小化测试。
