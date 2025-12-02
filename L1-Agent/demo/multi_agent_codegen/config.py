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
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # 工作目录
    WORK_DIR = os.path.join(os.path.dirname(__file__), "workspace")
    
    # Agent配置
    TEMPERATURE = 0.7  # 温度参数，控制输出的随机性
    MAX_ITERATIONS = 10  # 最大迭代次数
    MAX_TOKENS = 2000  # 最大token数
    
    # 多Agent协作配置
    ENABLE_CODE_EXECUTION = True  # 是否启用代码执行
    ENABLE_HUMAN_INPUT = False  # 是否启用人工干预
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("请设置OPENAI_API_KEY环境变量")
        return True

