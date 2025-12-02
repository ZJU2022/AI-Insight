"""
RAG链模块：实现完整的检索增强生成流程

核心知识点：
1. RAG流程：检索(Retrieval) + 生成(Generation)
2. Prompt工程：设计有效的提示词模板
3. 上下文增强：将检索结果注入到生成模型的上下文中
"""
import os
from typing import List
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from vector_store import VectorStoreManager


class RAGChain:
    """RAG链：实现检索增强生成"""
    
    def __init__(self, vector_store_manager: VectorStoreManager, model_name: str = "gpt-3.5-turbo"):
        """
        初始化RAG链
        
        Args:
            vector_store_manager: 向量存储管理器
            model_name: 使用的LLM模型名称
        """
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,  # 温度参数，控制生成的随机性
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 定义Prompt模板
        # 这是RAG的核心：将检索到的文档作为上下文注入到Prompt中
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的HR助手，负责回答员工关于公司HR制度的问题。

请严格基于以下提供的公司制度文档内容回答问题。如果文档中没有相关信息，请明确说明"暂无相关规定"。

回答要求：
1. 答案必须准确、完整
2. 必须标注信息来源（如"根据《员工手册》第X章第X节"）
3. 使用简洁、友好的语言
4. 如果涉及具体数字或流程，请详细说明

公司制度文档内容：
{context}"""),
            ("human", "{question}")
        ])
    
    def format_docs(self, docs: List[Document]) -> str:
        """
        格式化检索到的文档为字符串
        
        Args:
            docs: 文档列表
            
        Returns:
            格式化后的文档字符串
        """
        formatted_docs = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'unknown')
            chunk_id = doc.metadata.get('chunk_id', 'unknown')
            content = doc.page_content
            
            formatted_docs.append(
                f"[文档片段 {i} - 来源: {source}, ID: {chunk_id}]\n{content}\n"
            )
        
        return "\n".join(formatted_docs)
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            k: 返回的文档数量
            
        Returns:
            相关文档列表
        """
        return self.vector_store_manager.similarity_search(query, k=k)
    
    def generate(self, query: str, context: str) -> str:
        """
        基于上下文生成回答
        
        Args:
            query: 用户问题
            context: 检索到的文档上下文
            
        Returns:
            生成的回答
        """
        # 构建完整的Prompt
        messages = self.prompt_template.format_messages(
            context=context,
            question=query
        )
        
        # 调用LLM生成回答
        response = self.llm.invoke(messages)
        return response.content
    
    def invoke(self, query: str, k: int = 3) -> dict:
        """
        执行完整的RAG流程
        
        Args:
            query: 用户问题
            k: 检索的文档数量
            
        Returns:
            包含问题、检索结果、回答的字典
        """
        # 步骤1: 检索相关文档
        print(f"🔍 正在检索相关文档...")
        retrieved_docs = self.retrieve(query, k=k)
        
        # 步骤2: 格式化文档为上下文
        context = self.format_docs(retrieved_docs)
        
        # 步骤3: 生成回答
        print(f"🤖 正在生成回答...")
        answer = self.generate(query, context)
        
        return {
            "question": query,
            "retrieved_docs": retrieved_docs,
            "context": context,
            "answer": answer
        }
    
    def create_chain(self, k: int = 3):
        """
        创建LangChain风格的RAG链（使用链式调用）
        
        Args:
            k: 检索的文档数量
            
        Returns:
            RAG链对象
        """
        # 定义检索函数
        def retrieve_docs(query: str) -> str:
            docs = self.vector_store_manager.similarity_search(query, k=k)
            return self.format_docs(docs)
        
        # 构建RAG链
        # 1. 接收用户问题
        # 2. 检索相关文档
        # 3. 格式化文档为上下文
        # 4. 注入到Prompt中
        # 5. 调用LLM生成回答
        # 6. 解析输出为字符串
        chain = (
            {
                "context": RunnablePassthrough() | retrieve_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        
        return chain


def demo_rag_chain():
    """演示RAG链功能"""
    print("=" * 60)
    print("RAG链模块演示")
    print("=" * 60)
    
    from vector_store import VectorStoreManager
    
    # 1. 加载向量存储
    vector_manager = VectorStoreManager()
    storage_path = os.path.join(os.path.dirname(__file__), "storage", "vectorstore")
    
    try:
        vector_manager.load_vector_store(storage_path)
    except FileNotFoundError:
        print("❌ 向量存储不存在，请先运行 vector_store.py 创建向量存储")
        return
    
    # 2. 创建RAG链
    rag = RAGChain(vector_manager)
    
    # 3. 测试问题
    test_questions = [
        "年假如何申请？需要提前几天？",
        "产假有多少天？工资怎么发？",
        "工资什么时候发放？",
        "试用期是多长时间？"
    ]
    
    print("\n" + "=" * 60)
    print("RAG问答测试")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n❓ 问题: {question}")
        print("-" * 60)
        
        result = rag.invoke(question, k=3)
        
        print(f"📝 回答:\n{result['answer']}")
        print(f"\n📚 参考文档数量: {len(result['retrieved_docs'])}")
    
    print("\n✅ 演示完成！")


if __name__ == "__main__":
    demo_rag_chain()

