#导入所需的库
import config  # 导入配置文件以设置 API keys
from langchain_core.output_parsers import StrOutputParser#用于将输出结果解析为字符串
from langchain_core.prompts import ChatPromptTemplate#用于创建聊天提示模板
from langchain_openai import ChatOpenAI
import os

#创建一个聊天提示模板，其中{topic)是占位符，用于后续插入具体的话题
prompt = ChatPromptTemplate.from_template("请讲一个关于{topic}的故事")

#初始化模型
model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-r1:70b"),
    temperature=0.7,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_BASE")
)

#初始化一个输出解析器，用于将模型的输出解析成字符串
output_parser = StrOutputParser()

"通过管道操作符(1)连接各个处理步骤，以创建一个处理链其中，prompt用于生成具体的提示文本，model用于根据提示文本生成回应，output_parser用于处理Out回应并将其转换为字符串"
chain = prompt | model | output_parser

#调用处理链，传入话题"水仙花"，执行生成故事的操作
message = chain.invoke({"topic": "水仙花"})

#打印链的输出结果
print(message)