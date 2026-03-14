# 一、三种消息类型：

|   角色    |                 字典格式                 |           对象格式            |   用途   |
| :-------: | :--------------------------------------: | :---------------------------: | :------: |
|  System   |  {'role': "system", 'content': 'text'}   | SystemMessage(content='text') | 系统提示 |
|   User    |   {'role': 'user', 'content': 'text'}    | HumanMessage(content='text')  | 用户输入 |
| Assistant | {'role': 'assistant', 'content': 'text'} |   AIMessae(content='text')    |  AI回复  |

```python
messages = [
    {'role':'system', 'content':'你是助手'},
    {'role':'user', 'content':"你好"}
]

from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content='你是助手。'),
    HumanMessage(content='你好。')
]
```







---

# 二、对话历史管理（关键）：

==关键规则：==每次调用时都需要**传入完整的对话历史**。

```python
from langchain_core.messages import (SystemMessage, HumanMessage, AIMessage)

conversation = []

# 第一次
conversation.append(SystemMessage(content='我叫张三'))
r1 = model.invoke(conversation)

# 保留AI回复
conversation.append(AIMessage(content=r1.content))

# 第二次（传递完整历史）
conversation.append(HumanMessage(content='我叫什么？'))
r2 = model.invoke(conversation) # 这样AI就能记得历史记录了。
```

**对话流程：**

```
第 1 轮：
  [system, user] → AI回复 → 保存回复

第 2 轮：
  [system, user, assistant, user] → AI回复 → 保存回复

第 3 轮：
  [system, user, assistant, user, assistant, user] → AI回复

每次都传递所有历史！
```







---

# 三、对话历史优化（避免过长）：

==问题：==对话历史会越来越差，那么就会消耗大量的tokens和成本。

**解决方案：**只保留最近 N 轮的对话。

```python
def keep_recent_messages(messages, max_pairs=3):
    """
    保留最近的 N 轮对话
    
    max_pairs：保留的对话轮数。
    	轮数的计算规则 = user + assistant
    """
    
    # 分离 system 和对话
    system_messages = [for m in messages if m.get('role') == 'system']
    conversation = [for m in messages if m.get('role') != 'system']
    
    # 只保留最近的conversation,对于system_messages不做处理
    
    recent = conversation[-(max_pairs * 2):] # 表示从倒数第2max_pairs开始取到最后
    
    return system_messages + recent

# 如何使用呢
optimized_messages = keep_recent_messages(conversation, max_pairs=5)
response = model.invoke(optimized)
```

**原理：**

- 总是保留 system 消息（定义角色）
- 只保留最近 5 轮对话（10 条消息）
- 丢弃更早的历史

## 完整示例：

```python
# 初始化
conversation = [
    {"role": "system", "content": "你是 Python 导师"}
]

# 第 1 轮
conversation.append({"role": "user", "content": "什么是列表？"})
r1 = model.invoke(conversation)
conversation.append({"role": "assistant", "content": r1.content})

# 第 2 轮
conversation.append({"role": "user", "content": "它和元组有什么区别？"})
r2 = model.invoke(conversation)
conversation.append({"role": "assistant", "content": r2.content})

# 第 3 轮（测试记忆）
conversation.append({"role": "user", "content": "我第一个问题问的是什么？"})
r3 = model.invoke(conversation)
# AI 会回答："你问的是什么是列表"

# 优化：只保留最近 3 轮
optimized = keep_recent_messages(conversation, max_pairs=3)
```







---

# 总结：

- **历史：**每次必须传递完整的历史；
- **保存：**必须保存AI的回复；
- **优化：**只保存最近N轮；
- **System：**总是保留System的消息。