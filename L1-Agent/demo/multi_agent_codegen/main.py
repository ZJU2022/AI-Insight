"""
主程序：多智能体协同代码生成应用的入口

这个程序展示了完整的多Agent协作流程：
1. 需求分析
2. 架构设计
3. 代码生成
4. 代码审查
5. 测试生成
6. 迭代优化
"""
import sys
import os
from config import Config
from coordinator import MultiAgentCoordinator


def main():
    """主函数"""
    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n请设置环境变量或创建.env文件，包含以下内容：")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # 创建协调器
    coordinator = MultiAgentCoordinator()
    
    # 示例需求
    example_requirements = [
        "创建一个简单的待办事项（Todo）应用，支持添加、删除、查看和标记完成功能",
        "实现一个计算器，支持加减乘除四则运算",
        "创建一个文件管理器，可以列出目录、读取文件内容"
    ]
    
    print("=" * 60)
    print("多智能体协同代码生成系统")
    print("=" * 60)
    print("\n你可以：")
    print("1. 输入自定义需求")
    print("2. 选择示例需求")
    print("3. 输入 'quit' 退出")
    print("\n示例需求：")
    for i, req in enumerate(example_requirements, 1):
        print(f"  {i}. {req}")
    
    while True:
        try:
            user_input = input("\n请输入你的需求（或输入数字选择示例）: ").strip()
            
            if not user_input:
                continue
            
            # 退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再见！")
                break
            
            # 选择示例
            if user_input.isdigit() and 1 <= int(user_input) <= len(example_requirements):
                user_input = example_requirements[int(user_input) - 1]
                print(f"\n✅ 已选择示例需求: {user_input}")
            
            # 执行工作流
            print("\n" + "=" * 60)
            result = coordinator.execute_workflow(user_input, max_iterations=2)
            
            if result["success"]:
                # 显示结果摘要
                print("\n" + "=" * 60)
                print("📊 结果摘要")
                print("=" * 60)
                print(f"✅ 生成代码文件数: {len(result['code_files'])}")
                print(f"✅ 代码审查平均分: {sum(r['review']['score'] for r in result['review_results']) / len(result['review_results']) if result['review_results'] else 0:.1f}/100")
                print(f"✅ 迭代次数: {result['iterations']}")
                
                # 保存最终报告
                report_path = os.path.join(Config.WORK_DIR, "final_report.md")
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(result['final_report'])
                print(f"\n📄 最终报告已保存到: {report_path}")
                
                # 保存任务状态
                coordinator.save_state()
            else:
                print(f"\n❌ 执行失败: {result.get('error', '未知错误')}")
            
            print("\n" + "=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

