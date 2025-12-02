"""
向量存储模块：负责将文档向量化并存储到向量数据库

核心知识点：
1. Embedding向量化：将文本转换为高维向量（语义的数学表达）
2. 向量数据库：高效存储和检索向量数据
3. 相似度计算：余弦相似度、欧氏距离等
"""
import os
from typing import List, Optional
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.base import VectorStore


class VectorStoreManager:
    """向量存储管理器：负责文档向量化和向量数据库管理"""
    
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        """
        初始化向量存储管理器
        
        Args:
            embedding_model: Embedding模型名称
        """
        # 初始化OpenAI Embedding模型
        # 这个模型会将文本转换为1536维的向量
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store: Optional[VectorStore] = None
    
    def create_vector_store(self, documents: List[Document]) -> VectorStore:
        """
        创建向量存储并添加文档
        
        Args:
            documents: 文档列表
            
        Returns:
            向量存储对象
        """
        print("🔄 开始向量化文档...")
        
        # 使用FAISS创建向量存储
        # FAISS会自动调用embedding模型将文档转换为向量
        # 并建立索引以便快速检索
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print(f"✅ 成功创建向量存储，包含 {len(documents)} 个文档块")
        return self.vector_store
    
    def save_vector_store(self, save_path: str):
        """
        保存向量存储到磁盘
        
        Args:
            save_path: 保存路径
        """
        if self.vector_store is None:
            raise ValueError("向量存储未初始化，请先创建向量存储")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 保存向量存储
        self.vector_store.save_local(save_path)
        print(f"✅ 向量存储已保存到: {save_path}")
    
    def load_vector_store(self, load_path: str) -> VectorStore:
        """
        从磁盘加载向量存储
        
        Args:
            load_path: 加载路径
            
        Returns:
            向量存储对象
        """
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"向量存储不存在: {load_path}")
        
        # 加载向量存储
        self.vector_store = FAISS.load_local(
            load_path=load_path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True  # FAISS需要此参数
        )
        
        print(f"✅ 成功加载向量存储: {load_path}")
        return self.vector_store
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """
        相似度搜索：根据查询文本找到最相关的文档
        
        Args:
            query: 查询文本
            k: 返回最相关的k个文档
            
        Returns:
            最相关的文档列表
        """
        if self.vector_store is None:
            raise ValueError("向量存储未初始化，请先创建或加载向量存储")
        
        # 执行相似度搜索
        # FAISS会：
        # 1. 将查询文本转换为向量
        # 2. 计算查询向量与所有文档向量的相似度（默认使用余弦相似度）
        # 3. 返回最相似的k个文档
        results = self.vector_store.similarity_search(query, k=k)
        
        return results
    
    def similarity_search_with_score(self, query: str, k: int = 3) -> List[tuple]:
        """
        相似度搜索并返回相似度分数
        
        Args:
            query: 查询文本
            k: 返回最相关的k个文档
            
        Returns:
            (文档, 相似度分数) 元组列表
        """
        if self.vector_store is None:
            raise ValueError("向量存储未初始化，请先创建或加载向量存储")
        
        # 返回文档和相似度分数
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        return results


def demo_vector_store():
    """演示向量存储功能"""
    print("=" * 60)
    print("向量存储模块演示")
    print("=" * 60)
    
    from document_loader import DocumentLoader
    
    # 1. 加载文档
    loader = DocumentLoader(chunk_size=500, chunk_overlap=75)
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_dir, "hr_policy.txt")
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    documents = loader.load_and_split(file_path)
    
    # 2. 创建向量存储
    vector_manager = VectorStoreManager()
    vector_store = vector_manager.create_vector_store(documents)
    
    # 3. 测试相似度搜索
    test_queries = [
        "年假如何申请？",
        "产假有多少天？",
        "工资什么时候发放？"
    ]
    
    print("\n" + "=" * 60)
    print("相似度搜索测试")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 查询: {query}")
        results = vector_manager.similarity_search_with_score(query, k=2)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n  结果 {i} (相似度: {score:.4f}):")
            print(f"  {doc.page_content[:200]}...")
    
    # 4. 保存向量存储
    save_path = os.path.join(os.path.dirname(__file__), "storage", "vectorstore")
    vector_manager.save_vector_store(save_path)
    
    print("\n✅ 演示完成！")


if __name__ == "__main__":
    demo_vector_store()

