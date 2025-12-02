## 章节导览

> 本导览将现有示例脚本与学习目标进行映射，方便你快速上手。随着仓库的发展，我们会在 `docs/chapters/` 中提供更详细的课程手册、讲义和练习题。

---

### 第二章 · ReAct Agent 实战
- **目标**：体验 ReAct 思维链 + 工具调用模式，掌握 LangChain Hub 与 SerpAPI 的结合方式
- **核心脚本**：`Agent/第二章/react_agent.py`
- **任务建议**
  - 自定义 Prompt 模板，尝试增加领域知识
  - 替换或扩展工具（如知识库检索、内部 API）
  - 为响应增加结构化输出，便于后续处理

---

### 第三章 · 大模型 API 与 RAG 入门
- **目标**：熟悉 OpenAI 官方 SDK、LangChain、LlamaIndex 的基础用法
- **核心脚本**
  - `Agent/第三章/openai_test_01.py`：Chat Completions 基本交互
  - `Agent/第三章/openai_test_langchain_03.py`：LangChain 工具使用
  - `Agent/第三章/openai_test_LlamaIndex_04.py`：向量存储与检索
- **任务建议**
  - 体验不同模型参数（temperature、top_p）的影响
  - 尝试对接国内模型服务（Moonshot、DeepSeek 等）
  - 整理 API 响应，构建最小化的文档检索问答

---

### 第四章 · 助手能力与函数调用
- **目标**：理解 LLM 函数调用（Function Calling）以及多轮对话状态管理
- **核心脚本**
  - `Agent/第四章/assiant.py`：基础助手能力
  - `Agent/第四章/assiant02.py`：上下文管理与扩展
- **任务建议**
  - 引入自定义工具函数，处理结构化数据
  - 添加日志与错误处理，提升可靠性
  - 结合外部 API，构建领域助手（如天气、金融）

---

### 第五章 · ReAct 进阶与多工具协同
- **目标**：深度理解 ReAct 框架的思考过程，探索多步工具链的协作策略
- **核心脚本**
  - `Agent/第五章/functioncalling.py`
  - `Agent/第五章/react.py`
- **任务建议**
  - 设计实验对比不同思维链长度的影响
  - 引入工具并行、回退机制，增强容错能力
  - 对接真实业务场景（如数据分析、客服）

---

### 第七章 · Agent 框架百宝箱
- **目标**：横向对比主流 Agent 框架（AutoGen、CrewAI、BabyAGI 等），理解框架抽象
- **核心资源**
  - `Agent/第七章/autogen_demo.py`
  - `Agent/第七章/camel.py`
  - `Agent/第七章/babyagi_example.py`
- **任务建议**
  - 评估不同框架在任务规划、对话管理、工具调用上的差异
  - 整理 Benchmark，输出心得报告
  - 探索框架混搭的可能性（如 AutoGen + 自建工具集）

---

### 附录 · 数据获取与分析
- `Agent/1.py`：招聘需求爬虫示例，可扩展用于岗位调研与趋势分析
- 结合第三阶段“面试实践与能力验证”，可构建岗位能力 Radar 图或技能差距分析工具

---

## 接下来做什么？
1. 复制示例脚本至 `examples/`，根据任务拆分输入输出流程
2. 为每章补充 README、数据资源与测试用例
3. 整理环境依赖，提供一键启动脚本或 Docker 配置

