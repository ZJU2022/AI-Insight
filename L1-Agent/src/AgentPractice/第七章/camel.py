from typing import List, Dict
import json
import config
import requests
import os

# 定义一个通用的LLM接口类，用于替代DeepSeek
class LLM:
    def __init__(self, model_name: str = None):
        """
        初始化LLM模型
        Args:
            model_name: 使用的模型名称，默认使用环境变量中的配置
        """
        self.model_name = model_name or os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-r1:70b")
        self.api_base = os.getenv("DEEPSEEK_API_BASE")
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
    
    def generate(self, prompt: str) -> str:
        """
        生成文本响应
        Args:
            prompt: 输入提示
        Returns:
            模型生成的响应文本
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return f"Error: {str(e)}"

class Agent:
    """
    代理类：CAMEL框架中的核心组件
    每个代理代表一个具有特定角色的AI助手，可以独立思考和与其他代理交互
    """
    def __init__(self, name: str, role: str, model: LLM):
        """
        初始化代理
        Args:
            name: 代理名称
            role: 代理角色（如产品经理、开发者等）
            model: 使用的语言模型实例
        """
        self.name = name
        self.role = role
        self.model = model
        # 存储代理的对话历史
        self.conversation_history: List[Dict] = []

    def think(self, task: str) -> str:
        """
        代理独立思考方法
        让代理基于其角色对任务进行思考和分析
        
        Args:
            task: 需要思考的任务描述
        Returns:
            代理的思考结果
        """
        prompt = f"""作为{self.role}，你需要帮助完成以下任务：
        {task}
        
        请提供你的想法和解决方案。"""
        
        response = self.model.generate(prompt)
        # 记录对话历史
        self.conversation_history.append({
            "role": self.role,
            "content": response
        })
        return response

    def communicate(self, message: str, other_agent: 'Agent') -> str:
        """
        代理间通信方法
        实现代理之间的信息交换和协作
        
        Args:
            message: 要发送的消息
            other_agent: 接收消息的代理
        Returns:
            接收代理的响应
        """
        prompt = f"""作为{self.role}，你收到了来自{other_agent.role}的消息：
        {message}
        
        请提供你的回应。"""
        
        response = self.model.generate(prompt)
        self.conversation_history.append({
            "role": self.role,
            "content": response
        })
        return response

class Task:
    """
    任务类：用于表示和管理需要完成的工作
    支持任务分解和状态追踪
    """
    def __init__(self, description: str):
        """
        初始化任务
        Args:
            description: 任务描述
        """
        self.description = description
        self.subtasks: List[str] = []  # 存储分解后的子任务
        self.status = "pending"  # 任务状态

    def decompose(self, agent: Agent) -> List[str]:
        """
        任务分解方法
        将大任务分解成更小、更易管理的子任务
        
        Args:
            agent: 负责分解任务的代理
        Returns:
            分解后的子任务列表
        """
        prompt = f"""请帮助将以下任务分解成更小的子任务：
        {self.description}
        
        请以JSON数组格式返回子任务列表。"""
        
        response = agent.model.generate(prompt)
        try:
            self.subtasks = json.loads(response)
        except:
            self.subtasks = [response]
        return self.subtasks

def main():
    """
    主函数：演示CAMEL框架的工作流程
    展示了代理协作、任务分解和问题解决的过程
    """
    # 初始化语言模型
    model = LLM()
    
    # 创建两个不同角色的代理
    # 产品经理负责需求分析和任务规划
    product_manager = Agent("PM", "产品经理", model)
    # 开发者负责技术实现
    developer = Agent("Dev", "软件开发者", model)
    
    # 创建一个示例任务
    task = Task("设计并实现一个简单的待办事项应用")
    
    # 产品经理进行任务分解
    subtasks = task.decompose(product_manager)
    print("任务分解结果:", subtasks)
    
    # 代理协作处理每个子任务
    for subtask in subtasks:
        # 产品经理思考并提出需求
        pm_thoughts = product_manager.think(subtask)
        print(f"\n产品经理的想法: {pm_thoughts}")
        
        # 产品经理与开发者沟通需求
        dev_response = developer.communicate(pm_thoughts, product_manager)
        print(f"开发者的回应: {dev_response}")
        
        # 开发者思考技术实现方案
        dev_thoughts = developer.think(dev_response)
        print(f"开发者的实现方案: {dev_thoughts}")

if __name__ == "__main__":
    main()
