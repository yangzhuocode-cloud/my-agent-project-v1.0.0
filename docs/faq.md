# 常见问题

本文档收集了使用过程中的常见问题和解决方案。

## 安装和配置

### Q: 如何获取火山方舟 API Key？

A: 
1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 注册并登录账号
3. 创建应用或选择现有应用
4. 在 API 管理页面获取 API Key

### Q: 依赖安装失败怎么办？

A: 尝试以下方法：
```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# 或升级 pip
pip install --upgrade pip
pip install requests
```

## API 调用问题

### Q: API 调用失败，返回 401 错误

A: 检查以下几点：
1. API Key 是否正确配置
2. API Key 是否已过期
3. 是否有足够的调用额度

### Q: API 调用失败，返回 404 错误

A: 检查以下几点：
1. BASE_URL 是否正确
2. 模型名称是否与控制台一致
3. 网络连接是否正常

### Q: 回复内容被截断

A: 增加 `MAX_TOKENS` 参数：
```python
MAX_TOKENS = 3000  # 或更大的值
```

### Q: 回复速度很慢

A: 尝试以下优化：
1. 减少 `MAX_TOKENS` 值
2. 减少 `CONTEXT_MAX_LENGTH` 值
3. 检查网络连接质量

## 对话问题

### Q: Agent 忘记了之前的对话内容

A: 可能原因：
1. 对话轮数超过 `CONTEXT_MAX_LENGTH`（默认 10 轮）
2. 程序重启导致上下文丢失

解决方法：
- 增加 `CONTEXT_MAX_LENGTH` 值
- 实现上下文持久化存储

### Q: Agent 回复不够准确

A: 调整以下参数：
1. 降低 `TEMPERATURE`（如 0.3-0.5）提高确定性
2. 优化 `SYSTEM_PROMPT` 提供更明确的角色定位
3. 在提问时提供更多上下文信息

### Q: Agent 回复太保守/太随机

A: 调整 `TEMPERATURE` 参数：
- 太保守：增加到 0.7-0.9
- 太随机：降低到 0.3-0.5

## 开发问题

### Q: 如何添加新的 Agent？

A: 参考 [开发规范](./development-guide.md) 中的"新增 Agent 流程"。

### Q: 如何实现上下文持久化？

A: 可以将 `self.context` 保存到文件或数据库：
```python
import json

# 保存上下文
def save_context(self):
    with open('context.json', 'w', encoding='utf-8') as f:
        json.dump(self.context, f, ensure_ascii=False)

# 加载上下文
def load_context(self):
    with open('context.json', 'r', encoding='utf-8') as f:
        self.context = json.load(f)
```

### Q: 如何支持流式输出？

A: 修改配置并处理流式响应：
```python
STREAM = True

# 在 API 调用中处理流式响应
for chunk in response.iter_lines():
    # 处理每个数据块
    pass
```

## 其他问题

### Q: 项目文档在哪里？

A: 所有文档位于 `docs/` 目录：
- [快速开始](./quick-start.md)
- [配置说明](./configuration.md)
- [开发规范](./development-guide.md)

### Q: 如何贡献代码？

A: 
1. Fork 项目
2. 创建功能分支
3. 提交代码（遵循提交规范）
4. 创建 Pull Request

### Q: 遇到其他问题怎么办？

A: 
1. 查看错误日志和响应内容
2. 检查配置是否正确
3. 查阅火山方舟官方文档
4. 在项目中提交 Issue

## 错误代码参考

| 错误码 | 说明 | 解决方法 |
|--------|------|----------|
| 401 | 认证失败 | 检查 API Key |
| 404 | 资源不存在 | 检查 URL 和模型名称 |
| 429 | 请求过多 | 降低请求频率 |
| 500 | 服务器错误 | 稍后重试或联系技术支持 |
