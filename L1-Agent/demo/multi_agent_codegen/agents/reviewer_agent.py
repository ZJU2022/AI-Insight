"""
代码审查Agent：负责审查代码质量

核心知识点：
1. 代码审查：检查代码质量、规范、安全性
2. 反馈生成：提供具体的改进建议
3. 质量评估：评估代码的整体质量
"""
from .base_agent import BaseAgent
from langchain.tools import Tool
from typing import Dict, List, Optional


class ReviewerAgent(BaseAgent):
    """
    代码审查Agent
    
    职责：
    1. 审查代码质量
    2. 检查编码规范
    3. 识别潜在问题
    4. 提供改进建议
    """
    
    def __init__(self, model_name: str = None):
        """初始化代码审查Agent"""
        system_message = """你是一位严格的代码审查专家，擅长：
1. 发现代码中的bug和潜在问题
2. 检查代码是否符合编码规范
3. 评估代码的可读性和可维护性
4. 识别性能问题和安全隐患
5. 提供具体、可操作的改进建议

你的审查标准：
1. 代码正确性：逻辑是否正确，是否有bug
2. 编码规范：是否符合PEP 8等规范
3. 代码质量：可读性、可维护性、可扩展性
4. 性能优化：是否有性能问题
5. 安全性：是否有安全隐患
6. 测试覆盖：是否有足够的测试

你的工作流程：
1. 仔细阅读代码
2. 检查各个方面的问题
3. 按优先级列出问题
4. 提供具体的改进建议
5. 给出整体质量评估"""
        
        tools = [
            Tool(
                name="代码审查",
                func=self._review_code,
                description="审查代码质量"
            ),
            Tool(
                name="规范检查",
                func=self._check_style,
                description="检查代码规范"
            )
        ]
        
        super().__init__(
            name="代码审查员",
            role="代码审查专家",
            system_message=system_message,
            tools=tools,
            model_name=model_name
        )
    
    def review_code(self, code: str, requirements: Optional[str] = None) -> Dict:
        """
        审查代码
        
        Args:
            code: 要审查的代码
            requirements: 需求文档（可选）
            
        Returns:
            包含审查结果的字典
        """
        # 全面审查
        review_result = self._comprehensive_review(code, requirements)
        
        # 提取问题列表
        issues = self._extract_issues(review_result)
        
        # 生成改进建议
        suggestions = self._generate_suggestions(code, issues)
        
        # 质量评分
        score = self._calculate_score(issues)
        
        return {
            "review_result": review_result,
            "issues": issues,
            "suggestions": suggestions,
            "score": score,
            "code": code
        }
    
    def _comprehensive_review(self, code: str, requirements: Optional[str] = None) -> str:
        """全面审查代码"""
        prompt = f"""请对以下代码进行全面审查：

代码：
```python
{code}
```

{f"需求文档：\n{requirements}" if requirements else ""}

请从以下方面审查：
1. **正确性**：逻辑是否正确，是否有bug
2. **编码规范**：是否符合PEP 8等规范
3. **代码质量**：可读性、可维护性、可扩展性
4. **性能**：是否有性能问题，可以如何优化
5. **安全性**：是否有安全隐患
6. **文档**：注释和文档字符串是否充分
7. **测试**：是否考虑了测试
8. **需求符合度**：是否满足需求（如果提供了需求文档）

请详细列出发现的问题，按严重程度分类（严重、中等、轻微）。"""
        
        return self.think(prompt)
    
    def _extract_issues(self, review_result: str) -> List[Dict]:
        """从审查结果中提取问题列表"""
        # 简单的解析逻辑，实际可以使用更复杂的NLP方法
        issues = []
        lines = review_result.split('\n')
        
        current_severity = "中等"
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测严重程度标记
            if "严重" in line or "严重问题" in line:
                current_severity = "严重"
            elif "轻微" in line or "建议" in line:
                current_severity = "轻微"
            elif "中等" in line:
                current_severity = "中等"
            
            # 提取问题描述
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '*')) or \
               any(keyword in line for keyword in ['问题', '错误', 'bug', '建议', '改进']):
                issues.append({
                    "severity": current_severity,
                    "description": line
                })
        
        return issues if issues else [{"severity": "中等", "description": review_result}]
    
    def _generate_suggestions(self, code: str, issues: List[Dict]) -> str:
        """生成改进建议"""
        issues_text = "\n".join(f"{i+1}. [{issue['severity']}] {issue['description']}" 
                               for i, issue in enumerate(issues))
        
        prompt = f"""基于以下发现的问题，请提供具体的改进建议：

代码：
```python
{code}
```

发现的问题：
{issues_text}

请为每个问题提供：
1. 具体的改进方案
2. 改进后的代码示例（如果适用）
3. 改进的优先级"""
        
        return self.think(prompt)
    
    def _calculate_score(self, issues: List[Dict]) -> int:
        """计算代码质量评分（0-100）"""
        if not issues:
            return 100
        
        # 根据问题严重程度扣分
        score = 100
        for issue in issues:
            if issue['severity'] == "严重":
                score -= 10
            elif issue['severity'] == "中等":
                score -= 5
            else:
                score -= 2
        
        return max(0, score)
    
    def _review_code(self, code: str) -> str:
        """工具函数：代码审查"""
        result = self.review_code(code)
        return f"审查完成。发现 {len(result['issues'])} 个问题，质量评分: {result['score']}/100"
    
    def _check_style(self, code: str) -> str:
        """工具函数：规范检查"""
        prompt = f"""请检查以下代码是否符合Python编码规范（PEP 8）：

代码：
```python
{code}
```

请检查：
1. 命名规范（变量、函数、类名）
2. 缩进和空格
3. 行长度
4. 导入顺序
5. 文档字符串格式"""
        
        return self.think(prompt)

