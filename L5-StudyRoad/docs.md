# 适合入门和复习的大模型必看课程推荐

### 一、入门学习路径（从认知到实操）
按“概念→核心原理→动手→架构深入”的逻辑推进，时间周期约4-9周：
1. **快速概念入门**
   - 内容：通过《DeepLearning.AI - Generative AI for Everyone》了解大模型全貌
   - 耗时：1-2周
   - 作用：建立大模型领域的整体认知
2. **Transformer核心原理**
   - 内容：学习《Andrej Karpathy - Introduction to Transformers》（斯坦福CS25 V2），掌握自注意力机制
   - 耗时：1天
   - 作用：聚焦大模型核心架构的基础逻辑
3. **动手实践**
   - 内容：借助《Hugging Face - NLP Course》或《Andrej Karpathy - Neural Networks: Zero to Hero》的代码示例，尝试训练/微调简单模型
   - 耗时：2-4周
   - 作用：将理论转化为实操能力
4. **巩固基础**
   - 内容：通过《Andrej Karpathy - Build nanoGPT》从头实现小型GPT模型
   - 耗时：1-2周
   - 作用：深入理解大模型的底层架构


### 二、复习学习路径（从理论框架到前沿动态）
针对已有基础的学习者，侧重体系完善与前沿跟进，时间周期约2-5周（前沿动态需持续关注）：
1. **梳理理论框架**
   - 内容：重温《Geoffrey Hinton - Representing Part-Whole Hierarchies》（斯坦福CS25 V2），回顾Transformer的局限性与未来方向
   - 耗时：1天
   - 作用：完善大模型的理论认知体系
2. **深入RAG技术**
   - 内容：学习《Douwe Kiela - Retrieval Augmented Language Models》（斯坦福CS25 V3）与《Knowledge Graphs for RAG》，巩固检索增强生成技术
   - 耗时：1-2周
   - 作用：聚焦大模型落地的关键技术（RAG）
3. **中文资源补充**
   - 内容：通过《清华大学NLP公开课》复习中文NLP与大模型的本地化应用
   - 耗时：1-2周
   - 作用：适配中文场景的技术需求
4. **前沿动态跟进**
   - 内容：关注斯坦福CS25 V5最新讲座（https://web.stanford.edu/class/cs25/），了解2025年研究进展
   - 要求：持续跟进
   - 作用：保持对大模型领域前沿的认知

# 大模型入门资源分类整理与学习建议

## 分类整理

### 1. 综合教程与课程（理论+实践）
- 动手学大模型应用开发: Datawhale的开源教程，覆盖大模型基础、开发与应用，适合初学者系统学习。
- Large Language Models (LLMs) with Colab notebooks: 提供Colab笔记本，边学边练，适合动手实践。
- AI-Guide-and-Demos: 中文AI指南与代码示例，适合中文用户快速上手。
- LLM-Action: 聚焦大模型实战项目，适合进阶开发者。


### 2. 视频资源（B站/YT）
- B站：五里墩茶社、木羽Cheney、漆妮妮、TechBeat人工智能社区等，内容涵盖大模型基础、算法解析和项目实战，适合初学者和爱好者。
- YouTube：AI Anytime、AI超元域、IBM Technology，提供英文内容，适合了解国际前沿动态。
- Unify Reading Paper Group：论文解读，适合深入研究大模型理论。


### 3. 博客与文章（深入理论与实践）
- Huggingface Blog：提供大模型工具、框架和案例，适合开发者参考。
- Lil' Log (OponAI)：OpenAI研究员博客，深入解析大模型技术，适合进阶学习。
- 科学空间（苏剑林）：中文AI博客，理论与代码结合，适合国内开发者。
- Chip Huyen、mlabonne：英文博客，分享大模型开发经验与趋势。


### 4. Prompt工程与可视化
- Prompt Engineering Guide：Prompt设计的最佳实践，适合优化大模型交互。
- LLM Visualization：大模型结构可视化，助力理解Transformer等核心概念。


### 5. 进阶与实战工具
- How Much VRAM：帮助评估大模型训练的显存需求，适合硬件选型。
- Implementation of all RAG techniques：RAG（检索增强生成）技术实现，适合开发知识密集型应用。
- W&B articles：Weights & Biases的文章，分享模型训练与调优技巧。


### 6. 理论书籍与资源
- Theoretical Machine Learning: A Handbook for Everyone：机器学习理论手册，适合打牢基础。


## 学习建议
- 零基础入门：从[动手学大模型应用开发]和B站视频（如五里墩茶社、漆妮妮）开始，结合Colab笔记本实践。
- 进阶开发：深入[Huggingface Blog]、[Lil' Log]，并尝试[LLM-Action]和[Implementation of all RAG techniques]的实战项目。
- 优化Prompt：参考[Prompt Engineering Guide]，提升模型交互效果。
- 硬件与资源管理：用[How Much VRAM]评估显存需求，结合[W&B articles]优化训练流程。
- 持续跟踪前沿：关注[Unify Reading Paper Group]和[Chip Huyen]，了解最新论文与趋势。


## 补充资源
- DeepLearning.AI：提供大模型与AI开发的免费/付费课程，Andrew Ng团队出品。
- Fast.ai：实用深度学习课程，适合快速上手。
- GitHub Awesome-LLM：大模型资源合集，包含论文、工具和数据集。

# 全套课程资源与学习规划（tips：以下内容皆有具体资料，不存放于此项目中）

### 一、资源分类（覆盖多元学习渠道）
该框架将大模型学习资源分为5类，适配不同学习场景：
1. **大学课程**：包含斯坦福大学、卡内基梅隆大学等高校的专业课程，这类资源理论体系扎实、学术性强，适合构建学科基础；
2. **在线课程与教程**：涵盖DeepLearning.AI、OpenAI、Hugging Face、微软等机构的内容，侧重实践与前沿应用，适配不同学习进度的用户；
3. **开源资源与教程**：（仅标注分类）通常是社区驱动的免费材料，适合动手实践与自主探索；
4. **专题资源**：（仅标注分类）聚焦特定技术方向（如RAG、Agent等），适合深入细分领域；
5. **社区与中文资源**：（仅标注分类）侧重中文语境的内容与交流渠道，降低国内学习者的入门门槛。


### 二、学习阶段划分（适配不同基础）
框架区分了两类课程，匹配不同学习者的需求：
- **入门必看**：针对零基础用户，内容以基础概念、核心原理为主；
- **复习必看**：面向有基础的学习者，侧重知识体系的巩固与查漏补缺。


### 三、学习路径规划（明确时间与重点）
框架提供了分周期的进度指引：
- **入门路径（1-2个月）**：帮助新手快速建立大模型领域的认知与基础能力；
- **复习路径（1个月）**：辅助学习者高效回顾核心知识，强化体系连贯性；
- **其他建议**：（仅标注分类）通常包含学习方法、资源搭配等实用指导。