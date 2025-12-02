"""
文档加载模块：负责加载和预处理HR制度文档

核心知识点：
1. 文档加载：支持多种格式（TXT、PDF、Word等）
2. 文档分块：将长文档切分为适合向量化的文本块
3. 分块策略：固定窗口、滑动窗口、按段落分块
"""
import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document


class DocumentLoader:
    """文档加载器：负责加载和分块文档"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 75):
        """
        初始化文档加载器
        
        Args:
            chunk_size: 每个文本块的大小（字符数）
            chunk_overlap: 文本块之间的重叠字符数（用于保持上下文连续性）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # 创建文本分割器
        # RecursiveCharacterTextSplitter会智能地按照分隔符优先级进行分割
        # 优先按段落分割，然后是句子，最后是字符
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n## ", "\n### ", "\n\n", "\n", "。", "，", " ", ""]  # 分隔符优先级
        )
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """
        加载文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Document列表
        """
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        return documents
    
    def load_pdf_file(self, file_path: str) -> List[Document]:
        """
        加载PDF文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Document列表
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        将文档分割成文本块
        
        Args:
            documents: 原始文档列表
            
        Returns:
            分割后的文档块列表
        """
        # 使用RecursiveCharacterTextSplitter进行智能分割
        chunks = self.text_splitter.split_documents(documents)
        
        # 为每个块添加元数据（来源信息）
        for i, chunk in enumerate(chunks):
            if not chunk.metadata.get('source'):
                chunk.metadata['source'] = 'unknown'
            chunk.metadata['chunk_id'] = i
        
        return chunks
    
    def load_and_split(self, file_path: str) -> List[Document]:
        """
        加载文件并自动分割（便捷方法）
        
        Args:
            file_path: 文件路径
            
        Returns:
            分割后的文档块列表
        """
        # 根据文件扩展名选择加载器
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.txt':
            documents = self.load_text_file(file_path)
        elif file_ext == '.pdf':
            documents = self.load_pdf_file(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        # 分割文档
        chunks = self.split_documents(documents)
        
        print(f"✅ 成功加载文档: {file_path}")
        print(f"📄 原始文档数: {len(documents)}")
        print(f"📦 分割后文本块数: {len(chunks)}")
        print(f"📊 平均每个文本块大小: {sum(len(chunk.page_content) for chunk in chunks) // len(chunks)} 字符")
        
        return chunks


def demo_document_loading():
    """演示文档加载功能"""
    print("=" * 60)
    print("文档加载模块演示")
    print("=" * 60)
    
    # 创建文档加载器
    loader = DocumentLoader(chunk_size=500, chunk_overlap=75)
    
    # 加载示例文档
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_dir, "hr_policy.txt")
    
    if os.path.exists(file_path):
        chunks = loader.load_and_split(file_path)
        
        # 显示前3个文本块
        print("\n前3个文本块示例：")
        for i, chunk in enumerate(chunks[:3], 1):
            print(f"\n--- 文本块 {i} ---")
            print(f"内容长度: {len(chunk.page_content)} 字符")
            print(f"来源: {chunk.metadata.get('source', 'unknown')}")
            print(f"内容预览: {chunk.page_content[:200]}...")
    else:
        print(f"❌ 文件不存在: {file_path}")


if __name__ == "__main__":
    demo_document_loading()

