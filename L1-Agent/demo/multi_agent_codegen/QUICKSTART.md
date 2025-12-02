# 快速开始指南

## 🚀 5分钟快速上手

### 步骤1: 安装依赖

```bash
cd L1-Agent/demo/multi_agent_codegen
pip install -r requirements.txt
```

### 步骤2: 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的OpenAI API密钥：

```bash
cp .env.example .env
# 然后编辑 .env 文件，填入你的 OPENAI_API_KEY
```

或者直接设置环境变量：

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 步骤3: 运行程序

```bash
python main.py
```

### 步骤4: 输入需求

程序启动后，你可以：

1. **输入自定义需求**：
   ```
   请输入你的需求: 创建一个简单的待办事项应用，支持添加、删除、查看和标记完成功能
   ```

2. **选择示例需求**：
   ```
   请输入你的需求: 1  # 选择第一个示例
   ```

3. **退出程序**：
   ```
   请输入你的需求: quit
   ```

## 📚 学习路径

### 初学者路径

1. **运行主程序** (`python main.py`)
   - 体验完整的多Agent协作流程
   - 观察每个Agent的工作过程

2. **阅读基础Agent** (`agents/base_agent.py`)
   - 理解Agent的基本结构
   - 理解Agent的四大核心要素

3. **阅读单个Agent实现**
   - `agents/requirement_agent.py` - 需求分析
   - `agents/architect_agent.py` - 架构设计
   - `agents/coder_agent.py` - 代码生成

4. **阅读协调器** (`coordinator.py`)
   - 理解多Agent协作机制
   - 理解工作流管理

5. **阅读README.md**
   - 深入理解每个模块的原理
   - 学习Agent的核心概念

### 进阶路径

1. **修改Agent行为**
   - 调整Agent的系统消息
   - 添加新的工具
   - 优化Prompt

2. **扩展工作流**
   - 添加新的工作流步骤
   - 集成新的Agent
   - 优化迭代策略

3. **应用到其他场景**
   - 文档生成系统
   - 数据分析系统
   - 自动化测试系统

## 🐛 常见问题

### Q: 提示"请设置OPENAI_API_KEY环境变量"

**解决方案**：
1. 确保创建了 `.env` 文件
2. 在 `.env` 文件中填入：`OPENAI_API_KEY=your_key_here`
3. 或者直接设置环境变量：`export OPENAI_API_KEY=your_key_here`

### Q: 生成的代码质量不高

**优化方法**：
1. 增加迭代次数（修改`main.py`中的`max_iterations`参数）
2. 使用更好的模型（如GPT-4）
3. 优化Agent的Prompt模板

### Q: 如何添加新的Agent？

**步骤**：
1. 在`agents/`目录下创建新文件（如`new_agent.py`）
2. 继承`BaseAgent`类
3. 实现Agent的特定方法
4. 在`coordinator.py`中集成新Agent

### Q: 如何修改工作流？

**方法**：
1. 编辑`coordinator.py`中的`workflow`列表
2. 添加新的工作流方法（如`_new_step()`）
3. 在`execute_workflow()`中调用新方法

## 📖 下一步学习

完成基础学习后，可以：

1. **阅读项目文档** (`README.md`)
   - 深入理解Agent原理
   - 学习最佳实践

2. **探索高级特性**
   - 添加记忆持久化
   - 实现Agent间的异步通信
   - 优化性能

3. **应用到其他场景**
   - 文档生成
   - 数据分析
   - 自动化测试

祝你学习愉快！🎉

