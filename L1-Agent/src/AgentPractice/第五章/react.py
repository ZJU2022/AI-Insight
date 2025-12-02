from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
import os
import logging
from typing import Dict, Any
import config
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 初始化 SerpAPI
search = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY"),  # 从环境变量获取 SerpAPI key
    search_engine="google",  # 使用 Google 搜索引擎
    params={
        "gl": "cn",  # 设置地区为中国
        "hl": "zh-cn"  # 设置语言为中文
    }
)

# 创建工具
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="用于搜索互联网上的信息。输入参数是搜索查询。"
    )
]

# 创建 ReAct 提示模板
template = """你是一个智能助手，可以帮助用户查询信息并进行分析。你可以使用以下工具：

{tools}

工具名称: {tool_names}

使用以下格式：

问题：你必须回答的输入问题
思考：你应该一步步思考要做什么
行动：要使用的工具名称，例如 "Search"
行动输入：工具的输入参数
观察：工具的输出
...（这个思考/行动/行动输入/观察可以重复多次）
思考：我现在知道最终答案
最终答案：对原始输入问题的最终答案

问题：{input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# 创建 LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    request_timeout=30  # 设置请求超时时间
)

# 创建 ReAct Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  # 添加错误处理
    max_iterations=3  # 限制最大迭代次数
)

def process_query(query: str) -> Dict[str, Any]:
    """处理用户查询"""
    logger.info(f"收到查询: {query}")
    
    # 检查必要的环境变量
    if not os.getenv("SERPAPI_API_KEY"):
        error_msg = "错误：未设置 SERPAPI_API_KEY 环境变量。请设置 SERPAPI_API_KEY 以启用搜索功能。"
        logger.error(error_msg)
        return {"error": error_msg}
    
    try:
        # 添加重试机制
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                result = agent_executor.invoke({"input": query})
                logger.info(f"查询结果: {result}")
                return result
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"查询失败，正在重试 ({attempt + 1}/{max_retries}): {str(e)}")
                    time.sleep(retry_delay)
                else:
                    raise
    except Exception as e:
        error_msg = f"处理查询时发生错误: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def main():
    print("\n" + "="*50)
    print("欢迎使用智能搜索助手！")
    print("示例问题：")
    print("1. 当前玫瑰花的价格是多少？")
    print("2. 玫瑰花涨价5%后是多少钱？")
    print("3. 不同品种的玫瑰花价格对比")
    print("="*50 + "\n")
    
    # 检查环境变量
    if not os.getenv("SERPAPI_API_KEY"):
        print("\n警告：未设置 SERPAPI_API_KEY 环境变量。")
        print("请设置 SERPAPI_API_KEY 环境变量以启用搜索功能。")
        print("您可以在 https://serpapi.com/ 注册并获取 API key。")
        return
    
    while True:
        try:
            user_input = input("\n请输入您的问题（输入'quit'退出）：")
            if user_input.lower() == 'quit':
                logger.info("用户退出程序")
                break
                
            logger.info("="*50)
            logger.info("开始新的查询")
            result = process_query(user_input)
            print("\n系统回答：", result.get("output", "抱歉，无法处理您的请求。"))
            logger.info("查询结束")
            logger.info("="*50)
        except KeyboardInterrupt:
            print("\n程序被用户中断")
            break
        except Exception as e:
            error_msg = f"发生错误：{str(e)}"
            logger.error(error_msg)
            print(error_msg)

if __name__ == "__main__":
    main()
