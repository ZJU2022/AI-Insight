"""
主程序：HR制度问答系统的入口

这个程序展示了完整的RAG工作流程：
1. 文档加载和分块
2. 向量化和存储
3. 检索和生成
"""
import os
import sys
from config import Config
from document_loader import DocumentLoader
from vector_store import VectorStoreManager
from rag_chain import RAGChain


def build_knowledge_base():
    """构建知识库：加载文档、向量化、存储"""
    print("=" * 60)
    print("步骤1: 构建知识库")
    print("=" * 60)
    
    # 1. 加载文档
    loader = DocumentLoader(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    
    # 查找数据目录中的所有文档
    data_dir = Config.DATA_DIR
    documents = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith(('.txt', '.pdf', '.md')):
            file_path = os.path.join(data_dir, filename)
            print(f"\n📄 处理文件: {filename}")
            docs = loader.load_and_split(file_path)
            documents.extend(docs)
    
    if not documents:
        print("❌ 未找到任何文档，请确保data目录下有文档文件")
        return None
    
    # 2. 创建向量存储
    print("\n" + "=" * 60)
    print("步骤2: 向量化文档")
    print("=" * 60)
    
    vector_manager = VectorStoreManager(embedding_model=Config.EMBEDDING_MODEL)
    vector_store = vector_manager.create_vector_store(documents)
    
    # 3. 保存向量存储
    print("\n" + "=" * 60)
    print("步骤3: 保存向量存储")
    print("=" * 60)
    
    os.makedirs(os.path.dirname(Config.VECTOR_STORE_PATH), exist_ok=True)
    vector_manager.save_vector_store(Config.VECTOR_STORE_PATH)
    
    print("\n✅ 知识库构建完成！")
    return vector_manager


def load_knowledge_base():
    """加载已存在的知识库"""
    print("=" * 60)
    print("加载知识库")
    print("=" * 60)
    
    vector_manager = VectorStoreManager(embedding_model=Config.EMBEDDING_MODEL)
    
    try:
        vector_manager.load_vector_store(Config.VECTOR_STORE_PATH)
        print("✅ 知识库加载成功！")
        return vector_manager
    except FileNotFoundError:
        print("❌ 知识库不存在，正在构建...")
        return build_knowledge_base()


def interactive_qa(vector_manager: VectorStoreManager):
    """交互式问答"""
    print("\n" + "=" * 60)
    print("HR制度智能问答系统")
    print("=" * 60)
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'rebuild' 重新构建知识库")
    print("-" * 60)
    
    # 创建RAG链
    rag = RAGChain(vector_manager, model_name=Config.OPENAI_MODEL)
    
    while True:
        try:
            # 获取用户输入
            question = input("\n❓ 请输入您的问题: ").strip()
            
            if not question:
                continue
            
            # 退出命令
            if question.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再见！")
                break
            
            # 重建知识库命令
            if question.lower() == 'rebuild':
                vector_manager = build_knowledge_base()
                if vector_manager:
                    rag = RAGChain(vector_manager, model_name=Config.OPENAI_MODEL)
                continue
            
            # 执行RAG查询
            print("\n" + "-" * 60)
            result = rag.invoke(question, k=Config.TOP_K)
            
            # 显示结果
            print(f"\n📝 回答:\n{result['answer']}")
            
            # 显示参考文档
            print(f"\n📚 参考文档 ({len(result['retrieved_docs'])} 条):")
            for i, doc in enumerate(result['retrieved_docs'], 1):
                source = doc.metadata.get('source', 'unknown')
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. [{source}] {preview}...")
            
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


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
    
    # 加载或构建知识库
    vector_manager = load_knowledge_base()
    
    if vector_manager is None:
        print("❌ 无法加载或构建知识库")
        sys.exit(1)
    
    # 启动交互式问答
    interactive_qa(vector_manager)


if __name__ == "__main__":
    main()

