from openai import OpenAI
import os
import json
import requests
from datetime import datetime
import config
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# 定义工具函数
def get_weather(location: str, date: str = None) -> str:
    """
    获取指定地点的天气信息（模拟函数）
    
    Args:
        location: 地点名称
        date: 日期（可选），格式：YYYY-MM-DD
    
    Returns:
        str: 天气信息
    """
    logger.info(f"调用天气查询函数 - 地点: {location}, 日期: {date}")
    
    # 这里使用模拟数据，实际应用中应该调用真实的天气 API
    weather_data = {
        "北京": {"temperature": "25°C", "condition": "晴朗", "humidity": "45%"},
        "上海": {"temperature": "28°C", "condition": "多云", "humidity": "60%"},
        "广州": {"temperature": "30°C", "condition": "雨", "humidity": "80%"},
        "深圳": {"temperature": "29°C", "condition": "阴", "humidity": "75%"}
    }
    
    if location in weather_data:
        weather = weather_data[location]
        date_str = f"在 {date}" if date else "今天"
        result = f"{location}{date_str}的天气：温度{weather['temperature']}，{weather['condition']}，湿度{weather['humidity']}"
        logger.info(f"天气查询结果: {result}")
        return result
    else:
        result = f"抱歉，没有找到{location}的天气信息"
        logger.warning(f"天气查询失败: {result}")
        return result

# 定义工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定地点的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "地点名称，例如：北京、上海、广州、深圳"
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式：YYYY-MM-DD，可选参数"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def process_function_call(function_call):
    """处理函数调用"""
    logger.info(f"开始处理函数调用 - 函数名: {function_call.name}")
    logger.info(f"函数参数: {function_call.arguments}")
    
    function_name = function_call.name
    function_args = json.loads(function_call.arguments)
    
    if function_name == "get_weather":
        result = get_weather(**function_args)
        logger.info(f"函数调用完成 - 结果: {result}")
        return result
    else:
        result = f"未知函数：{function_name}"
        logger.error(f"函数调用失败: {result}")
        return result

def chat_with_assistant(user_input):
    """与助手对话并处理函数调用"""
    logger.info(f"收到用户输入: {user_input}")
    
    # 创建对话
    logger.info("调用大模型 - 第一次对话")
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "你是一个天气助手，可以帮助用户查询天气信息。请使用提供的工具函数来获取天气数据。"},
            {"role": "user", "content": user_input}
        ],
        tools=tools,
        tool_choice="auto"
    )
    
    # 获取助手的回复
    assistant_message = response.choices[0].message
    logger.info(f"大模型回复: {assistant_message.content if assistant_message.content else '需要调用函数'}")
    
    # 检查是否需要调用函数
    if assistant_message.tool_calls:
        logger.info("检测到需要调用函数")
        # 处理函数调用
        tool_call = assistant_message.tool_calls[0]
        function_response = process_function_call(tool_call.function)
        
        # 将函数调用结果发送给助手
        logger.info("调用大模型 - 第二次对话（处理函数调用结果）")
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "你是一个天气助手，可以帮助用户查询天气信息。请使用提供的工具函数来获取天气数据。"},
                {"role": "user", "content": user_input},
                assistant_message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": function_response
                }
            ]
        )
        final_response = response.choices[0].message.content
        logger.info(f"大模型最终回复: {final_response}")
        return final_response
    else:
        logger.info("无需调用函数，直接返回大模型回复")
        return assistant_message.content

def main():
    print("\n" + "="*50)
    print("欢迎使用天气助手！输入 'quit' 退出。")
    print("示例问题：")
    print("1. 北京今天天气怎么样？")
    print("2. 上海明天的天气如何？")
    print("3. 广州和深圳的天气对比")
    print("="*50 + "\n")
    
    while True:
        user_input = input("\n请输入您的问题：")
        if user_input.lower() == 'quit':
            logger.info("用户退出程序")
            break
            
        try:
            logger.info("="*50)
            logger.info("开始新的对话轮次")
            response = chat_with_assistant(user_input)
            print("\n助手：", response)
            logger.info("对话轮次结束")
            logger.info("="*50)
        except Exception as e:
            error_msg = f"发生错误：{str(e)}"
            logger.error(error_msg)
            print(error_msg)

if __name__ == "__main__":
    main()
