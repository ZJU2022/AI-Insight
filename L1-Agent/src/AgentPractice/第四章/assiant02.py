from openai import OpenAI
import os
import config
import time

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # 从环境变量获取 API key
)

def create_assistant():
    # 创建助手
    assistant = client.beta.assistants.create(
        name="数据分析助手",
        instructions="""我是一个专业的数据分析助手，可以帮助你进行数据分析和可视化。
        我可以使用Python创建各种图表，包括折线图、柱状图、散点图等。
        我会使用pandas进行数据处理，使用matplotlib和seaborn进行可视化。""",
        model="gpt-4-turbo-preview",
        tools=[{"type": "code_interpreter"}]  # 启用代码解释器
    )
    return assistant

def create_thread():
    # 创建对话线程
    thread = client.beta.threads.create()
    return thread

def add_message(thread_id, content):
    # 添加用户消息到线程
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message

def run_assistant(thread_id, assistant_id):
    # 运行助手
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run

def wait_for_run_completion(thread_id, run_id):
    # 等待 Run 完成
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == 'completed':
            return run
        elif run.status == 'failed':
            raise Exception(f"Run failed: {run.last_error}")
        elif run.status == 'requires_action':
            # 处理需要工具操作的情况
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                # 这里可以添加工具调用的处理逻辑
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": "Tool output here"
                })
            
            # 提交工具输出
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
        time.sleep(1)  # 避免过于频繁的API调用

def get_messages(thread_id):
    # 获取对话历史
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages

def print_message_content(message):
    """打印消息内容，处理不同类型的消息块"""
    for content in message.content:
        if hasattr(content, 'text'):
            print(f"{message.role}: {content.text.value}")
        elif hasattr(content, 'image_file'):
            print(f"{message.role}: [包含图片: {content.image_file.file_id}]")

def main():
    # 创建助手
    assistant = create_assistant()
    print(f"助手已创建，ID: {assistant.id}")
    
    # 创建对话线程
    thread = create_thread()
    print(f"对话线程已创建，ID: {thread.id}")
    
    # 示例：添加数据分析请求
    analysis_request = """
    请帮我分析以下数据并创建可视化图表：
    
    1. 创建一个包含以下数据的DataFrame：
       - 日期：2024年1月1日到2024年1月10日
       - 销售额：随机生成1000到5000之间的数据
       - 客户数量：随机生成50到200之间的数据
       
    2. 创建以下图表：
       - 销售额随时间变化的折线图
       - 销售额和客户数量的散点图
       - 销售额的箱线图
       
    3. 添加适当的标题、标签和图例
    4. 使用seaborn设置美观的样式
    5. 请确保保存图表到文件，并告诉我文件的位置
    """
    
    message = add_message(thread.id, analysis_request)
    print("数据分析请求已添加")
    
    # 运行助手并等待完成
    run = run_assistant(thread.id, assistant.id)
    print(f"助手运行中，Run ID: {run.id}")
    
    try:
        completed_run = wait_for_run_completion(thread.id, run.id)
        print("Run 已完成")
        
        # 获取对话历史
        messages = get_messages(thread.id)
        for msg in messages.data:
            print_message_content(msg)
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
