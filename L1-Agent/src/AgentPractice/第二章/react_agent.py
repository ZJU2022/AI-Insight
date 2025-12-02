# 导入必要的模块
import os
from langchain import hub  # 用于获取预定义的提示模板
from langchain_openai import OpenAI  # OpenAI语言模型接口
from langchain_community.utilities import SerpAPIWrapper  # 用于网络搜索功能
from langchain.tools import Tool  # 用于创建工具
from langchain.agents import create_react_agent, AgentExecutor  # 用于创建ReAct代理和执行器
import logging  # 用于日志记录
import config  # 导入配置文件，确保在所有用到API Key的包之前导入

# 配置日志记录
logging.basicConfig(level=logging.INFO)  # 设置日志级别为INFO
logger = logging.getLogger(__name__)  # 创建日志记录器

# 从LangChain Hub获取ReAct提示模板
# ReAct是一种结合推理(Reasoning)和行动(Acting)的框架
prompt = hub.pull("hwchase17/react")
print("ReAct Prompt:", prompt)

# 初始化OpenAI语言模型
# temperature参数控制输出的随机性：
# - 0.0: 输出最确定性的结果
# - 0.7: 平衡创造性和准确性
# - 1.0: 最大程度的创造性
llm = OpenAI(
    temperature=0.7,  # 设置温度为0.7，使回答既保持一定创造性又不会太过随机
)

# 初始化SerpAPI搜索工具
# SerpAPI是一个网络搜索API，用于获取实时信息
search = SerpAPIWrapper()

# 准备工具列表
# 这里我们只使用搜索工具，但可以根据需要添加更多工具
tools = [
    Tool(
        name="Search",  # 工具名称
        func=search.run,  # 工具函数
        description="当大模型没有相关知识时，用于搜索知识"  # 工具描述
    )
]

# 创建ReAct代理
# ReAct代理结合了语言模型和工具，能够进行推理和行动
agent = create_react_agent(llm, tools, prompt)

# 创建代理执行器
# 执行器负责运行代理，处理输入输出，并管理工具调用
agent_executor = AgentExecutor(
    agent=agent,  # 使用的代理
    tools=tools,  # 可用的工具
    verbose=True,  # 显示详细的执行过程
    handle_parsing_errors=True  # 自动处理解析错误
)

# 主程序入口
if __name__ == "__main__":
    try:
        # 使用代理回答问题
        # 这里我们询问Agent的最新研究进展
        response = agent_executor.invoke({"input": "当前 Agent最新研究进展是什么？请用中文回答"})
        
        # 将输出转换为中文
        # 如果输出是字符串类型，使用LLM进行翻译
        if isinstance(response['output'], str):
            # 构建翻译提示词
            translation_prompt = f"请将以下英文翻译成中文，保持专业性和准确性：\n{response['output']}"
            # 使用LLM进行翻译
            chinese_output = llm.invoke(translation_prompt)
            # 更新响应中的输出为中文
            response['output'] = chinese_output
            
        # 打印代理的响应
        print("\nAgent Response:", response)
    except Exception as e:
        # 错误处理
        logger.error(f"执行过程中出现错误: {str(e)}")  # 记录错误日志
        print(f"\n执行出错: {str(e)}")  # 打印错误信息 