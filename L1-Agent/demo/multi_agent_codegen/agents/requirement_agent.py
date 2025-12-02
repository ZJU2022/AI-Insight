"""
需求分析Agent：负责分析用户需求，拆解任务

核心知识点：
1. 任务分解（Planning）：将复杂需求拆解为可执行的子任务
2. 需求澄清：通过提问补充缺失信息
3. 需求文档生成：输出结构化的需求文档
"""
from .base_agent import BaseAgent
from langchain.tools import Tool
from typing import List, Dict


class RequirementAgent(BaseAgent):
    """
    需求分析Agent
    
    职责：
    1. 分析用户需求
    2. 拆解复杂任务为子任务
    3. 生成需求文档
    4. 与用户和其他Agent沟通澄清需求
    """
    
    def __init__(self, model_name: str = None):
        """初始化需求分析Agent"""
        system_message = """你是一位专业的需求分析师，擅长：
1. 理解用户需求，识别核心功能点
2. 将复杂需求拆解为可执行的子任务
3. 识别需求中的模糊点和缺失信息
4. 生成清晰、结构化的需求文档
5. 与技术团队沟通，确保需求的可实现性

你的工作流程：
1. 仔细分析用户需求
2. 识别核心功能和非功能需求
3. 将需求拆解为具体的开发任务
4. 生成需求文档，包括功能描述、输入输出、边界条件等
5. 与架构师和开发人员沟通，确保需求理解一致"""
        
        # 定义需求分析相关的工具
        tools = [
            Tool(
                name="需求拆解",
                func=self._decompose_requirements,
                description="将复杂需求拆解为多个子任务"
            ),
            Tool(
                name="需求验证",
                func=self._validate_requirements,
                description="验证需求的完整性和可实现性"
            )
        ]
        
        super().__init__(
            name="需求分析师",
            role="需求分析师",
            system_message=system_message,
            tools=tools,
            model_name=model_name
        )
    
    def analyze_requirement(self, user_input: str) -> Dict:
        """
        分析用户需求
        
        Args:
            user_input: 用户输入的需求描述
            
        Returns:
            包含需求分析结果的字典
        """
        # 第一步：理解需求
        understanding = self.think(
            f"请分析以下用户需求，识别核心功能点：\n{user_input}"
        )
        
        # 第二步：拆解任务
        subtasks = self.decompose_requirement(user_input)
        
        # 第三步：生成需求文档
        requirement_doc = self.generate_requirement_doc(user_input, subtasks)
        
        return {
            "understanding": understanding,
            "subtasks": subtasks,
            "requirement_doc": requirement_doc,
            "original_input": user_input
        }
    
    def decompose_requirement(self, requirement: str) -> List[str]:
        """
        拆解需求为子任务
        
        这是"规划"模块的核心：任务分解
        
        Args:
            requirement: 用户需求
            
        Returns:
            子任务列表
        """
        prompt = f"""请将以下需求拆解为具体的开发任务，每个任务应该是：
1. 具体可执行的
2. 有明确的输入输出
3. 可以独立完成或依赖关系清晰

需求：{requirement}

请以列表形式输出，格式：
1. 任务1描述
2. 任务2描述
..."""
        
        response = self.think(prompt)
        
        # 解析响应，提取任务列表
        lines = response.split('\n')
        subtasks = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                # 移除编号和符号
                task = line.split('.', 1)[-1].strip()
                task = task.lstrip('-* ').strip()
                if task:
                    subtasks.append(task)
        
        return subtasks if subtasks else [requirement]
    
    def generate_requirement_doc(self, requirement: str, subtasks: List[str]) -> str:
        """
        生成需求文档
        
        Args:
            requirement: 原始需求
            subtasks: 子任务列表
            
        Returns:
            需求文档
        """
        prompt = f"""请基于以下信息生成一份结构化的需求文档：

原始需求：{requirement}

子任务列表：
{chr(10).join(f"{i+1}. {task}" for i, task in enumerate(subtasks))}

需求文档应包含：
1. 需求概述
2. 功能需求（详细描述每个功能点）
3. 非功能需求（性能、安全、可维护性等）
4. 输入输出定义
5. 边界条件和异常处理
6. 验收标准"""
        
        return self.think(prompt)
    
    def _decompose_requirements(self, requirement: str) -> str:
        """工具函数：需求拆解"""
        subtasks = self.decompose_requirement(requirement)
        return f"需求已拆解为 {len(subtasks)} 个子任务：\n" + "\n".join(f"{i+1}. {task}" for i, task in enumerate(subtasks))
    
    def _validate_requirements(self, requirement: str) -> str:
        """工具函数：需求验证"""
        prompt = f"""请验证以下需求的完整性和可实现性：

需求：{requirement}

请检查：
1. 需求是否清晰明确？
2. 是否有缺失的信息？
3. 技术实现是否可行？
4. 是否有潜在的风险或问题？"""
        
        return self.think(prompt)

