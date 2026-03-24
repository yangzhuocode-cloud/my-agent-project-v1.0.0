# Python 字典（Dictionary）数据结构详解

> 📅 创建时间：2026-03-20  
> 🎯 目标读者：从 Java 转 Python 的开发者  
> 📝 学习目标：理解 Python 字典的本质和使用方法

## 核心理解

### 什么是字典？

**字典就是 KV 键值对（Key-Value Pairs）**，可以通过 key 快速找到对应的 value（对象）。

- **Key（键）**：用于查找的标识符，必须是不可变类型（字符串、数字、元组）
- **Value（值）**：可以是任何类型的数据，包括：
  - 普通类型：字符串、数字、布尔值
  - 复杂类型：列表、字典、对象
  - **重要**：值可以是另一个字典（嵌套结构）

### 类比理解

```
字典 = 一本真正的字典
├── Key（词条）：通过词条查找
└── Value（解释）：词条对应的内容

例如：
"apple" → "苹果，一种水果"
"banana" → "香蕉，热带水果"
```

## Python 字典 vs Java 对比

| 特性 | Python 字典 | Java HashMap/Map |
|------|------------|------------------|
| 定义方式 | `{}` 或 `dict()` | `new HashMap<>()` |
| 类型约束 | 无（动态类型） | 有（需要指定泛型） |
| Key 类型 | 不可变类型 | 实现 hashCode/equals |
| Value 类型 | 任意类型 | 需要指定泛型 |
| 访问方式 | `dict[key]` | `map.get(key)` |
| 添加元素 | `dict[key] = value` | `map.put(key, value)` |
| 灵活性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 类型安全 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 基础语法

### 1. 创建字典

```python
# 方式1：使用花括号 {}
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

# 方式2：使用 dict() 构造函数
person = dict(name="张三", age=25, city="北京")

# 方式3：空字典
empty_dict = {}
empty_dict2 = dict()
```

**Java 对比**：
```java
// Java
Map<String, Object> person = new HashMap<>();
person.put("name", "张三");
person.put("age", 25);
person.put("city", "北京");
```

### 2. 访问元素

```python
person = {"name": "张三", "age": 25}

# 方式1：使用 [] 访问（推荐）
print(person["name"])  # 输出: 张三

# 方式2：使用 get() 方法（更安全）
print(person.get("name"))      # 输出: 张三
print(person.get("gender"))    # 输出: None（不存在时返回 None）
print(person.get("gender", "未知"))  # 输出: 未知（提供默认值）
```

**Java 对比**：
```java
// Java
String name = (String) person.get("name");  // 需要类型转换
String gender = (String) person.getOrDefault("gender", "未知");
```

### 3. 添加/修改元素

```python
person = {"name": "张三"}

# 添加新键值对
person["age"] = 25
person["city"] = "北京"

# 修改已有键值对
person["age"] = 26

print(person)
# 输出: {'name': '张三', 'age': 26, 'city': '北京'}
```

**Java 对比**：
```java
// Java
person.put("age", 25);      // 添加
person.put("age", 26);      // 修改（覆盖）
```

### 4. 删除元素

```python
person = {"name": "张三", "age": 25, "city": "北京"}

# 方式1：使用 del
del person["city"]

# 方式2：使用 pop()（返回被删除的值）
age = person.pop("age")
print(age)  # 输出: 25

# 方式3：使用 popitem()（删除最后一个键值对）
item = person.popitem()
print(item)  # 输出: ('name', '张三')
```

**Java 对比**：
```java
// Java
person.remove("city");
Object age = person.remove("age");
```

## 值的类型多样性

### 1. 普通类型作为值

```python
data = {
    "name": "张三",        # 字符串
    "age": 25,            # 整数
    "height": 1.75,       # 浮点数
    "is_student": True,   # 布尔值
    "score": None         # 空值
}

print(data["name"])        # 输出: 张三
print(data["age"])         # 输出: 25
print(data["is_student"])  # 输出: True
```

**Java 对比**：
```java
// Java（需要使用包装类）
Map<String, Object> data = new HashMap<>();
data.put("name", "张三");           // String
data.put("age", 25);                // Integer（自动装箱）
data.put("height", 1.75);           // Double
data.put("is_student", true);       // Boolean
data.put("score", null);            // null
```

### 2. 列表作为值

```python
student = {
    "name": "张三",
    "hobbies": ["游泳", "跑步", "阅读"],  # 列表作为值
    "scores": [85, 90, 88]
}

# 访问列表
print(student["hobbies"])      # 输出: ['游泳', '跑步', '阅读']
print(student["hobbies"][0])   # 输出: 游泳

# 修改列表
student["hobbies"].append("绘画")
print(student["hobbies"])      # 输出: ['游泳', '跑步', '阅读', '绘画']
```

**Java 对比**：
```java
// Java
Map<String, Object> student = new HashMap<>();
List<String> hobbies = new ArrayList<>();
hobbies.add("游泳");
hobbies.add("跑步");
student.put("hobbies", hobbies);

// 访问
List<String> h = (List<String>) student.get("hobbies");
System.out.println(h.get(0));  // 游泳
```

### 3. 字典作为值（嵌套字典）⭐ 重点

```python
person = {
    "name": "张三",
    "age": 25,
    "address": {              # 字典作为值（嵌套）
        "city": "北京",
        "district": "朝阳区",
        "street": "建国路"
    },
    "contact": {              # 另一个嵌套字典
        "phone": "13800138000",
        "email": "zhangsan@example.com"
    }
}

# 访问嵌套字典
print(person["address"])              # 输出: {'city': '北京', ...}
print(person["address"]["city"])      # 输出: 北京
print(person["contact"]["phone"])     # 输出: 13800138000

# 修改嵌套字典
person["address"]["city"] = "上海"
print(person["address"]["city"])      # 输出: 上海
```

**Java 对比**：
```java
// Java
Map<String, Object> person = new HashMap<>();
person.put("name", "张三");

// 嵌套 Map
Map<String, String> address = new HashMap<>();
address.put("city", "北京");
address.put("district", "朝阳区");
person.put("address", address);

// 访问（需要类型转换）
Map<String, String> addr = (Map<String, String>) person.get("address");
System.out.println(addr.get("city"));  // 北京
```

## 项目实战示例

### 示例 1：My First Agent 的上下文结构

这是我们项目中实际使用的字典结构：

```python
# 初始化
self.context = {
    # 第1层：永久保留
    "permanent": {
        "system": "你是一个专业的AI助手",
        "task": ""
    },
    # 第2层：重要信息
    "important": {
        "errors": [],
        "milestones": []
    },
    # 第3层：最近对话
    "recent": []
}
```

**结构分析**：
```
字典 (self.context)
├── "permanent" → 字典
│   ├── "system" → 字符串
│   └── "task" → 字符串
├── "important" → 字典
│   ├── "errors" → 列表
│   └── "milestones" → 列表
└── "recent" → 列表
```

### 示例 2：添加消息到 recent 列表

```python
# 添加第1条消息（字典）
self.context["recent"].append({
    "role": "user",
    "content": "请创建 main.py",
    "priority": 5,
    "timestamp": 1234567890
})

# 添加第2条消息（字典）
self.context["recent"].append({
    "role": "assistant",
    "content": "成功创建了 main.py 文件",
    "priority": 8,
    "timestamp": 1234567891
})

# 现在 recent 包含 2 个字典
print(len(self.context["recent"]))  # 输出: 2

# 访问第1条消息的内容
print(self.context["recent"][0]["content"])
# 输出: 请创建 main.py
```

**实际数据示例**：
```python
{
    "permanent": {
        "system": "你是一个专业的AI助手",
        "task": "创建一个计算器程序"
    },
    "important": {
        "errors": [
            {
                "signature": "NameError:x",
                "message": "NameError: name 'x' is not defined",
                "timestamp": 1234567890,
                "count": 1
            }
        ],
        "milestones": [
            "成功创建 main.py",
            "修复了语法错误"
        ]
    },
    "recent": [
        {
            "role": "user",
            "content": "请创建 main.py",
            "priority": 5,
            "timestamp": 1234567890
        },
        {
            "role": "assistant",
            "content": "成功创建了 main.py 文件",
            "priority": 8,
            "timestamp": 1234567891
        }
    ]
}
```

### 示例 3：访问和修改

```python
# 访问永久层的 system
system_prompt = self.context["permanent"]["system"]
print(system_prompt)  # 输出: 你是一个专业的AI助手

# 修改任务
self.context["permanent"]["task"] = "创建一个计算器程序"

# 添加里程碑
self.context["important"]["milestones"].append("成功创建 main.py")

# 访问最近的消息
recent_messages = self.context["recent"]
for msg in recent_messages:
    print(f"{msg['role']}: {msg['content']}")
# 输出:
# user: 请创建 main.py
# assistant: 成功创建了 main.py 文件

# 访问第1条消息的优先级
priority = self.context["recent"][0]["priority"]
print(priority)  # 输出: 5
```

## 常用操作

### 1. 遍历字典

```python
person = {"name": "张三", "age": 25, "city": "北京"}

# 遍历键
for key in person:
    print(key)
# 输出: name, age, city

# 遍历值
for value in person.values():
    print(value)
# 输出: 张三, 25, 北京

# 遍历键值对
for key, value in person.items():
    print(f"{key}: {value}")
# 输出:
# name: 张三
# age: 25
# city: 北京
```

**Java 对比**：
```java
// Java
for (Map.Entry<String, Object> entry : person.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

### 2. 检查键是否存在

```python
person = {"name": "张三", "age": 25}

# 方式1：使用 in
if "name" in person:
    print("name 存在")

if "gender" not in person:
    print("gender 不存在")

# 方式2：使用 get()
name = person.get("name")
if name is not None:
    print(f"name = {name}")
```

**Java 对比**：
```java
// Java
if (person.containsKey("name")) {
    System.out.println("name 存在");
}
```

### 3. 合并字典

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# 方式1：使用 update()
dict1.update(dict2)
print(dict1)  # 输出: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 方式2：使用 ** 解包（Python 3.5+）
dict3 = {**dict1, **dict2}
print(dict3)  # 输出: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 方式3：使用 | 运算符（Python 3.9+）
dict4 = dict1 | dict2
print(dict4)  # 输出: {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

**Java 对比**：
```java
// Java
dict1.putAll(dict2);
```

### 4. 复制字典

```python
original = {"name": "张三", "age": 25}

# 浅拷贝
copy1 = original.copy()
copy2 = dict(original)

# 深拷贝（嵌套字典需要）
import copy
deep_copy = copy.deepcopy(original)
```

**Java 对比**：
```java
// Java
Map<String, Object> copy = new HashMap<>(original);
```

## 高级技巧

### 1. 字典推导式

```python
# 创建字典
squares = {x: x**2 for x in range(5)}
print(squares)  # 输出: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 过滤字典
person = {"name": "张三", "age": 25, "city": "北京"}
filtered = {k: v for k, v in person.items() if k != "age"}
print(filtered)  # 输出: {'name': '张三', 'city': '北京'}
```

### 2. 默认值字典

```python
from collections import defaultdict

# 自动创建默认值
counts = defaultdict(int)  # 默认值为 0
counts["apple"] += 1
counts["banana"] += 1
print(counts)  # 输出: {'apple': 1, 'banana': 1}
```

### 3. 有序字典

```python
from collections import OrderedDict

# 保持插入顺序（Python 3.7+ 普通字典也保持顺序）
ordered = OrderedDict()
ordered["a"] = 1
ordered["b"] = 2
ordered["c"] = 3
```

## 常见陷阱

### 1. 键必须是不可变类型

```python
# ✅ 正确：字符串、数字、元组可以作为键
dict1 = {"name": "张三"}
dict2 = {1: "one"}
dict3 = {(1, 2): "tuple"}

# ❌ 错误：列表不能作为键
# dict4 = {[1, 2]: "list"}  # TypeError
```

### 2. 访问不存在的键

```python
person = {"name": "张三"}

# ❌ 错误：直接访问不存在的键会报错
# print(person["age"])  # KeyError

# ✅ 正确：使用 get() 方法
print(person.get("age"))         # 输出: None
print(person.get("age", 0))      # 输出: 0（默认值）
```

### 3. 字典是可变的

```python
def modify_dict(d):
    d["new_key"] = "new_value"

original = {"name": "张三"}
modify_dict(original)
print(original)  # 输出: {'name': '张三', 'new_key': 'new_value'}
# 注意：字典被修改了！
```

## 性能特点

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 访问元素 | O(1) | 平均情况 |
| 添加元素 | O(1) | 平均情况 |
| 删除元素 | O(1) | 平均情况 |
| 查找键 | O(1) | 平均情况 |
| 遍历 | O(n) | n 为元素个数 |

## 总结

### Python 字典的核心特点

1. **KV 键值对结构**：通过 key 快速查找 value
2. **值类型灵活**：可以是任何类型，包括嵌套字典
3. **动态类型**：不需要预先声明类型
4. **高性能**：O(1) 的查找、插入、删除
5. **可变对象**：可以动态添加、修改、删除键值对

### 与 Java 的主要区别

| 特性 | Python | Java |
|------|--------|------|
| 类型声明 | 不需要 | 需要泛型 |
| 语法 | 简洁 `{}` | 冗长 `new HashMap<>()` |
| 灵活性 | 高 | 中 |
| 类型安全 | 运行时检查 | 编译时检查 |
| 嵌套 | 自然支持 | 需要类型转换 |

### 学习建议

1. 多练习字典的基本操作（创建、访问、修改）
2. 理解嵌套字典的结构和访问方式
3. 熟悉字典与列表的组合使用
4. 对比 Java 的 Map，理解异同
5. 在实际项目中多使用，加深理解

## 参考资料

- [Python 官方文档 - 字典](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Real Python - Dictionaries](https://realpython.com/python-dicts/)
- 项目代码：`worktrees/my-first-agent/agents/my first agent/main.py`
