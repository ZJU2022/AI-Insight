"""
测试生成Agent：负责生成测试代码

核心知识点：
1. 测试用例设计：设计全面的测试用例
2. 测试代码生成：生成单元测试、集成测试
3. 测试执行：执行测试并分析结果
"""
from .base_agent import BaseAgent
from langchain.tools import Tool
from typing import Dict, List, Optional
import os
import subprocess


class TesterAgent(BaseAgent):
    """
    测试生成Agent
    
    职责：
    1. 生成测试用例
    2. 编写测试代码
    3. 执行测试
    4. 分析测试结果
    """
    
    def __init__(self, model_name: str = None, work_dir: str = None):
        """初始化测试生成Agent"""
        system_message = """你是一位专业的测试工程师，擅长：
1. 设计全面的测试用例（正常情况、边界情况、异常情况）
2. 编写高质量的测试代码
3. 使用测试框架（如pytest、unittest）
4. 分析测试结果和覆盖率
5. 识别测试中的问题

你的测试策略：
1. 单元测试：测试每个函数和类
2. 集成测试：测试模块间的交互
3. 边界测试：测试边界条件和极端情况
4. 异常测试：测试错误处理
5. 性能测试：测试性能关键路径

你的工作流程：
1. 分析代码，理解功能
2. 设计测试用例（正常、边界、异常）
3. 编写测试代码
4. 执行测试
5. 分析结果，提供改进建议"""
        
        self.work_dir = work_dir or "workspace"
        os.makedirs(self.work_dir, exist_ok=True)
        
        tools = [
            Tool(
                name="执行测试",
                func=self._run_tests,
                description="执行测试代码"
            ),
            Tool(
                name="分析覆盖率",
                func=self._analyze_coverage,
                description="分析测试覆盖率"
            )
        ]
        
        super().__init__(
            name="测试工程师",
            role="测试工程师",
            system_message=system_message,
            tools=tools,
            model_name=model_name
        )
    
    def generate_tests(self, code: str, requirements: Optional[str] = None) -> Dict:
        """
        生成测试代码
        
        Args:
            code: 要测试的代码
            requirements: 需求文档（可选）
            
        Returns:
            包含测试代码和测试计划的字典
        """
        # 设计测试用例
        test_cases = self._design_test_cases(code, requirements)
        
        # 生成测试代码
        test_code = self._generate_test_code(code, test_cases)
        
        # 保存测试文件
        test_file_path = os.path.join(self.work_dir, "test_generated.py")
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        return {
            "test_cases": test_cases,
            "test_code": test_code,
            "test_file_path": test_file_path
        }
    
    def _design_test_cases(self, code: str, requirements: Optional[str] = None) -> str:
        """设计测试用例"""
        prompt = f"""请为以下代码设计全面的测试用例：

代码：
```python
{code}
```

{f"需求文档：\n{requirements}" if requirements else ""}

请设计以下类型的测试用例：
1. **正常情况测试**：测试正常的功能流程
2. **边界情况测试**：测试边界值和极端情况
3. **异常情况测试**：测试错误处理和异常情况
4. **性能测试**：测试性能关键路径（如需要）

对于每个测试用例，请说明：
- 测试目的
- 输入数据
- 预期输出
- 测试步骤"""
        
        return self.think(prompt)
    
    def _generate_test_code(self, code: str, test_cases: str) -> str:
        """生成测试代码"""
        prompt = f"""请基于以下信息生成完整的pytest测试代码：

要测试的代码：
```python
{code}
```

测试用例设计：
{test_cases}

要求：
1. 使用pytest框架
2. 测试代码要完整、可运行
3. 使用清晰的测试函数命名（test_xxx格式）
4. 使用断言验证结果
5. 使用fixture管理测试数据（如需要）
6. 添加必要的注释

请直接输出测试代码，不要包含其他说明文字。"""
        
        response = self.think(prompt)
        
        # 提取代码部分
        test_code = response
        if "```python" in test_code:
            test_code = test_code.split("```python")[1].split("```")[0]
        elif "```" in test_code:
            test_code = test_code.split("```")[1].split("```")[0]
        
        return test_code.strip()
    
    def run_tests(self, test_file_path: str) -> Dict:
        """
        执行测试
        
        Args:
            test_file_path: 测试文件路径
            
        Returns:
            测试结果
        """
        try:
            # 执行pytest
            result = subprocess.run(
                ["pytest", test_file_path, "-v"],
                capture_output=True,
                text=True,
                cwd=self.work_dir,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "测试执行超时",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def _run_tests(self, test_file: str) -> str:
        """工具函数：执行测试"""
        result = self.run_tests(test_file)
        if result["success"]:
            return f"测试通过！\n{result['stdout']}"
        else:
            return f"测试失败！\n{result['stderr']}\n{result['stdout']}"
    
    def _analyze_coverage(self, test_file: str) -> str:
        """工具函数：分析覆盖率"""
        try:
            # 执行pytest with coverage
            result = subprocess.run(
                ["pytest", test_file, "--cov", ".", "--cov-report", "term"],
                capture_output=True,
                text=True,
                cwd=self.work_dir,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            return f"覆盖率分析失败: {str(e)}"

