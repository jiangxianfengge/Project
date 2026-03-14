**核心概念：**
$$
Agent执行循环=自动化的“思考-行动-观察”过程
$$
Agent不是一次调用的，而是一个循环。

```
用户问题 → AI 思考 → 调用工具 → 观察结果 → 继续思考 → 最终答案
```







---

# 执行循环详解：

## 完整流程：

```
┌─────────────┐
│ 用户提问    │
│ HumanMessage│
└──────┬──────┘
       ↓
┌─────────────┐
│ AI 分析问题 │
│ 需要工具？  │
└──────┬──────┘
       ↓ 是
┌─────────────┐
│ AI 决定调用 │
│ AIMessage   │
│ (tool_calls)│
└──────┬──────┘
       ↓
┌─────────────┐
│ 执行工具    │
│ ToolMessage │
└──────┬──────┘
       ↓
┌─────────────┐
│ AI 看结果   │
│ 生成答案    │
│ AIMessage   │
└─────────────┘
```





## 消息历史示例：

```python
response = agent.invoke({'messages':[{"role": "user", "content": "25 乘以 8"}]
})

# response['messages'] 包含：
[
    HumanMessage(content="25 乘以 8"),
    AIMessage(tool_calls=[{
        'name': 'calculator',
        'args': {'operation': 'multiply', 'a': 25, 'b': 8}
    }]),
    ToolMessage(content="25.0 multiply 8.0 = 200.0"),
    AIMessage(content="25 乘以 8 等于 200")
]
```







---

# 查看执行流程：

## 1、查看完整历史：

```python
response = agent.invoke({"messages": [...]})

for msg in response['messages']:
    print(f"{msg.__class__.__name__}: {msg.content}")
```





## 2、获取最终答案：

```python
# 最后一条消息就是最终答案
final_answer = response['messages'][-1].content
```





## 3、查看使用的工具：

```python
used_tools = []
for msg in response['messages']:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            used_tools.append(tc['name'])

print(f"使用的工具: {used_tools}")
```

==对于一些函数的解释：==

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  hasattr() 函数                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  语法：                                                                  │
│  ──────                                                                 │
│  hasattr(对象，'属性名')                                                │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  作用：                                                                  │
│  ──────                                                                 │
│  • 检查对象是否有某个属性                                              │
│  • 返回 True 或 False                                                   │
│  • 避免访问不存在的属性时报错                                          │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  msg.tool_calls 结构                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  当 AI 决定调用工具时：                                                  │
│  ───────────────────                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AIMessage(                                                     │   │
│  │      content="",                                                │   │
│  │      tool_calls=[                                               │   │
│  │          {                                                      │   │
│  │              'name': 'get_weather',      ← 工具名               │   │
│  │              'args': {'city': '北京'},   ← 参数                 │   │
│  │              'id': 'call_abc123'         ← 调用 ID              │   │
│  │          },                                                     │   │
│  │          {                                                      │   │
│  │              'name': 'search_web',       ← 另一个工具           │   │
│  │              'args': {'query': 'AI 新闻'},                      │   │
│  │              'id': 'call_def456'                                │   │
│  │          }                                                      │   │
│  │      ]                                                          │   │
│  │  )                                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  当 AI 不调用工具时：                                                    │
│  ──────────────────                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AIMessage(                                                     │   │
│  │      content="你好！我是一个 AI 助手...",                        │   │
│  │      tool_calls=[]  ← 空列表                                    │   │
│  │  )                                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```







---

# 流式输出（Streaming）：

用于实时显示 Agent 的进度。

**两种流式模式对比：**

|       模式        |           参数           |         返回格式         |              用途              |
| :---------------: | :----------------------: | :----------------------: | :----------------------------: |
|  **按步骤输出**   | `stream_mode="updates"`  |          `dict`          | 显示每步进度（工具调用、结果） |
| **逐 token 输出** | `stream_mode="messages"` | `(chunk, metadata)` 元组 |    打字机效果，实时显示文字    |

## 方式1：按步骤输出(stream_mode="updates")

**特点：**每个节点(model、tools)执行完后返回一次，适合显示执行进度。

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "北京天气如何？"}]},
    stream_mode="updates"  # 默认模式
):
    for node_name, node_output in chunk.items():
        if 'messages' in node_output:
            latest_msg = node_output['messages'][-1]
            msg_type = latest_msg.__class__.__name__

            if msg_type == "AIMessage":
                if hasattr(latest_msg, 'tool_calls') and latest_msg.tool_calls:
                    print(f"[{node_name}] 调用工具: {latest_msg.tool_calls[0]['name']}")
                elif latest_msg.content:
                    print(f"[{node_name}] 最终回答: {latest_msg.content}")
            elif msg_type == "ToolMessage":
                print(f"[{node_name}] 工具返回: {latest_msg.content}")
```

**输出示例：**

```
[model] 调用工具: get_weather
[tools] 工具返回: 晴天，温度 15°C...
[model] 最终回答: 北京今天天气晴朗，温度15°C
```





## 方式2：逐token输出(`stream_mode='messages'`)

**特点：**逐字符/token 输出，实现打字机效果。返回 `(chunk, metadata)` 元组。

```python
print("回答: ", end="", flush=True)

for chunk, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "用一句话介绍 Python"}]},
    stream_mode="messages"  # 逐 token 模式
):
    # 只显示 model 节点的输出
    if metadata.get("langgraph_node") == "model":
        if hasattr(chunk, 'content') and chunk.content:
            print(chunk.content, end="", flush=True)

print()  # 换行
```

| 参数        | 默认值        | 这里设置        | 作用                     |
| :---------- | :------------ | :-------------- | :----------------------- |
| **`end`**   | `'\n'` (换行) | `''` (空字符串) | 不换行，继续在同一行输出 |
| **`flush`** | `False`       | `True`          | 立即刷新缓冲区，立刻显示 |

**输出效果（逐字显示）：**

```
回答: Python是一种简洁易读的编程语言...
```







---

# 两种模式的选择：

|        场景         |         推荐模式         |
| :-----------------: | :----------------------: |
| 显示 Agent 执行步骤 | `stream_mode="updates"`  |
| 聊天界面打字机效果  | `stream_mode="messages"` |
|  调试/监控工具调用  | `stream_mode="updates"`  |
|    用户体验优化     | `stream_mode="messages"` |







---

# stream vs invoke：

|    方法    |   返回   |          用途          |
| :--------: | :------: | :--------------------: |
| `invoke()` | 完整结果 |  等待完成后一次性获取  |
| `stream()` |  生成器  | 实时获取中间步骤/token |







---

# 消息类型：

## HumanMessage：

用户的输入`HumanMessage(content="北京天气如何？")`





## AIMessage：

### 情况1：调用工具

```python
AIMessage(
    content="",
    tool_calls=[{
        'name': 'get_weather',
        'args': {'city': '北京'},
        'id': 'call_xxx'
    }]
)
```



### 情况2：最终答案

`AIMessage(content="北京今天晴天，温度 15°C")`



### 区别：

- 使用工具的，会导致`content`为空，`tool_calls`存在一个列表，里面存放工具的`name、args和id`
- 不使用工具，那么就是最终的答案，`content`有一个`最终答案`。





## ToolMessage：

工具执行的结果：

```python
ToolMessage(
    content="晴天，温度 15°C",
    name="get_weather"
)
```





## SystemMessage：

系统指令（通过`system_prompt`设置）

```python
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个helpful assistant"
)
```







---

# 多步执行：

Agent 可以多次调用工具：

```python
# 问题：先算 10 + 20，然后乘以 3
response = agent.invoke({
    "messages": [{"role": "user", "content": "先算 10 + 20，然后乘以 3"}]
})

# Agent 可能会：
# 1. 调用 calculator(add, 10, 20) → 30
# 2. 调用 calculator(multiply, 30, 3) → 90
# 3. 返回最终答案
```

统计工具调用次数：

```python
tool_calls_count = sum(
    # 三元表达式 A if 条件 else B
    len(msg.tool_calls) if hasattr(msg, 'tool_calls') and msg.tool_calls else 0
    for msg in response['messages']
)
```







---

# 调试技巧：

## 1、打印所有的消息：

```python
for i, msg in enumerate(response['messages'], 1):
	# enumerate(可迭代对象，起始值) 
    # 实际是 msg 获得了enumerate中可迭代对象的值，i则是从i=1开始
    print(f"\n--- 消息 {i}: {msg.__class__.__name__} ---")

    if hasattr(msg, 'content'):
        print(f"内容: {msg.content}")

    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"工具: {tc['name']}, 参数: {tc['args']}")
```





## 2、使用stream查看步骤：

```python
step = 0
for chunk in agent.stream(input): # agent.stream(input)默认是updates
    step += 1
    print(f"步骤 {step}:")
    if 'messages' in chunk:
        latest = chunk['messages'][-1]
        print(f"  类型: {latest.__class__.__name__}")
```





## 3、检查是否使用工具：

```python
has_tool_calls = any( # 检查是否有任何一个元素为True
    hasattr(msg, 'tool_calls') and msg.tool_calls
    for msg in response['messages']
)

if has_tool_calls:
    print("Agent 使用了工具")
else:
    print("Agent 直接回答")
```







---

# 常见问题：

## 1、如何知道Agent合适完成？

==当AIMessage没有tool_calls时。==

```python
for msg in response['messages']:
    if isinstance(msg, 'AIMessage'):
        if hasattr(msg, 'tool_calls'):
            print("还在调用工具...")
        else:
            print("完成！最终答案：", msg.content)
```





## 2、Agent可以调用多少次工具？

==默认没有限制，直到得到最终答案。==

但可能会：

- 超时；
- 达到token限制；
- 模型决定停止。





## 3、如何限制工具调用次数？

LangChain1.0中的`create_agent`默认使用LangGraph，可以通过配置限制：

```python
# 注意：这是高级用法，后续会详细学习
config = {
    "recursion_limit": 5  # 最多 5 步
}

response = agent.invoke(input, config=config)
```

