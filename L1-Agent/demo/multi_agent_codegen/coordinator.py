"""
多Agent协调器：协调多个Agent协同完成代码生成任务

核心知识点：
1. 多Agent协作：协调不同角色的Agent
2. 工作流管理：管理任务执行流程
3. 状态管理：跟踪任务状态和Agent间的通信
4. 迭代优化：根据反馈进行迭代改进
"""
from typing import Dict, List, Optional
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from agents.coder_agent import CoderAgent
from agents.reviewer_agent import ReviewerAgent
from agents.tester_agent import TesterAgent
import config
import os
import json
from datetime import datetime


class MultiAgentCoordinator:
    """
    多Agent协调器
    
    职责：
    1. 管理多个Agent的协作
    2. 控制工作流程
    3. 管理任务状态
    4. 处理Agent间的通信
    """
    
    def __init__(self):
        """初始化协调器"""
        # 创建各个Agent
        self.requirement_agent = RequirementAgent()
        self.architect_agent = ArchitectAgent()
        self.coder_agent = CoderAgent(work_dir=config.Config.WORK_DIR)
        self.reviewer_agent = ReviewerAgent()
        self.tester_agent = TesterAgent(work_dir=config.Config.WORK_DIR)
        
        # 任务状态
        self.task_state = {
            "status": "idle",  # idle, analyzing, designing, coding, reviewing, testing, completed
            "current_step": None,
            "requirements": None,
            "architecture": None,
            "code_files": [],
            "review_results": [],
            "test_results": [],
            "iterations": 0
        }
        
        # 工作流定义
        self.workflow = [
            "requirement_analysis",  # 需求分析
            "architecture_design",   # 架构设计
            "code_generation",       # 代码生成
            "code_review",           # 代码审查
            "test_generation",      # 测试生成
            "iteration"              # 迭代优化（可选）
        ]
    
    def execute_workflow(self, user_input: str, max_iterations: int = 2) -> Dict:
        """
        执行完整的工作流
        
        Args:
            user_input: 用户需求
            max_iterations: 最大迭代次数
            
        Returns:
            完整的工作流结果
        """
        print("=" * 60)
        print("🚀 开始多Agent协同代码生成")
        print("=" * 60)
        
        try:
            # 步骤1: 需求分析
            print("\n📋 步骤1: 需求分析")
            print("-" * 60)
            requirements = self._analyze_requirements(user_input)
            self.task_state["requirements"] = requirements
            
            # 步骤2: 架构设计
            print("\n🏗️  步骤2: 架构设计")
            print("-" * 60)
            architecture = self._design_architecture(requirements)
            self.task_state["architecture"] = architecture
            
            # 步骤3: 代码生成
            print("\n💻 步骤3: 代码生成")
            print("-" * 60)
            code_results = self._generate_code(requirements, architecture)
            self.task_state["code_files"] = code_results
            
            # 步骤4: 代码审查
            print("\n🔍 步骤4: 代码审查")
            print("-" * 60)
            review_results = self._review_code(code_results)
            self.task_state["review_results"] = review_results
            
            # 步骤5: 测试生成
            print("\n🧪 步骤5: 测试生成")
            print("-" * 60)
            test_results = self._generate_tests(code_results, requirements)
            self.task_state["test_results"] = test_results
            
            # 步骤6: 迭代优化（如果需要）
            iteration_count = 0
            while iteration_count < max_iterations:
                # 检查是否需要迭代
                needs_iteration = self._check_if_needs_iteration(review_results, test_results)
                
                if not needs_iteration:
                    break
                
                iteration_count += 1
                print(f"\n🔄 迭代 {iteration_count}: 优化代码")
                print("-" * 60)
                
                # 改进代码
                improved_results = self._improve_code(
                    code_results,
                    review_results,
                    test_results
                )
                code_results = improved_results
                self.task_state["code_files"] = code_results
                
                # 重新审查和测试
                review_results = self._review_code(code_results)
                test_results = self._generate_tests(code_results, requirements)
            
            self.task_state["iterations"] = iteration_count
            self.task_state["status"] = "completed"
            
            # 生成最终报告
            final_report = self._generate_final_report()
            
            print("\n" + "=" * 60)
            print("✅ 工作流执行完成！")
            print("=" * 60)
            
            return {
                "success": True,
                "requirements": requirements,
                "architecture": architecture,
                "code_files": code_results,
                "review_results": review_results,
                "test_results": test_results,
                "final_report": final_report,
                "iterations": iteration_count
            }
            
        except Exception as e:
            self.task_state["status"] = "error"
            print(f"\n❌ 执行出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_requirements(self, user_input: str) -> Dict:
        """需求分析阶段"""
        self.task_state["status"] = "analyzing"
        self.task_state["current_step"] = "requirement_analysis"
        
        result = self.requirement_agent.analyze_requirement(user_input)
        
        print(f"✅ 需求理解: {result['understanding'][:200]}...")
        print(f"✅ 拆解为 {len(result['subtasks'])} 个子任务")
        
        return result
    
    def _design_architecture(self, requirements: Dict) -> Dict:
        """架构设计阶段"""
        self.task_state["status"] = "designing"
        self.task_state["current_step"] = "architecture_design"
        
        result = self.architect_agent.design_system(
            requirements["requirement_doc"],
            requirements["subtasks"]
        )
        
        print(f"✅ 架构设计完成")
        print(f"✅ 技术栈: {result['tech_stack'][:200]}...")
        
        return result
    
    def _generate_code(self, requirements: Dict, architecture: Dict) -> List[Dict]:
        """代码生成阶段"""
        self.task_state["status"] = "coding"
        self.task_state["current_step"] = "code_generation"
        
        code_results = []
        
        # 为每个子任务生成代码
        for i, subtask in enumerate(requirements["subtasks"], 1):
            print(f"\n  生成代码 {i}/{len(requirements['subtasks'])}: {subtask[:50]}...")
            
            result = self.coder_agent.generate_code(
                task=subtask,
                architecture=architecture["architecture"],
                module_interface=architecture["module_interfaces"],
                tech_stack=architecture["tech_stack"]
            )
            
            code_results.append(result)
            print(f"  ✅ 代码已保存到: {result['file_path']}")
        
        return code_results
    
    def _review_code(self, code_results: List[Dict]) -> List[Dict]:
        """代码审查阶段"""
        self.task_state["status"] = "reviewing"
        self.task_state["current_step"] = "code_review"
        
        review_results = []
        
        for code_result in code_results:
            print(f"\n  审查代码: {code_result['file_path']}")
            
            review = self.reviewer_agent.review_code(code_result["code"])
            review_results.append({
                "file_path": code_result["file_path"],
                "review": review
            })
            
            print(f"  ✅ 审查完成，质量评分: {review['score']}/100")
            print(f"  ⚠️  发现 {len(review['issues'])} 个问题")
        
        return review_results
    
    def _generate_tests(self, code_results: List[Dict], requirements: Dict) -> List[Dict]:
        """测试生成阶段"""
        self.task_state["status"] = "testing"
        self.task_state["current_step"] = "test_generation"
        
        test_results = []
        
        for code_result in code_results:
            print(f"\n  生成测试: {code_result['file_path']}")
            
            test_result = self.tester_agent.generate_tests(
                code_result["code"],
                requirements.get("requirement_doc")
            )
            
            test_results.append({
                "file_path": code_result["file_path"],
                "test_result": test_result
            })
            
            # 执行测试
            if os.path.exists(test_result["test_file_path"]):
                print(f"  ✅ 测试代码已生成")
                test_execution = self.tester_agent.run_tests(test_result["test_file_path"])
                test_results[-1]["execution"] = test_execution
                
                if test_execution["success"]:
                    print(f"  ✅ 测试通过")
                else:
                    print(f"  ⚠️  测试失败: {test_execution['stderr'][:100]}")
        
        return test_results
    
    def _check_if_needs_iteration(self, review_results: List[Dict], test_results: List[Dict]) -> bool:
        """检查是否需要迭代优化"""
        # 如果审查评分低于80或测试失败，需要迭代
        for review in review_results:
            if review["review"]["score"] < 80:
                return True
        
        for test in test_results:
            if "execution" in test and not test["execution"]["success"]:
                return True
        
        return False
    
    def _improve_code(self, code_results: List[Dict], review_results: List[Dict], test_results: List[Dict]) -> List[Dict]:
        """改进代码"""
        improved_results = []
        
        for i, code_result in enumerate(code_results):
            # 获取对应的审查结果
            review = review_results[i] if i < len(review_results) else None
            
            if review and review["review"]["score"] < 80:
                print(f"  改进代码: {code_result['file_path']}")
                
                # 生成改进建议
                feedback = review["review"]["suggestions"]
                
                # 改进代码
                improved_code = self.coder_agent.improve_code(
                    code_result["code"],
                    feedback
                )
                
                # 保存改进后的代码
                code_result["code"] = improved_code
                with open(code_result["full_path"], 'w', encoding='utf-8') as f:
                    f.write(improved_code)
                
                print(f"  ✅ 代码已改进")
            
            improved_results.append(code_result)
        
        return improved_results
    
    def _generate_final_report(self) -> str:
        """生成最终报告"""
        report = f"""
# 代码生成项目报告

## 项目概览
- 状态: {self.task_state['status']}
- 迭代次数: {self.task_state['iterations']}
- 生成文件数: {len(self.task_state['code_files'])}

## 需求分析
{self.task_state['requirements']['requirement_doc'][:500] if self.task_state['requirements'] else 'N/A'}

## 架构设计
{self.task_state['architecture']['architecture'][:500] if self.task_state['architecture'] else 'N/A'}

## 生成的代码文件
"""
        for code_file in self.task_state['code_files']:
            report += f"- {code_file['file_path']}\n"
        
        report += "\n## 代码审查结果\n"
        for review in self.task_state['review_results']:
            report += f"- {review['file_path']}: 评分 {review['review']['score']}/100\n"
        
        report += "\n## 测试结果\n"
        for test in self.task_state['test_results']:
            if "execution" in test:
                status = "通过" if test["execution"]["success"] else "失败"
                report += f"- {test['file_path']}: {status}\n"
        
        return report
    
    def save_state(self, file_path: str = None):
        """保存任务状态"""
        if file_path is None:
            file_path = os.path.join(config.Config.WORK_DIR, "task_state.json")
        
        # 转换不可序列化的对象
        state = {
            "status": self.task_state["status"],
            "current_step": self.task_state["current_step"],
            "iterations": self.task_state["iterations"],
            "code_files_count": len(self.task_state["code_files"]),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 任务状态已保存到: {file_path}")

