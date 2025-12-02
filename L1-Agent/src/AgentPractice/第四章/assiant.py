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
        name="代码助手",
        instructions="我是一个专业的代码助手，可以帮助你解决编程问题。",
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

def main():
    # 创建助手
    assistant = create_assistant()
    print(f"助手已创建，ID: {assistant.id}")
    
    # 创建对话线程
    thread = create_thread()
    print(f"对话线程已创建，ID: {thread.id}")
    
    # 示例：添加消息并运行助手
    message = add_message(thread.id, "请帮我写一个计算斐波那契数列的函数")
    print("消息已添加")
    
    # 运行助手并等待完成
    run = run_assistant(thread.id, assistant.id)
    print(f"助手运行中，Run ID: {run.id}")
    
    try:
        completed_run = wait_for_run_completion(thread.id, run.id)
        print("Run 已完成")
        
        # 获取对话历史 
        messages = get_messages(thread.id)
        for msg in messages.data:
            print(f"{msg.role}: {msg.content[0].text.value}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
