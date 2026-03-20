# Python 成员变量与静态变量详解

## 1. 类变量（静态变量）与实例变量（成员变量）的区别

### 类变量（静态变量）
- 定义在类内部，但在方法之外
- 所有实例共享同一个变量
- 可以通过类名或实例访问
- 通常用于存储类级别的共享数据

### 实例变量（成员变量）
- 定义在 `__init__` 方法中，使用 `self.` 前缀
- 每个实例拥有自己的副本
- 通过 `self.变量名` 定义和访问

## 2. 代码示例

```python
class Person:
    # 类变量（静态变量） - 所有实例共享
    species = "人类"  # 类变量，所有Person实例共享
    count = 0        # 统计实例数量
    
    def __init__(self, name, age):
        # 实例变量（成员变量） - 每个实例独立
        self.name = name  # 实例变量，每个实例独立
        self.age = age    # 实例变量，每个实例独立
        
        # 修改类变量（通过类名访问）
        Person.count += 1  # 统计实例数量
    
    def display_info(self):
        """显示实例信息"""
        return f"{self.name}, {self.age}岁，物种：{self.species}"

# 测试代码
if __name__ == "__main__":
    # 创建实例
    p1 = Person("张三", 20)
    p2 = Person("李四", 25)
    
    # 访问类变量
    print(f"物种: {Person.species}")  # 通过类名访问
    print(f"实例数量: {Person.count}")  # 应该显示2
    
    # 访问实例变量
    print(f"p1: {p1.name}, {p1.age}岁")
    print(f"p2: {p2.name}, {p2.age}岁")
    
    # 通过实例访问类变量
    print(f"p1的物种: {p1.species}")  # 输出：人类
    print(f"p2的物种: {p2.species}")  # 输出：人类
    
    # 修改类变量会影响所有实例
    Person.species = "智人"
    print(f"修改后p1的物种: {p1.species}")  # 输出：智人
    print(f"修改后p2的物种: {p2.species}")  # 输出：智人
```

## 3. 与Java的区别

### Python 与 Java 的对比

| 特性 | Python | Java |
|------|--------|------|
| **类变量定义** | 直接定义在类中，方法外 | 使用 `static` 关键字 |
| **实例变量** | 在 `__init__` 中使用 `self.变量名` | 在类中直接定义，不使用 `static` |
| **访问方式** | 类名.变量名 或 实例.变量名 | 类名.变量名 或 实例.变量名 |
| **共享性** | 类变量被所有实例共享 | 静态变量被所有实例共享 |
| **内存** | 类变量只有一份，实例变量每个实例独立 | 静态变量只有一份，实例变量每个实例独立 |

## 4. 重要注意事项

### 4.1 类变量与实例变量的优先级
```python
class Example:
    class_var = "类变量"
    
    def __init__(self):
        self.class_var = "实例变量"  # 这会覆盖同名的类变量访问

e = Example()
print(e.class_var)  # 输出：实例变量（实例变量优先）
print(Example.class_var)  # 输出：类变量
```

### 4.2 修改类变量
```python
class Counter:
    count = 0  # 类变量
    
    def __init__(self):
        Counter.count += 1  # 通过类名修改类变量
        self.id = Counter.count  # 使用类变量为每个实例分配ID

# 测试
c1 = Counter()  # count=1, id=1
c2 = Counter()  # count=2, id=2
print(f"总实例数: {Counter.count}")  # 输出：2
```

### 4.3 类变量与实例变量的查找顺序
Python 查找变量时遵循 MRO（方法解析顺序）：
1. 先在实例的 `__dict__` 中查找
2. 然后在类的 `__dict__` 中查找
3. 最后在父类中查找

## 5. 最佳实践

1. **使用类变量存储共享数据**：如配置信息、计数器等
2. **使用实例变量存储实例特有数据**：如用户信息、状态等
3. **避免在实例中修改类变量**：应通过类名访问和修改
4. **使用属性（property）封装**：保护数据，提供更好的接口

```python
class Person:
    def __init__(self, name):
        self._name = name  # 使用下划线约定表示"受保护"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("姓名不能为空")
        self._name = value

# 使用属性而不是直接访问变量
p = Person("张三")
print(p.name)  # 使用属性访问
p.name = "李四"  # 使用setter方法
```

## 6. 总结

- **类变量（静态变量）**：所有实例共享，通过类名访问
- **实例变量（成员变量）**：每个实例独立，通过 `self.` 定义
- **优先使用属性（property）** 来封装数据访问
- **避免直接修改类变量**，除非明确需要共享状态

这种设计模式在需要统计实例数量、共享配置或实现单例模式时特别有用。