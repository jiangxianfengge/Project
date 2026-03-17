# """
# Configuration for the Aligo Multi-Agent System
# """
# import os
# API_KEY = os.environ.get("DEEPSEEK_API_KEY")
#
# # LLM Configuration
# LLM_CONFIG = {
#     "api_key": API_KEY,
#     "model_name": "deepseek-chat",
#     "base_url": "https://api.deepseek.com",
#     "temperature": 0.7,
#     "max_tokens": 8192,
# }
#
# # System Configuration
# SYSTEM_CONFIG = {
#     "enable_llm": True,  # Set to True to use LLM (recommended), False for rule-based
#     "log_level": "INFO",
#     "max_retries": 3,
#     "timeout": 60,  # Increased timeout for better stability
# }
#
# # RAG 知识库：嵌入模型（本地路径，无需连 HuggingFace）
# RAG_CONFIG = {
#     "embedding_model": "data/models/bge-small-zh-v1.5",
# }
#
# # 连接与可用性：重试、熔断、健康检查
# RESILIENCE_CONFIG = {
#     "max_retries": 3,              # 单次请求最大重试次数（与 SYSTEM_CONFIG 对齐）
#     "retry_base_delay_sec": 1.0,   # 重试退避基数（秒）
#     "retry_max_delay_sec": 30.0,   # 重试退避上限（秒）
#     "circuit_failure_threshold": 5, # 连续失败多少次后熔断
#     "circuit_recovery_timeout_sec": 60.0,  # 熔断后多少秒进入半开
#     "circuit_half_open_successes": 2,      # 半开状态下连续成功多少次后关闭
#     "health_check_timeout_sec": 10.0,      # 健康检查请求超时（秒）
# }

"""
Aligo 多智能体系统的配置文件
"""
import os

# 从环境变量中读取 DeepSeek 的 API Key
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# 大语言模型配置
LLM_CONFIG = {
    "api_key": API_KEY,                       # DeepSeek API 密钥
    "model_name": "deepseek-chat",           # 使用的模型名称
    "base_url": "https://api.deepseek.com",  # DeepSeek 接口基础地址
    "temperature": 0.7,                      # 采样温度，越高越发散，越低越稳定
    "max_tokens": 8192,                      # 单次生成的最大输出 token 数
}

# 系统级配置
SYSTEM_CONFIG = {
    "enable_llm": True,      # 是否启用大模型；True 表示使用 LLM，False 表示使用规则逻辑
    "log_level": "INFO",     # 日志级别
    "max_retries": 3,        # 系统层面的最大重试次数
    "timeout": 60,           # 单次请求超时时间（秒），适当调大可提升稳定性
}

# RAG 知识库配置：本地嵌入模型路径（无需联网下载 HuggingFace 模型）
RAG_CONFIG = {
    "embedding_model": "data/models/bge-small-zh-v1.5",
}

# 弹性与可用性配置：重试、熔断、健康检查
RESILIENCE_CONFIG = {
    "max_retries": 3,                    # 单次请求的最大重试次数（与 SYSTEM_CONFIG 保持一致）
    "retry_base_delay_sec": 1.0,         # 重试退避的基础延迟时间（秒）
    "retry_max_delay_sec": 30.0,         # 重试退避的最大延迟时间（秒）
    "circuit_failure_threshold": 5,      # 连续失败达到多少次后触发熔断
    "circuit_recovery_timeout_sec": 60.0,# 熔断后经过多少秒进入半开状态
    "circuit_half_open_successes": 2,    # 半开状态下连续成功多少次后恢复为关闭状态
    "health_check_timeout_sec": 10.0,    # 健康检查请求的超时时间（秒）
}