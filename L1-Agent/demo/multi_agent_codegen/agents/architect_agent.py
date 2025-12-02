"""
架构设计Agent：负责系统架构设计和技术选型

核心知识点：
1. 架构规划：设计系统整体架构
2. 技术选型：选择合适的工具和框架
3. 模块划分：将系统拆分为可开发的模块
"""
from .base_agent import BaseAgent
from langchain.tools import Tool
from typing import Dict, List


class ArchitectAgent(BaseAgent):
    """
    架构设计Agent
    
    职责：
    1. 设计系统架构
    2. 进行技术选型
    3. 定义模块接口
    4. 制定开发规范
    """
    
    def __init__(self, model_name: str = None):
        """初始化架构设计Agent"""
        system_message = """你是一位资深的软件架构师，擅长：
1. 设计清晰、可扩展的系统架构
2. 进行合理的技术选型
3. 定义模块间的接口和依赖关系
4. 制定代码规范和开发流程
5. 平衡性能、可维护性和开发效率

你的工作流程：
1. 分析需求文档，理解系统功能
2. 设计整体架构（分层架构、模块划分）
3. 选择合适的技术栈和工具
4. 定义模块接口和数据流
5. 制定开发规范和最佳实践
6. 与开发团队沟通，确保架构的可实现性"""
        
        tools = [
            Tool(
                name="架构设计",
                func=self._design_architecture,
                description="设计系统整体架构"
            ),
            Tool(
                name="技术选型",
                func=self._select_technology,
                description="选择合适的技术栈"
            )
        ]
        
        super().__init__(
            name="架构师",
            role="软件架构师",
            system_message=system_message,
            tools=tools,
            model_name=model_name
        )
    
    def design_system(self, requirement_doc: str, subtasks: List[str]) -> Dict:
        """
        设计系统架构
        
        Args:
            requirement_doc: 需求文档
            subtasks: 子任务列表
            
        Returns:
            包含架构设计结果的字典
        """
        # 第一步：分析需求
        analysis = self.think(
            f"请分析以下需求文档，识别系统的核心模块和技术要求：\n{requirement_doc}"
        )
        
        # 第二步：设计架构
        architecture = self.create_architecture_design(requirement_doc, subtasks)
        
        # 第三步：技术选型
        tech_stack = self.select_tech_stack(requirement_doc)
        
        # 第四步：定义模块接口
        module_interfaces = self.define_module_interfaces(subtasks)
        
        return {
            "analysis": analysis,
            "architecture": architecture,
            "tech_stack": tech_stack,
            "module_interfaces": module_interfaces
        }
    
    def create_architecture_design(self, requirement_doc: str, subtasks: List[str]) -> str:
        """
        创建架构设计文档
        
        Args:
            requirement_doc: 需求文档
            subtasks: 子任务列表
            
        Returns:
            架构设计文档
        """
        prompt = f"""请基于以下需求设计系统架构：

需求文档：
{requirement_doc}

子任务列表：
{chr(10).join(f"{i+1}. {task}" for i, task in enumerate(subtasks))}

请提供：
1. 整体架构图（文字描述）
2. 分层设计（如：表现层、业务层、数据层）
3. 模块划分和职责
4. 模块间的依赖关系
5. 数据流设计"""
        
        return self.think(prompt)
    
    def select_tech_stack(self, requirement_doc: str) -> str:
        """
        选择技术栈
        
        Args:
            requirement_doc: 需求文档
            
        Returns:
            技术选型说明
        """
        prompt = f"""请基于以下需求进行技术选型：

需求文档：
{requirement_doc}

请为以下方面选择合适的技术：
1. 编程语言和框架
2. 数据库（如需要）
3. 第三方库和工具
4. 开发工具和环境

请说明选择理由，并考虑：
- 项目规模和复杂度
- 团队技术栈
- 性能和可维护性
- 社区支持和文档"""
        
        return self.think(prompt)
    
    def define_module_interfaces(self, subtasks: List[str]) -> str:
        """
        定义模块接口
        
        Args:
            subtasks: 子任务列表
            
        Returns:
            模块接口定义
        """
        prompt = f"""请基于以下子任务定义模块接口：

子任务列表：
{chr(10).join(f"{i+1}. {task}" for i, task in enumerate(subtasks))}

请为每个模块定义：
1. 模块名称和职责
2. 输入参数（类型、说明）
3. 输出结果（类型、说明）
4. 异常处理
5. 模块间的调用关系"""
        
        return self.think(prompt)
    
    def _design_architecture(self, requirement: str) -> str:
        """工具函数：架构设计"""
        return self.create_architecture_design(requirement, [])
    
    def _select_technology(self, requirement: str) -> str:
        """工具函数：技术选型"""
        return self.select_tech_stack(requirement)

