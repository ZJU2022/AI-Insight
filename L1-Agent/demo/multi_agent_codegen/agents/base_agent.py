"""
基础Agent类：定义所有Agent的通用接口和功能

核心知识点：
1. Agent的四大核心要素：规划、记忆、工具、执行
2. Agent的基本结构：角色定义、系统消息、工具配置
3. Agent间的通信机制
"""
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
import config


class BaseAgent:
    """
    基础Agent类：所有专业Agent的基类
    
    核心特性：
    - 自主性：能够独立思考和决策
    - 适应性：能够根据反馈调整行为
    - 交互性：能够与其他Agent和工具交互
    - 功能性：专注于特定领域的任务
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        system_message: str,
        tools: Optional[List[BaseTool]] = None,
        model_name: str = None
    ):
        """
        初始化Agent
        
        Args:
            name: Agent名称
            role: Agent角色（如需求分析师、架构师等）
            system_message: 系统消息，定义Agent的行为和职责
            tools: Agent可用的工具列表
            model_name: 使用的LLM模型名称
        """
        self.name = name
        self.role = role
        self.system_message = system_message
        self.tools = tools or []
        
        # 初始化LLM（Agent的"大脑"）
        self.llm = ChatOpenAI(
            model=model_name or config.Config.OPENAI_MODEL,
            temperature=config.Config.TEMPERATURE,
            max_tokens=config.Config.MAX_TOKENS,
            openai_api_key=config.Config.OPENAI_API_KEY
        )
        
        # 初始化记忆模块（短期记忆）
        # 存储当前会话的上下文信息
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 任务历史（长期记忆的简化版本）
        self.task_history: List[Dict] = []
    
    def think(self, task: str, context: Optional[Dict] = None) -> str:
        """
        Agent思考方法：基于任务和上下文进行推理
        
        这是Agent的"规划"模块的核心实现
        
        Args:
            task: 需要处理的任务
            context: 上下文信息（来自其他Agent的输出）
            
        Returns:
            Agent的思考结果
        """
        # 构建Prompt，包含系统消息、上下文和任务
        prompt = f"""{self.system_message}

当前任务: {task}

{f"上下文信息: {context}" if context else ""}

请基于你的角色和专业能力，提供你的分析和建议。"""
        
        # 调用LLM进行推理
        response = self.llm.invoke(prompt)
        
        # 记录到任务历史
        self.task_history.append({
            "task": task,
            "context": context,
            "response": response.content
        })
        
        return response.content
    
    def execute(self, action: str, parameters: Optional[Dict] = None) -> str:
        """
        Agent执行方法：调用工具执行具体操作
        
        这是Agent的"执行"模块的核心实现
        
        Args:
            action: 要执行的动作
            parameters: 动作参数
            
        Returns:
            执行结果
        """
        # 查找匹配的工具
        tool = None
        for t in self.tools:
            if t.name == action or action in t.description:
                tool = t
                break
        
        if tool:
            try:
                # 执行工具
                result = tool.run(parameters or {})
                return f"工具 {tool.name} 执行成功: {result}"
            except Exception as e:
                return f"工具 {tool.name} 执行失败: {str(e)}"
        else:
            return f"未找到匹配的工具: {action}"
    
    def communicate(self, message: str, other_agent: 'BaseAgent') -> str:
        """
        Agent间通信方法：实现多Agent协作
        
        这是多Agent系统的核心：Agent之间的信息交换
        
        Args:
            message: 要发送的消息
            other_agent: 接收消息的Agent
            
        Returns:
            接收Agent的响应
        """
        # 构建通信Prompt
        prompt = f"""{self.system_message}

你收到了来自 {other_agent.role} ({other_agent.name}) 的消息:
{message}

请基于你的专业能力，提供回应和建议。"""
        
        response = self.llm.invoke(prompt)
        
        # 记录通信历史
        self.memory.save_context(
            {"input": f"[来自 {other_agent.name}]: {message}"},
            {"output": response.content}
        )
        
        return response.content
    
    def reflect(self, result: str, original_task: str) -> str:
        """
        Agent反思方法：评估执行结果并调整策略
        
        这是Agent"适应性"的体现：根据反馈调整行为
        
        Args:
            result: 执行结果
            original_task: 原始任务
            
        Returns:
            反思和改进建议
        """
        prompt = f"""{self.system_message}

原始任务: {original_task}
执行结果: {result}

请反思：
1. 任务是否完成？
2. 结果是否符合预期？
3. 有哪些可以改进的地方？
4. 下一步应该做什么？"""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def get_memory_summary(self) -> str:
        """
        获取记忆摘要：用于长期记忆管理
        
        Returns:
            记忆摘要
        """
        if not self.task_history:
            return "暂无任务历史"
        
        summary = f"{self.role} ({self.name}) 的任务历史:\n"
        for i, task in enumerate(self.task_history[-5:], 1):  # 只显示最近5条
            summary += f"{i}. {task['task'][:50]}...\n"
        
        return summary

