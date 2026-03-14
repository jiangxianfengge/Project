[推理时代](https://aihubmix.com/?aff=anNj)

里面提供了很多的免费API，能够方便学习。

在模型标签页选择==免费==可以看到很多免费的大模型。

密钥：sk-6PauFubw0XeksZBp32A4D13887044486942152Ce5d50E525

==如何使用呢==：

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-6PauFubw0XeksZBp32A4D13887044486942152Ce5d50E525" # 密钥
os.environ["OPENAI_BASE_URL"] = "https://aihubmix.com/v1"  # 网址

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI # 用于创建和配置LLM，大多数模型都兼容openai的API

def get_weather(city: str) -> str: # 定义工具
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = ChatOpenAI(
    model="coding-minimax-m2.5-free" # 模型的名称
)

agent = create_agent( # 创建agent
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke( # 运行agent
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

