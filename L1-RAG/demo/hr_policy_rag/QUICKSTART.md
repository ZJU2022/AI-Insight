# 快速开始指南

## 🚀 5分钟快速上手

### 步骤1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤2: 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的OpenAI API密钥：

```bash
cp .env.example .env
# 然后编辑 .env 文件，填入你的 OPENAI_API_KEY
```

### 步骤3: 运行程序

```bash
python main.py
```

### 步骤4: 开始提问

程序启动后，你可以输入问题，例如：

```
❓ 请输入您的问题: 年假如何申请？
❓ 请输入您的问题: 产假有多少天？
❓ 请输入您的问题: 工资什么时候发放？
```

输入 `quit` 或 `exit` 退出程序。

## 📚 学习路径

### 初学者路径

1. **运行主程序** (`python main.py`)
   - 体验完整的RAG问答流程
   - 理解用户交互界面

2. **阅读代码模块**
   - `document_loader.py` - 理解文档加载和分块
   - `vector_store.py` - 理解向量化和存储
   - `rag_chain.py` - 理解RAG链实现

3. **运行演示脚本**
   ```bash
   python document_loader.py  # 演示文档加载
   python vector_store.py     # 演示向量存储
   python rag_chain.py        # 演示RAG链
   ```

4. **阅读README.md**
   - 深入理解每个模块的原理
   - 学习RAG的核心概念

### 进阶路径

1. **使用Jupyter Notebook**
   - 打开 `notebooks/rag_tutorial.ipynb`
   - 逐步执行每个单元格
   - 修改参数观察效果

2. **修改和实验**
   - 调整分块大小 (`chunk_size`, `chunk_overlap`)
   - 修改检索数量 (`TOP_K`)
   - 优化Prompt模板

3. **添加新功能**
   - 支持多轮对话
   - 添加置信度评估
   - 实现混合检索

## 🐛 常见问题

### Q: 提示"请设置OPENAI_API_KEY环境变量"

**解决方案**：
1. 确保创建了 `.env` 文件
2. 在 `.env` 文件中填入：`OPENAI_API_KEY=your_key_here`
3. 或者直接设置环境变量：`export OPENAI_API_KEY=your_key_here`

### Q: 向量存储文件很大

**原因**：这是正常的，每个文档块都会生成一个向量。

**优化**：
- 减少文档数量
- 使用更小的embedding模型
- 调整分块大小

### Q: 检索结果不准确

**优化方法**：
1. 调整分块大小（尝试300-800之间）
2. 增加检索数量（k值）
3. 优化查询问题（更具体、更明确）

## 📖 下一步学习

完成基础学习后，可以：

1. **阅读项目文档** (`README.md`)
   - 深入理解RAG原理
   - 学习最佳实践

2. **探索高级特性**
   - 混合检索（关键词+向量）
   - 重排序（Re-ranking）
   - 多轮对话支持

3. **应用到其他场景**
   - 法律文档问答
   - 技术文档助手
   - 客服机器人

祝你学习愉快！🎉

