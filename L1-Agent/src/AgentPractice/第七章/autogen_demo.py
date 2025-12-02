from autogen import AssistantAgent, UserProxyAgent
import autogen
import config
import os

# 配置DeepSeek模型
config_list = [
    {
        "model": os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-r1:70b"),
        "base_url": os.getenv("DEEPSEEK_API_BASE"),
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
    }
]

# 配置LLM
llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "max_tokens": 2000,
}

def main():
    """
    主函数：演示AutoGen框架的核心功能
    展示了多代理协作、任务分解和自动化执行的过程
    """
    
    # 创建用户代理（User Proxy Agent）
    # 用户代理代表人类用户，可以执行代码并与其他代理交互
    user_proxy = UserProxyAgent(
        name="用户代理",
        system_message="""你是一个用户代理，负责：
        1. 接收用户的任务需求
        2. 与助手代理协作完成任务
        3. 执行代码并验证结果
        4. 提供反馈和指导""",
        code_execution_config={"last_n_messages": 3, "work_dir": "workspace", "use_docker": False},
        human_input_mode="NEVER"  # 设置为NEVER以自动化执行
    )

    # 创建助手代理（Assistant Agent）
    # 助手代理负责提供解决方案和执行具体任务
    assistant = AssistantAgent(
        name="助手代理",
        system_message="""你是一个专业的AI助手，负责：
        1. 分析任务需求
        2. 提供解决方案
        3. 编写代码
        4. 解释实现细节""",
        llm_config=llm_config
    )

    # 创建代码执行代理（Code Execution Agent）
    # 专门负责代码的编写和执行
    coder = AssistantAgent(
        name="代码执行代理",
        system_message="""你是一个专业的程序员，负责：
        1. 编写高质量的代码
        2. 确保代码的可执行性
        3. 处理代码相关的错误
        4. 优化代码性能""",
        llm_config=llm_config
    )

    # 定义任务
    task = """
    请帮我实现一个简单的待办事项（Todo）应用，要求：
    1. 能够添加、删除、查看待办事项
    2. 支持标记待办事项为已完成
    3. 数据持久化存储
    4. 提供简单的命令行界面
    """

    # 启动多代理协作
    # 用户代理发起对话，其他代理自动响应和协作
    user_proxy.initiate_chat(
        assistant,
        message=task
    )

    # 添加代码执行代理到对话中
    user_proxy.initiate_chat(
        coder,
        message="请实现上述待办事项应用的具体代码。"
    )

if __name__ == "__main__":
    main()
