# Git 提交信息

## 提交类型：docs

## 提交范围：structure

## 完整提交信息

```
docs(structure): 深化文档架构重构，实施单一数据源和 ADR 体系

在上次"人机分离"文档重构基础上，进一步细化文档结构，实施单一数据源原则，新增架构决策记录(ADR)体系。

本次重构延续上次的"人机分离"理念，进一步优化：
1. 文档分类更加细化和合理
2. 实施项目结构文档单一数据源原则
3. 建立 ADR 体系记录架构演进历史
4. 优化文档间的引用关系和信息组织

主要变更：
- 新增 docs/understanding/adr/ 目录，包含 5 个架构决策记录
- 新增 docs/issues/README.md 开发过程记录指南
- 新增 prompts/METADATA-SPEC.md Prompt 元数据规范（从 docs/reference/ 迁移）
- 移除 docs/reference/ 目录下的重复文档（faq.md, issues-guide.md, prompt-metadata-spec.md）
- 清理 exports/my-first-agent/ 目录下的过期导出文件
- 更新 README.md、docs/INDEX.md 等文档，移除重复的项目结构树
- 更新 .kiro/instructions/workflow.md，添加项目结构引用规范
- 优化 docs/understanding/ 下的架构文档，增强文档间的关联性

影响范围：
- 18 个文件变更（227 行新增，1239 行删除）
- 文档结构更清晰，维护成本显著降低
- 贯彻"单一数据源"设计原则

重构历程：
- 第一阶段（上次提交）：人机分离，创建 understanding/guides/development/reference 分类
- 第二阶段（本次提交）：单一数据源，建立 ADR 体系，优化文档引用关系

相关 ADR：
- ADR 0004: 文档结构重构（人机分离）
- ADR 0005: 项目结构文档单一数据源
```

---

## 重构历程回顾

### 第一阶段：人机分离（上次提交 9a7e746）

**核心理念**：区分人类文档和 AI 指令

**主要工作**：
- 创建新的文档分类目录（understanding/guides/development/reference）
- 拆分 development-guide.md 为多个专注文档
- 创建 .kiro/instructions/ 目录存放 AI 指令
- 简化 .kiro/steering/main.md，通过引用组织
- 移动现有文档到对应分类

**成果**：
- 21 个文件变更（1591 行新增，651 行删除）
- 人类文档和 AI 指令完全分离
- 文档按功能清晰分类

### 第二阶段：单一数据源 + ADR 体系（本次提交）

**核心理念**：避免信息重复，建立架构决策追溯机制

**主要工作**：
- 建立 ADR（架构决策记录）体系
- 实施项目结构文档单一数据源原则
- 移除多处重复的项目结构树形图
- 优化文档引用关系
- 清理过期和重复文件

**成果**：
- 18 个文件变更（227 行新增，1239 行删除）
- 文档维护成本显著降低
- 架构演进历史可追溯

### 重构对比

| 维度 | 重构前 | 第一阶段 | 第二阶段（本次） |
|------|--------|---------|----------------|
| 文档分类 | 扁平化 | 按功能分类 | 进一步细化 |
| 人机分离 | 混合 | 已分离 | 持续优化 |
| 信息重复 | 严重 | 部分改善 | 完全消除 |
| 架构追溯 | 无 | 无 | 建立 ADR 体系 |
| 维护成本 | 高 | 中 | 低 |

---

## 变更详情

### 新增文件

#### 架构决策记录 (ADR)
- `docs/understanding/adr/README.md` - ADR 索引和说明
- `docs/understanding/adr/0001-虚拟路径引用机制.md`
- `docs/understanding/adr/0002-Prompts分离架构.md`
- `docs/understanding/adr/0003-Agent导出机制.md`
- `docs/understanding/adr/0004-文档结构重构.md`
- `docs/understanding/adr/0005-项目结构文档单一数据源.md`

#### 指南文档
- `docs/issues/README.md` - 开发过程记录指南
- `prompts/METADATA-SPEC.md` - Prompt 元数据规范（从 docs/reference/ 迁移）

### 删除文件

#### 重复的参考文档
- `docs/reference/faq.md` - 常见问题（内容已整合到其他文档）
- `docs/reference/issues-guide.md` - 开发记录指南（迁移到 docs/issues/README.md）
- `docs/reference/prompt-metadata-spec.md` - Prompt 元数据规范（迁移到 prompts/METADATA-SPEC.md）

#### 过期的导出文件
- `exports/my-first-agent/config.json`
- `exports/my-first-agent/main.py`
- `exports/my-first-agent/prompts/agent.md`
- `exports/my-first-agent/prompts/git_commit_angular_001.md`
- `exports/my-first-agent/references/README.md`

### 修改文件

#### 核心文档
- `README.md` - 移除项目结构树，改为引用链接
- `docs/INDEX.md` - 移除文档结构树，优化文档分类说明

#### 理解文档
- `docs/understanding/architecture.md` - 新增架构决策说明章节
- `docs/understanding/design-philosophy.md` - 移除重复的架构决策内容，引用 ADR
- `docs/understanding/project-structure.md` - 优化目录说明和引用链接

#### 指南文档
- `docs/guides/prompts-guide.md` - 移除 Prompts 目录树，改为引用

#### 开发记录
- `docs/issues/notes/user/20260319_文档重构总结.md` - 更新文档重构总结

#### AI 指令
- `.kiro/instructions/coding-standards.md` - 优化代码规范说明
- `.kiro/instructions/workflow.md` - 新增项目结构引用规范

#### 参考资源
- `references/README.md` - 优化目录结构说明

---

## 设计原则

本次重构延续并深化了以下设计原则：

### 1. 人机分离（第一阶段确立）

**原则**：人类文档和 AI 指令分开管理

**实施**：
- `docs/` - 人类文档（理解性、指导性）
  - understanding/ - 为什么这样设计
  - guides/ - 怎么使用
  - development/ - 如何贡献
  - issues/ - 开发过程记录
- `.kiro/instructions/` - AI 指令（执行性、规范性）
  - boundaries.md - 开发边界
  - workflow.md - 工作流程
  - coding-standards.md - 代码规范

**本次优化**：
- 进一步细化 issues/ 目录的使用规范
- 优化 AI 指令中的项目结构引用规范

### 2. 单一数据源（本次重点）

**原则**：同一信息只在一处维护，其他地方通过引用

**实施**：
- `docs/understanding/project-structure.md` 是项目结构的唯一维护点
- `prompts/METADATA-SPEC.md` 是 Prompt 元数据规范的唯一维护点
- 其他文档通过引用链接指向这些数据源
- 禁止在多个文档中复制粘贴项目结构树形图

**影响**：
- 项目结构变更只需更新一个文件
- 避免文档信息不一致
- 降低维护成本

### 3. 架构决策可追溯（本次新增）

**原则**：重要的架构决策应该被记录和追溯

**实施**：
- 建立 `docs/understanding/adr/` 目录
- 使用 ADR（Architecture Decision Record）格式
- 记录决策背景、方案对比、最终选择和影响
- 每个 ADR 有唯一编号和状态

**已记录的 ADR**：
- ADR 0001: 虚拟路径引用机制
- ADR 0002: Prompts 分离架构
- ADR 0003: Agent 导出机制
- ADR 0004: 文档结构重构（人机分离）
- ADR 0005: 项目结构文档单一数据源

### 4. 文档分层（持续优化）

**原则**：不同类型的文档有不同的职责和目标读者

**分层结构**：
```
docs/
├── understanding/     # 理解层 - 设计理念、架构、ADR
├── guides/           # 指导层 - 使用方法、配置、教程
├── development/      # 开发层 - 贡献指南、工作流程
└── issues/           # 记录层 - 问题、笔记、想法
```

**本次优化**：
- 新增 issues/README.md 规范开发记录
- 优化 understanding/ 下的文档关联
- 移除 reference/ 目录，内容整合到其他分类

---

## 设计原则

本次变更贯彻以下设计原则：

1. **单一数据源 (Single Source of Truth)**
   - `docs/understanding/project-structure.md` 是项目结构的唯一维护点
   - 其他文档通过引用链接指向该文档
   - 避免在多处维护相同信息

2. **文档分层**
   - 理解文档 (understanding/) - 设计理念和架构
   - 指南文档 (guides/) - 使用方法和教程
   - 开发文档 (development/) - 贡献和工作流程
   - 记录文档 (issues/) - 开发过程记录

3. **架构决策可追溯**
   - 通过 ADR 记录重要的架构决策
   - 记录决策背景、方案对比、最终选择和影响
   - 便于理解项目演进历史

---

## 影响评估

### 正面影响
- ✅ 降低文档维护成本（项目结构变更只需更新一处）
- ✅ 避免文档信息不一致
- ✅ 提高文档质量和可维护性
- ✅ 理念与实践保持一致
- ✅ 新增 ADR 体系，便于追溯架构演进

### 维护建议
- 项目结构变更时，只需更新 `docs/understanding/project-structure.md`
- 新增文档时，遵循 `.kiro/instructions/workflow.md` 中的引用规范
- 重要架构决策应记录到 `docs/understanding/adr/` 目录

---

## 统计数据

- 文件变更：18 个文件
- 新增行数：227 行
- 删除行数：1239 行
- 净减少：1012 行
- 新增文件：8 个
- 删除文件：10 个

---

## 相关文档

- [ADR 0005: 项目结构文档单一数据源](./docs/understanding/adr/0005-项目结构文档单一数据源.md)
- [项目结构说明](./docs/understanding/project-structure.md)
- [设计理念](./docs/understanding/design-philosophy.md)
- [架构设计](./docs/understanding/architecture.md)
