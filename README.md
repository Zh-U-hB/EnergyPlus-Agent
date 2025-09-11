# EnergyPlus Agent System

## 项目概述

EnergyPlus Agent是一个基于Python和MCP（Model Context Protocol）协议的智能建筑能耗模拟系统。该系统通过LLM驱动的交互式配置流程，将建筑设计从Rhino代码无缝转换为EnergyPlus IDF文件，并提供能耗分析和优化建议。

## 核心特性

### 智能转换
- **Rhino代码解析**：自动解析Rhino建筑生成代码，提取几何和材料信息
- **LLM驱动转换**：通过大语言模型理解建筑意图，生成标准化JSON配置
- **IDF自动生成**：将JSON配置映射为符合EnergyPlus标准的IDF文件

### 交互式配置
- **MCP协议支持**：基于标准MCP协议实现工具调用和上下文管理
- **智能对话引导**：通过自然语言交互补充HVAC、照明、设备等配置
- **知识库集成**：集成建筑规范和最佳实践，提供可解释的配置建议

### 仿真与优化
- **自动验证**：IDF文件完整性和合规性自动检查
- **能耗模拟**：集成EnergyPlus引擎进行精确能耗计算
- **性能评估**：多维度能耗分析和性能评估报告
- **优化建议**：基于仿真结果提供智能优化方案

## 系统架构

```
┌─────────────────────────────────────────────────┐
│              用户交互层                          │
│   Web UI | CLI | API Gateway | MCP Client       │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│              MCP协议层                           │
│   Tool Registry | Context Manager | Session     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│              业务逻辑层                          │
│   Rhino转换 | IDF生成 | 配置填充 | 仿真引擎     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│              AI服务层                            │
│   LLM Service | RAG Engine | Prompt Manager     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│              数据持久层                          │
│   Project DB | Knowledge Base | Templates       │
└─────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.11+
- EnergyPlus 24.1.0+
- Redis 7.4+
- PostgreSQL 16+
- Node.js 20+ (可选，用于Web界面)

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/your-org/energyplus-agent.git
cd energyplus-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量

# 初始化数据库
python scripts/init_db.py

# 启动服务
python main.py
```

### 基础使用

```python
from energyplus_agent import EnergyPlusAgent

# 初始化Agent
agent = EnergyPlusAgent()

# 加载Rhino代码
rhino_code = """
# Your Rhino building generation code here
"""

# 转换为IDF
result = agent.convert(
    rhino_code=rhino_code,
    climate_zone="5A",  # 北京气候区
    building_type="office"
)

# 交互式配置
agent.configure_interactive(result.project_id)

# 运行仿真
simulation = agent.simulate(result.idf_path)

# 获取优化建议
recommendations = agent.get_recommendations(simulation.results)
```

## 项目结构

```
energyplus-agent/
├── src/                      # 源代码
│   ├── core/                # 核心模块
│   │   ├── converter/       # Rhino转换器
│   │   ├── generator/       # IDF生成器
│   │   ├── validator/       # 验证器
│   │   └── simulator/       # 仿真引擎
│   ├── mcp/                 # MCP协议实现
│   │   ├── server/          # MCP服务器
│   │   ├── tools/           # MCP工具集
│   │   └── handlers/        # 请求处理器
│   ├── ai/                  # AI服务
│   │   ├── llm/            # LLM集成
│   │   ├── rag/            # RAG引擎
│   │   └── prompts/        # 提示词管理
│   └── api/                 # API接口
├── schemas/                  # 数据模式
│   ├── building_schema.json # 建筑信息模式
│   └── idf_mapping.yaml     # IDF映射规则
├── templates/               # IDF模板
├── knowledge/               # 知识库
│   ├── standards/          # 建筑标准
│   ├── best_practices/     # 最佳实践
│   └── templates/          # 配置模板
├── tests/                   # 测试代码
├── docs/                    # 文档
├── scripts/                 # 脚本工具
└── web/                     # Web界面（可选）
```

## MCP工具集

系统提供以下MCP工具供交互使用：

### 1. search_knowledge
搜索建筑能耗知识库，获取标准规范和最佳实践

### 2. validate_config
验证建筑配置的完整性和合规性

### 3. suggest_params
基于上下文智能推荐配置参数

### 4. optimize_settings
优化系统配置以达到特定性能目标

## 技术栈

- **后端框架**: FastAPI + Pydantic
- **MCP实现**: mcp-python SDK
- **数据库**: PostgreSQL + Redis
- **任务队列**: Celery
- **LLM集成**: LangChain + OpenAI/Anthropic API
- **前端框架**: React + TypeScript + Ant Design
- **3D可视化**: Three.js
- **容器化**: Docker + Kubernetes

## 文档

- [系统架构设计](docs/architecture.md)
- [JSON Schema设计](docs/schema-design.md)
- [MCP集成方案](docs/mcp-integration.md)
- [API参考文档](docs/api-reference.md)
- [部署指南](docs/deployment.md)
- [开发指南](docs/development.md)
