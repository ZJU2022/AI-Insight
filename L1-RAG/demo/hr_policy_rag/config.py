"""
配置文件：管理API密钥、模型参数等配置信息
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # OpenAI API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 向量数据库配置
    VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "storage", "vectorstore")
    
    # 文档配置
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    
    # 分块配置
    CHUNK_SIZE = 500  # 每个文本块的大小（字符数）
    CHUNK_OVERLAP = 75  # 文本块之间的重叠字符数
    
    # 检索配置
    TOP_K = 3  # 检索返回的最相关文档数量
    
    # Embedding配置
    EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI的embedding模型
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("请设置OPENAI_API_KEY环境变量")
        return True

