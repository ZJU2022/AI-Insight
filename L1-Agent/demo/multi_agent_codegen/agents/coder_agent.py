"""
代码生成Agent：负责根据设计和需求编写代码

核心知识点：
1. 代码生成：基于架构设计和需求生成代码
2. 工具使用：使用代码执行工具验证代码
3. 代码优化：根据反馈优化代码质量
"""
from .base_agent import BaseAgent
from typing import Optional
from langchain.tools import Tool
from typing import Dict, Optional
import os


class CoderAgent(BaseAgent):
    """
    代码生成Agent
    
    职责：
    1. 根据架构设计编写代码
    2. 遵循编码规范
    3. 编写清晰的注释
    4. 处理异常情况
    """
    
    def __init__(self, model_name: str = None, work_dir: str = None):
        """初始化代码生成Agent"""
        system_message = """你是一位经验丰富的软件工程师，擅长：
1. 编写高质量、可维护的代码
2. 遵循最佳实践和编码规范
3. 编写清晰的注释和文档
4. 处理异常和边界情况
5. 优化代码性能和可读性

你的工作流程：
1. 理解架构设计和模块接口
2. 编写符合规范的代码
3. 添加必要的注释和文档字符串
4. 处理异常情况
5. 确保代码的可测试性
6. 根据代码审查反馈进行优化"""
        
        self.work_dir = work_dir or "workspace"
        os.makedirs(self.work_dir, exist_ok=True)
        
        tools = [
            Tool(
                name="写入文件",
                func=self._write_file,
                description="将代码写入文件"
            ),
            Tool(
                name="读取文件",
                func=self._read_file,
                description="读取已有文件内容"
            )
        ]
        
        super().__init__(
            name="开发工程师",
            role="软件工程师",
            system_message=system_message,
            tools=tools,
            model_name=model_name
        )
    
    def generate_code(
        self,
        task: str,
        architecture: str,
        module_interface: str,
        tech_stack: str
    ) -> Dict:
        """
        生成代码
        
        Args:
            task: 具体任务描述
            architecture: 架构设计
            module_interface: 模块接口定义
            tech_stack: 技术栈
            
        Returns:
            包含代码和文件路径的字典
        """
        # 生成代码
        code = self._generate_code_impl(task, architecture, module_interface, tech_stack)
        
        # 确定文件路径
        file_path = self._determine_file_path(task)
        
        # 保存代码
        full_path = os.path.join(self.work_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return {
            "code": code,
            "file_path": file_path,
            "full_path": full_path
        }
    
    def _generate_code_impl(
        self,
        task: str,
        architecture: str,
        module_interface: str,
        tech_stack: str
    ) -> str:
        """生成代码的实现"""
        prompt = f"""请基于以下信息生成完整的代码：

任务描述：{task}

架构设计：
{architecture}

模块接口定义：
{module_interface}

技术栈：
{tech_stack}

要求：
1. 代码要完整、可运行
2. 遵循Python PEP 8编码规范
3. 添加详细的文档字符串和注释
4. 处理异常情况
5. 包含必要的类型提示
6. 代码要模块化、可复用

请直接输出代码，不要包含其他说明文字。"""
        
        response = self.think(prompt)
        
        # 提取代码部分（移除可能的markdown代码块标记）
        code = response
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
        
        return code.strip()
    
    def _determine_file_path(self, task: str) -> str:
        """根据任务确定文件路径"""
        # 简单的启发式方法：从任务中提取文件名
        task_lower = task.lower()
        
        if "main" in task_lower or "入口" in task:
            return "main.py"
        elif "test" in task_lower or "测试" in task:
            return "test.py"
        elif "utils" in task_lower or "工具" in task:
            return "utils.py"
        else:
            # 默认文件名
            return "module.py"
    
    def improve_code(self, code: str, feedback: str) -> str:
        """
        根据反馈改进代码
        
        Args:
            code: 原始代码
            feedback: 审查反馈
            
        Returns:
            改进后的代码
        """
        prompt = f"""请根据以下反馈改进代码：

原始代码：
```python
{code}
```

审查反馈：
{feedback}

请：
1. 修复所有指出的问题
2. 保持代码的原有功能
3. 改进代码质量和可读性
4. 添加必要的改进

请直接输出改进后的代码。"""
        
        response = self.think(prompt)
        
        # 提取代码部分
        improved_code = response
        if "```python" in improved_code:
            improved_code = improved_code.split("```python")[1].split("```")[0]
        elif "```" in improved_code:
            improved_code = improved_code.split("```")[1].split("```")[0]
        
        return improved_code.strip()
    
    def _write_file(self, file_path: str) -> str:
        """工具函数：写入文件"""
        # 这个工具主要用于Agent的工具调用
        return f"文件写入功能已集成到generate_code方法中"
    
    def _read_file(self, file_path: str) -> str:
        """工具函数：读取文件"""
        full_path = os.path.join(self.work_dir, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"文件不存在: {file_path}"

