# 一、init_chat_model - 模型初始化：

`init_chat_model`是 LangChain 1.0 中用于初始化聊天模型的**统一接口**。

**基本语法：**

```python
from langchain.chat_model import init_chat_model

model = init_chat_model{
    'provider:model_name', 	# 提供商:模型名称
    api_key="your-api-key", # API密钥（可选，可从环境变量中读取）
    temperature=0.7, 		# 温度参数，可选
    max_tokens=1000, 		# 最大 token 数（可选）
    **kwargs 				# 其他模型特定参数
}
```

- `model`：类型为**str**，是==必须的==，格式为`'provider:model_name'`，如`groq:llama-3.3-70b-versatile`，没有默认值；
- `api_key`：类型为**str**，API密钥，==若不提供，会从环境变量中提取==；
- `temperature`：类型为**float**，控制随机项，范围0.0~2.0，默认值为1.0；
	- 0.0：表示最确定性；
	- 1.0：表示默认的，平衡的；
	- 2.0：表示最随机的。
- `max_tokens`：类型为**int**，限制模型输出的最大token数量，默认值为**模型默认值**；
- `model_kwargs`：类型为**dict**，传递给底层模型的额外参数，默认值为**{}**。

**支持的提供商格式：**

```
# Groq
"groq:llama-3.3-70b-versatile"
"groq:mixtral-8x7b-32768"
"groq:gemma2-9b-it"

# OpenAI
"openai:gpt-4"
"openai:gpt-3.5-turbo"

# Anthropic
"anthropic:claude-sonnet-4-5-20250929"

# 其他提供商...
```

**使用`init_chat_model`的原因：**

- 统一接口；
- 易于切换模型；
- 类型安全；
- 简洁。

**示例：**

```python
from langchain.chat_model import init_chat_model
import os

# 方式1：直接传递API key
model = init_chat_model(
    "grop:llama-3.3-70b-versatile",
    api_key=''
)
# 方式2：从环境变量中读取（推荐）
model = init_chat_model(
    'grop:llama-3.3-70b-versatile',
    api_key=os.getenv("GROP_API_KEY")
)
# 方式3：配置温度和token限制
model = init_chat_model(
    'grop:llama-3.3-70b-versatile',
    api_key=os.getenv('GROP_API_KEY'),
    temperature=0.0,
    max_tokens=1000
)
```







---

# 二、invoke方法-调用模型：

`invoke`是LangChain中**最核心的方法**，用于同步调用LLM模型。理解`invoke`是学习LangChain的关键。

## invoke方法的作用：

1. **接收你的输入（问题、指令、对话历史等）**；
2. **发送给LLM模型**；
3. **返回模型的响应（文本回复 + 元数据信息）**。

==流程：==

```
你的输入 → invoke() → LLM 模型 → 响应 → 返回给你
```

==基本语法：==

```python
response = model.invoke(input, config=None)
```

- `input`：类型为`str | list[dict] | list[Message]`，也就是需要发送给模型的内容，是必须的；

	- **纯字符串：**最简单，适用于单词问题。

		- `model.invoke('你的问题')`

		- ```python
			from langchain.chat_model import init_chat_model
			
			model = init_chat_model("grop:llama-3.3-70b-versatile", api_key=os.getenv('GROP_API_KEY'))
			
			response = model.invoke("什么是机器学习？用一句话解释。")
			
			print(response.content)
			```

		- **优点**：最简单，适合快速测试；

		- **缺点：**无法设置系统提示，无法传递对话历史，灵活性低。

	- **字典列表（推荐，最灵活）：**需要设置系统角色、多轮对话、精确控制对话流程。

		- ```python
			messages=[
				{"role":"system", "content":"系统提示"}, 
				{"role":"user", "content":"用户消息"},
				{"role":"assistant", "content":"AI回复"},
				{"role":"user", "content":"继续提问"}
			]
			reponse = model.invoke(messages)
			```

		- ```python
			# 设置系统提示
			messages=[
			    {'role': 'system', 
			     'content': '你是一个专业的 Python 编程导师。回答要简洁、准确，并提供代码示例。'
			    },
			    {'role':'user', 
			     'content':'什么是 Python 列表推导式？'
			    }
			]
			```

		- ```python
			# 多轮对话，带历史
			# 第一轮对话
			messages=[
			    {'role': 'system', 'content':'你是一个友好的助手'},
			    {'role':'user', 'content':'我叫小明'}
			]
			
			response1 = model.invoke(messages)
			print(response1.content)
			
			# 第二轮对话
			messages.append('role':'system', 'content':response1.content)
			messages.append('role':'user', 'content':'我刚刚说我叫什么？')
			
			response2 = model.invoke(messages)
			print(response2.content) # 你说你叫小明
			```

		- ```python
			# 构建完整的对话
			# 初始化对话
			conversation = [
			    {"role": "system", "content": "你是一个 Python 专家"}
			]
			
			# 用户提问 1
			conversation.append({"role": "user", "content": "什么是列表？"})
			response1 = model.invoke(conversation)
			print(f"AI: {response1.content}")
			
			# 保存 AI 回复到历史
			conversation.append({"role": "assistant", "content": response1.content})
			
			# 用户提问 2（基于上下文）
			conversation.append({"role": "user", "content": "它和元组有什么区别？"})
			response2 = model.invoke(conversation)
			print(f"AI: {response2.content}")
			
			# 此时 conversation 包含完整的对话历史
			print(f"\n完整对话历史: {conversation}")
			```

		- **优点：**最灵活，完全控制；可以设置系统提示；支持多轮对话；与OpenAI格式一致；与JSON兼容。

		- **缺点：**代码更多（但是更清晰）。

		- ==推荐用于所有场景==。

	- **消息对象列表（类型安全，但是较为繁琐）：**

		- ```python
			# 语法
			from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
			
			messages = [
			    SystemMessage(content='系统提示'),
			    HumanMessage(content='用户消息'),
			    AIMessage(content='AI回复')
			]
			response = model.invoke(messages)
			```

			- `SystemMessage`：对应字典格式`{'role':'system', ...}`，作用为==系统提示==；
			- `HumanMessage`：对应字典格式`{'role':'user', ...}`，作用为==用户输入==；
			- `AIMessage`：对应字典格式`{'role':'assistant', ...}`，作用为==AI回复==。

		- ```python
			from langchain_core.message import SystemMessage, HumanMessage, AIMessage
			
			messages=[
			    SystemMessage(content='你是一个Python专家'),
			    HumanMessage(content='什么是生成器'),
			]
			
			response = model.invoke(messages)
			
			# 继续对话
			messages.append(AIMessage(content=response.content))
			messages.append(HumanMessage(content='能给个例子吗？'))
			
			response2 = model.invoke(messages)
			```

		- **优点：**类型安全、IDE自动补全，更容易发现错误；

		- **缺点：**代码较长，不如字典简洁，难以序列化（JSON）。

		- ==大型项目、团队协作时使用==。

- `config`：类型为`dict`，是高级配置，可选的，默认值为None。





## invoke返回值详解：

`invoke`返回一个AIMessage对象，包含丰富的信息：

- `response.content`：str类型，AI的回复文本；
- `response.response_metadata`：dict类型，响应元数据；
- `response.id`：str，消息唯一ID；
- `response.usage_metadata`：dict，Token使用情况；
- `response.additional_kwargs`：dict，其他额外信息。

**完整示例：**

```python
response = model.invoke('用一句话解释什么是AI')

# 1、获取回复内容
print("AI回复：", reponse.content)

# 2、获取模型信息
metadata = response.response_metadata
print(f"使用的模型：{metadata['model_name']}") # 可以替换为metadata.get('model_name')
print(f"结束原因：{metadata['finsh_reason']}")

# 3、获取Token使用情况
usage = metadata.get('token_usage', {}) # 后面的{}表示当key不存在时就返回空字典
print(f"提示 tokens: {usage.get('prompt_tokens')}") # 更安全，key不存在就返回None
print(f"完成 tokens: {usage.get('completion_tokens')}")
print(f"总计 tokens: {usage.get('total_tokens')}")

# 4. 获取消息 ID
print(f"消息 ID: {response.id}")
```

**response_metadata完整结构：**

```
{
    'model_name': 'llama-3.3-70b-versatile',      # 使用的模型
    'system_fingerprint': 'fp_4cfc2deea6',        # 系统指纹
    'finish_reason': 'stop',                      # 结束原因：stop/length/error
    'model_provider': 'groq',                     # 模型提供商
    'token_usage': {                              # Token 使用统计
        'prompt_tokens': 15,                      # 输入 tokens
        'completion_tokens': 25,                  # 输出 tokens
        'total_tokens': 40,                       # 总计 tokens
        'prompt_time': 0.002,                     # 输入处理时间（秒）
        'completion_time': 0.23                   # 输出生成时间（秒）
    }
}
```





## config参数（高级技术）：

`config`参数用于传递高级配置，一般初学者用不太到。

**常用配置：**

```python
config = {
    'callbacks':[callback_handler], 	# 回调参数
    'tags':["test", "development"], 	# 标签（用于追踪）
    'metadata':{"user_id": "123"}, 		# 元数据
    'run_name':"my_query"				# 运行名称
}

response = model.invoke(messages, config=config)
```

暂时可以忽略。







---

# 三、Messages-消息类型：

LangChain使用不同的消息类型来表示对话中的不同角色。

|    消息类型     |    角色     |            用途            |               示例                |
| :-------------: | :---------: | :------------------------: | :-------------------------------: |
| `SystemMessage` |  `system`   | 设定 AI 的行为、角色、规则 |     "你是一个专业的数学老师"      |
| `HumanMessage`  |   `user`    |         用户的输入         |         "什么是微积分？"          |
|   `AIMessage`   | `assistant` |         AI 的回复          | "微积分是研究变化率的数学分支..." |

**使用消息对象：**

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 创建消息
system_msg = SystemMessage(content="你是一个友好的助手")
human_msg = HumanMessage(content="你好")
ai_msg = AIMessage(content="你好！我能帮你什么？")

# 构建历史
messages = [system_msg, human_msg, ai_msg]
messages.append(HumanMessage(content='今天天气怎么样？'))

# 调用模型
response = model.invoke(messages)
```

