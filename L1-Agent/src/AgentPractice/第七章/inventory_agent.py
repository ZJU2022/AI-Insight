"""
基于LangChain的库存调度智能代理
该代理使用Plan-and-Execute模式来分析和执行库存调度任务
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from typing import List, Dict
import json
import config  # 导入配置文件
import os

class InventoryAgent:
    def __init__(self):
        """
        初始化库存调度代理
        """
        # 初始化LLM
        self.llm = ChatOpenAI(
            temperature=0,
            model_name=os.getenv("DEEPSEEK_MODEL_NAME"),
            openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
            openai_api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        
        # 初始化工具集
        self.tools = self._create_tools()
        
        # 初始化代理
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[Tool]:
        """
        创建代理可用的工具集
        
        返回:
            工具列表
        """
        return [
            Tool(
                name="获取库存状态",
                func=self._get_inventory_status,
                description="获取当前库存状态，包括各仓库的库存水平和位置信息"
            ),
            Tool(
                name="分析库存需求",
                func=self._analyze_inventory_needs,
                description="分析各仓库的库存需求，识别需要调度的物品"
            ),
            Tool(
                name="生成调度计划",
                func=self._generate_transfer_plan,
                description="根据库存状态和需求生成最优的调度计划"
            ),
            Tool(
                name="执行调度操作",
                func=self._execute_transfer,
                description="执行具体的库存调度操作"
            ),
            Tool(
                name="验证调度结果",
                func=self._verify_transfer,
                description="验证调度操作的结果，确保调度成功"
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """
        创建代理
        
        返回:
            配置好的代理执行器
        """
        # 创建系统提示模板
        system_prompt = """你是一个专业的库存调度专家。你的任务是：
        1. 分析当前库存状态
        2. 识别需要调度的物品
        3. 制定最优的调度计划
        4. 执行调度操作
        5. 验证调度结果
        
        请按照以下步骤执行任务：
        1. 首先获取当前库存状态
        2. 分析各仓库的库存需求
        3. 生成详细的调度计划
        4. 执行调度操作
        5. 验证调度结果
        
        在制定计划时，需要考虑：
        - 运输成本
        - 时间效率
        - 库存平衡
        - 紧急程度
        """
        
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 创建内存
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建代理
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True
        )
    
    def _get_inventory_status(self) -> Dict:
        """
        获取当前库存状态
        
        返回:
            包含库存信息的字典
        """
        # 这里应该实现实际的库存查询逻辑
        # 示例返回数据
        return {
            "warehouse_1": {
                "location": "北京",
                "items": {
                    "item_1": {"quantity": 100, "min_level": 50},
                    "item_2": {"quantity": 200, "min_level": 100}
                }
            },
            "warehouse_2": {
                "location": "上海",
                "items": {
                    "item_1": {"quantity": 30, "min_level": 50},
                    "item_2": {"quantity": 150, "min_level": 100}
                }
            }
        }
    
    def _analyze_inventory_needs(self, inventory_status: Dict) -> Dict:
        """
        分析库存需求
        
        参数:
            inventory_status: 当前库存状态
            
        返回:
            包含需求分析的字典
        """
        needs = {}
        for warehouse, data in inventory_status.items():
            needs[warehouse] = {}
            for item, info in data["items"].items():
                if info["quantity"] < info["min_level"]:
                    needs[warehouse][item] = info["min_level"] - info["quantity"]
        return needs
    
    def _generate_transfer_plan(self, inventory_status: Dict, needs: Dict) -> Dict:
        """
        生成调度计划
        
        参数:
            inventory_status: 当前库存状态
            needs: 需求分析结果
            
        返回:
            调度计划
        """
        plan = {
            "transfers": []
        }
        
        # 分析每个仓库的需求
        for warehouse, warehouse_needs in needs.items():
            for item, quantity_needed in warehouse_needs.items():
                # 查找有足够库存的仓库
                for source_warehouse, source_data in inventory_status.items():
                    if source_warehouse != warehouse:
                        item_data = source_data["items"].get(item, {})
                        if item_data.get("quantity", 0) > quantity_needed:
                            plan["transfers"].append({
                                "from": source_warehouse,
                                "to": warehouse,
                                "item": item,
                                "quantity": quantity_needed
                            })
                            break
        
        return plan
    
    def _execute_transfer(self, plan: Dict) -> bool:
        """
        执行调度操作
        
        参数:
            plan: 调度计划
            
        返回:
            执行是否成功
        """
        # 这里应该实现实际的调度执行逻辑
        # 示例实现
        for transfer in plan["transfers"]:
            print(f"执行调度: 从{transfer['from']}到{transfer['to']}调度{transfer['quantity']}个{transfer['item']}")
        return True
    
    def _verify_transfer(self, plan: Dict) -> Dict:
        """
        验证调度结果
        
        参数:
            plan: 调度计划
            
        返回:
            验证结果
        """
        # 这里应该实现实际的验证逻辑
        # 示例实现
        return {
            "status": "success",
            "message": "所有调度操作已成功完成",
            "details": plan["transfers"]
        }
    
    def run(self, task: str) -> str:
        """
        运行代理处理任务
        
        参数:
            task: 任务描述
            
        返回:
            执行结果
        """
        return self.agent.invoke({"input": task})["output"]

# 使用示例
if __name__ == "__main__":
    # 初始化代理
    agent = InventoryAgent()
    
    # 运行任务
    result = agent.run("请分析当前库存状态，并执行必要的调度操作")
    print(result) 