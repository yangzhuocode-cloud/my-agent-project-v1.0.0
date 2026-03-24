# Python 切片（Slicing）语法详解

> 📅 创建时间：2026-03-20  
> 🎯 目标读者：从 Java 转 Python 的开发者  
> 📝 学习目标：掌握 Python 切片语法的使用方法

## 什么是切片？

**切片（Slicing）** 是 Python 中用于获取序列（列表、字符串、元组等）的子集的强大语法。

### 核心理解

切片就像**切蛋糕**：
- 你可以指定从哪里开始切（起始位置）
- 切到哪里结束（结束位置）
- 每隔多少切一刀（步长）

```python
# 一个列表就像一块蛋糕
cake = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 切片：取一部分
piece = cake[2:7]  # 从索引 2 到 7（不含 7）
print(piece)  # [2, 3, 4, 5, 6]
```

## 基本语法

```python
序列[start:end:step]
```

- **start**：起始索引（包含），默认为 0
- **end**：结束索引（不包含），默认为序列长度
- **step**：步长，默认为 1

### 重要规则

1. **起始索引包含，结束索引不包含**（左闭右开）
2. **索引可以是负数**（从后往前数）
3. **省略参数使用默认值**

## 索引系统

### 正数索引（从前往后）

```python
items = ["a", "b", "c", "d", "e"]
#        0    1    2    3    4     # 正数索引

print(items[0])   # 输出: a（第1个）
print(items[2])   # 输出: c（第3个）
print(items[4])   # 输出: e（第5个）
```

### 负数索引（从后往前）

```python
items = ["a", "b", "c", "d", "e"]
#       -5   -4   -3   -2   -1     # 负数索引

print(items[-1])  # 输出: e（最后1个）
print(items[-2])  # 输出: d（倒数第2个）
print(items[-5])  # 输出: a（倒数第5个，即第1个）
```

### 双重索引对照表

```python
items = ["a", "b", "c", "d", "e"]

# 索引对照
正数索引:  0    1    2    3    4
元素:     "a"  "b"  "c"  "d"  "e"
负数索引: -5   -4   -3   -2   -1
```

## 基础切片操作

### 1. 取前 N 个元素 `[:n]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 取前 5 个
first_5 = items[:5]
print(first_5)  # [0, 1, 2, 3, 4]

# 解释：
# 省略 start，默认从 0 开始
# end = 5，到索引 5（不包含）
```

**图示**：
```
原列表：[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    ↑
                   索引5（不包含）
取出：  [0, 1, 2, 3, 4]
```

### 2. 取后 N 个元素 `[-n:]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 取最后 5 个
last_5 = items[-5:]
print(last_5)  # [5, 6, 7, 8, 9]

# 解释：
# start = -5，从倒数第5个开始
# 省略 end，默认到列表末尾
```

**图示**：
```
原列表：[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    ↑
                   -5 开始
取出：              [5, 6, 7, 8, 9]
```

### 3. 取中间部分 `[n:m]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 取索引 2 到 7 的元素
middle = items[2:7]
print(middle)  # [2, 3, 4, 5, 6]

# 解释：
# start = 2，从索引 2 开始（包含）
# end = 7，到索引 7（不包含）
```

**图示**：
```
原列表：[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            ↑           ↑
           索引2       索引7（不包含）
取出：      [2, 3, 4, 5, 6]
```

### 4. 从某位置到末尾 `[n:]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 从索引 3 到末尾
from_3 = items[3:]
print(from_3)  # [3, 4, 5, 6, 7, 8, 9]

# 解释：
# start = 3，从索引 3 开始
# 省略 end，默认到列表末尾
```

### 5. 除了后 N 个 `[:-n]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 除了最后 3 个
except_last_3 = items[:-3]
print(except_last_3)  # [0, 1, 2, 3, 4, 5, 6]

# 解释：
# 省略 start，默认从 0 开始
# end = -3，到倒数第3个（不包含）
```

**图示**：
```
原列表：[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                          ↑
                         -3（不包含）
取出：  [0, 1, 2, 3, 4, 5, 6]
```

### 6. 复制整个序列 `[:]`

```python
items = [0, 1, 2, 3, 4, 5]

# 复制整个列表（浅拷贝）
copy = items[:]
print(copy)  # [0, 1, 2, 3, 4, 5]

# 验证是不同的对象
print(copy is items)  # False
```

## 项目实战示例

### 示例 1：智能裁剪上下文（来自 main.py）

```python
def _smart_trim(self):
    """智能裁剪上下文"""
    recent_keep_count = 6  # 保留最近 6 条消息
    
    # 假设有 10 条消息
    self.context["recent"] = [
        "消息0", "消息1", "消息2", "消息3", "消息4",
        "消息5", "消息6", "消息7", "消息8", "消息9"
    ]
    
    # 1. 取最后 6 条（必须保留）
    must_keep = self.context["recent"][-6:]
    print(must_keep)
    # 输出: ['消息4', '消息5', '消息6', '消息7', '消息8', '消息9']
    
    # 2. 取前面的（可能被裁剪）
    older = self.context["recent"][:-6]
    print(older)
    # 输出: ['消息0', '消息1', '消息2', '消息3']
    
    # 3. 验证：两部分加起来等于原列表
    print(len(older) + len(must_keep))  # 输出: 10
```

**图示**：
```
原列表：["消息0", "消息1", "消息2", "消息3", "消息4", "消息5", "消息6", "消息7", "消息8", "消息9"]
                                            ↑
                                           -6 分界点
older:  ["消息0", "消息1", "消息2", "消息3"]
must_keep:                                  ["消息4", "消息5", "消息6", "消息7", "消息8", "消息9"]
```

### 示例 2：分页显示

```python
def paginate(items, page_size=5):
    """分页显示列表"""
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    for page in range(total_pages):
        start = page * page_size
        end = start + page_size
        page_items = items[start:end]
        print(f"第 {page + 1} 页: {page_items}")

# 使用
data = list(range(23))  # [0, 1, 2, ..., 22]
paginate(data, page_size=5)

# 输出:
# 第 1 页: [0, 1, 2, 3, 4]
# 第 2 页: [5, 6, 7, 8, 9]
# 第 3 页: [10, 11, 12, 13, 14]
# 第 4 页: [15, 16, 17, 18, 19]
# 第 5 页: [20, 21, 22]
```

### 示例 3：滑动窗口

```python
def sliding_window(items, window_size=3):
    """滑动窗口"""
    for i in range(len(items) - window_size + 1):
        window = items[i:i + window_size]
        print(f"窗口 {i}: {window}")

# 使用
data = [1, 2, 3, 4, 5, 6, 7]
sliding_window(data, window_size=3)

# 输出:
# 窗口 0: [1, 2, 3]
# 窗口 1: [2, 3, 4]
# 窗口 2: [3, 4, 5]
# 窗口 3: [4, 5, 6]
# 窗口 4: [5, 6, 7]
```

## 带步长的切片

### 1. 每隔 N 个取一个 `[::n]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 每隔一个取一个（取偶数索引）
even_indices = items[::2]
print(even_indices)  # [0, 2, 4, 6, 8]

# 每隔两个取一个
every_third = items[::3]
print(every_third)  # [0, 3, 6, 9]
```

### 2. 从指定位置开始，每隔 N 个取一个 `[start::n]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 从索引 1 开始，每隔一个取一个（取奇数索引）
odd_indices = items[1::2]
print(odd_indices)  # [1, 3, 5, 7, 9]

# 从索引 2 开始，每隔两个取一个
from_2_every_3 = items[2::3]
print(from_2_every_3)  # [2, 5, 8]
```

### 3. 反转序列 `[::-1]`

```python
items = [0, 1, 2, 3, 4, 5]

# 反转列表
reversed_items = items[::-1]
print(reversed_items)  # [5, 4, 3, 2, 1, 0]

# 字符串反转
text = "hello"
reversed_text = text[::-1]
print(reversed_text)  # "olleh"
```

### 4. 反向每隔 N 个取一个 `[::-n]`

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 反向每隔一个取一个
reverse_every_2 = items[::-2]
print(reverse_every_2)  # [9, 7, 5, 3, 1]

# 反向每隔两个取一个
reverse_every_3 = items[::-3]
print(reverse_every_3)  # [9, 6, 3, 0]
```

## 字符串切片

切片不仅适用于列表，也适用于字符串：

```python
text = "Hello, World!"

# 取前 5 个字符
print(text[:5])      # "Hello"

# 取后 6 个字符
print(text[-6:])     # "World!"

# 取中间部分
print(text[7:12])    # "World"

# 反转字符串
print(text[::-1])    # "!dlroW ,olleH"

# 每隔一个字符取一个
print(text[::2])     # "Hlo ol!"
```

## 切片赋值（修改列表）

切片不仅可以读取，还可以用于修改列表：

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 替换中间部分
items[2:5] = [20, 30, 40]
print(items)  # [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# 插入元素（空切片）
items[2:2] = [100, 200]
print(items)  # [0, 1, 100, 200, 20, 30, 40, 5, 6, 7, 8, 9]

# 删除元素
items[2:4] = []
print(items)  # [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# 清空列表
items[:] = []
print(items)  # []
```

## Java 对比

Java 没有内置的切片语法，需要使用方法：

### 列表切片

```java
// Java
List<Integer> items = Arrays.asList(0, 1, 2, 3, 4, 5, 6, 7, 8, 9);

// Python: items[:5]
List<Integer> first5 = items.subList(0, 5);
// 结果: [0, 1, 2, 3, 4]

// Python: items[-5:]
int size = items.size();
List<Integer> last5 = items.subList(size - 5, size);
// 结果: [5, 6, 7, 8, 9]

// Python: items[2:7]
List<Integer> middle = items.subList(2, 7);
// 结果: [2, 3, 4, 5, 6]

// Python: items[:-3]
List<Integer> exceptLast3 = items.subList(0, size - 3);
// 结果: [0, 1, 2, 3, 4, 5, 6]
```

### 字符串切片

```java
// Java
String text = "Hello, World!";

// Python: text[:5]
String first5 = text.substring(0, 5);
// 结果: "Hello"

// Python: text[-6:]
String last6 = text.substring(text.length() - 6);
// 结果: "World!"

// Python: text[7:12]
String middle = text.substring(7, 12);
// 结果: "World"

// Python: text[::-1]（反转）
String reversed = new StringBuilder(text).reverse().toString();
// 结果: "!dlroW ,olleH"
```

### 对比总结

| 操作 | Python | Java |
|------|--------|------|
| 取前 N 个 | `items[:n]` | `items.subList(0, n)` |
| 取后 N 个 | `items[-n:]` | `items.subList(size-n, size)` |
| 取中间 | `items[n:m]` | `items.subList(n, m)` |
| 反转 | `items[::-1]` | `Collections.reverse()` |
| 语法简洁度 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 功能强大度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 切片语法速查表

| 语法 | 说明 | 示例输入 | 示例输出 |
|------|------|---------|---------|
| `[n]` | 取单个元素 | `items[2]` | `2` |
| `[n:m]` | 从 n 到 m（不含） | `items[2:5]` | `[2, 3, 4]` |
| `[:n]` | 前 n 个 | `items[:3]` | `[0, 1, 2]` |
| `[n:]` | 从 n 到末尾 | `items[3:]` | `[3, 4, 5, ...]` |
| `[-n:]` | 最后 n 个 | `items[-3:]` | `[7, 8, 9]` |
| `[:-n]` | 除了最后 n 个 | `items[:-2]` | `[0, 1, ..., 7]` |
| `[:]` | 复制整个序列 | `items[:]` | `[0, 1, ..., 9]` |
| `[::n]` | 每隔 n 个 | `items[::2]` | `[0, 2, 4, 6, 8]` |
| `[n::m]` | 从 n 开始每隔 m 个 | `items[1::2]` | `[1, 3, 5, 7, 9]` |
| `[::-1]` | 反转 | `items[::-1]` | `[9, 8, ..., 0]` |
| `[n:m:k]` | 从 n 到 m 每隔 k 个 | `items[1:8:2]` | `[1, 3, 5, 7]` |

## 常见用例

### 1. 获取列表的前/后部分

```python
# 获取前 10 个
top_10 = items[:10]

# 获取后 10 个
bottom_10 = items[-10:]

# 获取除了第一个之外的所有
rest = items[1:]

# 获取除了最后一个之外的所有
all_but_last = items[:-1]
```

### 2. 分割列表

```python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 分成两半
mid = len(data) // 2
first_half = data[:mid]      # [1, 2, 3, 4, 5]
second_half = data[mid:]     # [6, 7, 8, 9, 10]

# 分成三部分
third = len(data) // 3
part1 = data[:third]         # [1, 2, 3]
part2 = data[third:third*2]  # [4, 5, 6]
part3 = data[third*2:]       # [7, 8, 9, 10]
```

### 3. 去除首尾元素

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 去除第一个和最后一个
middle = items[1:-1]
print(middle)  # [1, 2, 3, 4, 5, 6, 7, 8]

# 去除前两个和后两个
core = items[2:-2]
print(core)  # [2, 3, 4, 5, 6, 7]
```

### 4. 提取偶数/奇数位置的元素

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 偶数位置（索引 0, 2, 4, ...）
even_positions = items[::2]
print(even_positions)  # [0, 2, 4, 6, 8]

# 奇数位置（索引 1, 3, 5, ...）
odd_positions = items[1::2]
print(odd_positions)  # [1, 3, 5, 7, 9]
```

## 注意事项

### 1. 切片不会抛出索引错误

```python
items = [0, 1, 2, 3, 4]

# 索引超出范围会报错
# print(items[10])  # IndexError

# 但切片不会报错
print(items[10:20])  # []（返回空列表）
print(items[:100])   # [0, 1, 2, 3, 4]（返回所有元素）
```

### 2. 切片创建新对象（浅拷贝）

```python
original = [1, 2, 3, 4, 5]
sliced = original[1:4]

# 修改切片不影响原列表
sliced[0] = 100
print(original)  # [1, 2, 3, 4, 5]（未改变）
print(sliced)    # [100, 3, 4]（已改变）
```

### 3. 负数步长时，start 和 end 的含义相反

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 正向：从索引 2 到 7
print(items[2:7])     # [2, 3, 4, 5, 6]

# 反向：从索引 7 到 2（需要交换 start 和 end）
print(items[7:2:-1])  # [7, 6, 5, 4, 3]
```

## 性能考虑

- **时间复杂度**：O(k)，k 为切片长度
- **空间复杂度**：O(k)，创建新对象
- **优化建议**：
  - 避免在循环中频繁切片
  - 大数据量时考虑使用迭代器
  - 需要原地修改时使用切片赋值

## 练习题

### 练习 1：基础切片

```python
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# 1. 取前 3 个元素
# 答案: data[:3] → [10, 20, 30]

# 2. 取最后 4 个元素
# 答案: data[-4:] → [70, 80, 90, 100]

# 3. 取索引 2 到 6 的元素
# 答案: data[2:6] → [30, 40, 50, 60]

# 4. 取除了第一个和最后一个之外的所有元素
# 答案: data[1:-1] → [20, 30, 40, 50, 60, 70, 80, 90]
```

### 练习 2：步长切片

```python
numbers = list(range(20))  # [0, 1, 2, ..., 19]

# 1. 取所有偶数索引的元素
# 答案: numbers[::2] → [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 2. 反转列表
# 答案: numbers[::-1] → [19, 18, 17, ..., 1, 0]

# 3. 取索引 5 到 15，每隔 2 个取一个
# 答案: numbers[5:15:2] → [5, 7, 9, 11, 13]
```

### 练习 3：实战应用

```python
# 实现一个函数，返回列表的前半部分和后半部分
def split_half(items):
    mid = len(items) // 2
    return items[:mid], items[mid:]

# 测试
data = [1, 2, 3, 4, 5, 6, 7, 8]
first, second = split_half(data)
print(first)   # [1, 2, 3, 4]
print(second)  # [5, 6, 7, 8]
```

## 总结

### 切片的核心优势

1. **语法简洁**：一行代码完成复杂操作
2. **功能强大**：支持正负索引、步长、反转
3. **安全性高**：不会抛出索引错误
4. **通用性强**：适用于列表、字符串、元组等

### 记忆技巧

- **`[start:end]`**：从 start 到 end（不含 end）
- **负数索引**：从后往前数（-1 是最后一个）
- **省略参数**：省略 start 从头开始，省略 end 到末尾
- **步长为负**：反向切片

### 学习建议

1. 多练习基础切片操作
2. 理解负数索引的含义
3. 掌握步长的使用
4. 在实际项目中应用
5. 对比 Java 的实现方式

## 参考资料

- [Python 官方文档 - 序列类型](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [Python 切片详解](https://docs.python.org/3/tutorial/introduction.html#lists)
- 项目代码：`worktrees/my-first-agent/agents/my first agent/main.py`（`_smart_trim` 方法）
