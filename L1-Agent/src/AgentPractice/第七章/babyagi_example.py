import os
from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
from config import *  # 导入配置文件

class Task:
    def __init__(self, task_id: int, task_name: str, priority: int = 0):
        self.task_id = task_id
        self.task_name = task_name
        self.priority = priority
        self.status = "pending"
        self.result = None

class ExecutionAgent:
    """执行代理：负责执行具体任务"""
    def __init__(self, llm):
        self.llm = llm
        self.execution_prompt = PromptTemplate(
            input_variables=["task_name", "context"],
            template="""你是一个执行代理，负责完成具体任务。
            任务：{task_name}
            上下文信息：{context}
            请详细描述你的执行过程和结果。"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.execution_prompt)

    def execute(self, task: Task, context: str) -> str:
        """执行任务并返回结果"""
        result = self.chain.run(task_name=task.task_name, context=context)
        task.status = "completed"
        task.result = result
        return result

class TaskCreationAgent:
    """任务创建代理：根据执行结果生成新任务"""
    def __init__(self, llm):
        self.llm = llm
        self.creation_prompt = PromptTemplate(
            input_variables=["result", "objective"],
            template="""你是一个任务创建代理，负责根据执行结果生成新的任务。
            目标：{objective}
            当前执行结果：{result}
            请生成2-3个新的子任务，每个任务应该是具体且可执行的。
            返回格式：JSON数组，每个任务包含task_name和priority字段。"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.creation_prompt)

    def create_tasks(self, result: str, objective: str) -> List[Dict]:
        """根据执行结果创建新任务"""
        response = self.chain.run(result=result, objective=objective)
        try:
            return json.loads(response)
        except:
            return []

class PrioritizationAgent:
    """优先级代理：动态调整任务优先级"""
    def __init__(self, llm):
        self.llm = llm
        self.prioritization_prompt = PromptTemplate(
            input_variables=["tasks", "objective"],
            template="""你是一个优先级代理，负责调整任务优先级。
            目标：{objective}
            当前任务列表：{tasks}
            请根据目标的重要性和紧急性，重新评估每个任务的优先级（1-5，5最高）。
            返回格式：JSON数组，每个任务包含task_id和priority字段。"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prioritization_prompt)

    def prioritize(self, tasks: List[Task], objective: str) -> List[Task]:
        """调整任务优先级"""
        tasks_json = json.dumps([{"task_id": t.task_id, "task_name": t.task_name, "priority": t.priority} for t in tasks])
        response = self.chain.run(tasks=tasks_json, objective=objective)
        try:
            prioritized = json.loads(response)
            for task in tasks:
                for p in prioritized:
                    if p["task_id"] == task.task_id:
                        task.priority = p["priority"]
            return sorted(tasks, key=lambda x: x.priority, reverse=True)
        except:
            return tasks

class BabyAGI:
    def __init__(self):
        """
        初始化BabyAGI系统
        使用config.py中的配置信息
        """
        # 初始化LLM模型 - 使用Deepseek
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name=os.getenv("DEEPSEEK_MODEL_NAME"),
            openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
            openai_api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        
        # 初始化三个代理
        self.execution_agent = ExecutionAgent(self.llm)
        self.task_creation_agent = TaskCreationAgent(self.llm)
        self.prioritization_agent = PrioritizationAgent(self.llm)
        
        # 初始化向量数据库 - 使用HuggingFace的embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = Chroma(embedding_function=self.embeddings)
        
        # 初始化任务列表
        self.task_list: List[Task] = []
        self.task_id_counter = 0

    def add_task(self, task_name: str, priority: int = 0) -> Task:
        """添加新任务"""
        self.task_id_counter += 1
        task = Task(self.task_id_counter, task_name, priority)
        self.task_list.append(task)
        return task

    def get_context(self, task: Task) -> str:
        """获取任务相关的上下文信息"""
        # 从向量数据库中检索相关结果
        results = self.vectorstore.similarity_search(task.task_name, k=3)
        return "\n".join([doc.page_content for doc in results])

    def store_result(self, task: Task):
        """存储任务结果到向量数据库"""
        if task.result:
            doc = Document(
                page_content=task.result,
                metadata={"task_id": task.task_id}
            )
            self.vectorstore.add_documents([doc])

    def run(self, objective: str, max_iterations: int = 5):
        """运行BabyAGI系统"""
        # 创建初始任务
        initial_task = self.add_task(objective, priority=5)
        
        iteration = 0
        while iteration < max_iterations and self.task_list:
            # 获取优先级最高的任务
            current_task = self.prioritization_agent.prioritize(self.task_list, objective)[0]
            self.task_list.remove(current_task)
            
            print(f"\n执行任务 {current_task.task_id}: {current_task.task_name}")
            
            # 获取上下文
            context = self.get_context(current_task)
            
            # 执行任务
            result = self.execution_agent.execute(current_task, context)
            print(f"执行结果：{result}")
            
            # 存储结果
            self.store_result(current_task)
            
            # 创建新任务
            new_tasks = self.task_creation_agent.create_tasks(result, objective)
            for task_info in new_tasks:
                self.add_task(task_info["task_name"], task_info["priority"])
            
            iteration += 1
            
            if not self.task_list:
                print("\n所有任务已完成！")
                break

# 使用示例
if __name__ == "__main__":
    # 创建BabyAGI实例 - 不再需要传入API密钥
    baby_agi = BabyAGI()
    
    # 运行系统
    objective = "分析当前市场趋势并给出投资建议"
    baby_agi.run(objective) 