# AG-CLI - 多语言模型命令行交互应用

AG-CLI 是一个基于 Python 的命令行工具，支持与多个大语言模型进行交互，使用 DashScope API 提供服务。

## 功能特性

- 🚀 支持多种大语言模型
- 💬 单次对话和连续对话模式
- 🎨 使用 Rich 库提供美观的终端界面
- ⚙️ 灵活的模型选择和配置
- 🔐 安全的 API 密钥管理

## 预览

![Usage](./static/Usage.png)

## 环境要求

- Python 3.14.*
- PDM (Python 包管理器)

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd ag-cli
```

### 2. 安装依赖

项目使用 PDM 管理依赖，请确保已安装 PDM：

```bash
pip install pdm
```

然后安装项目依赖：

```bash
pdm install
```

### 3. 配置环境变量

复制环境变量模板文件：

```bash
copy .env.template .env
```

编辑 `.env` 文件，设置你的 DashScope API 密钥：

```env
DASHSCOPE_API_KEY=sk-your-actual-api-key-here
```

> 注意：请从 [DashScope 控制台](https://dashscope.aliyun.com/) 获取有效的 API 密钥。

## 使用方法

### 基本使用

项目提供了 `ag` 命令别名，可以通过以下方式运行：

```bash
pdm run ag 你好，请介绍一下你自己
```

或者直接运行 Python 脚本：

```bash
python src/main.py 你好，请介绍一下你自己
```

### 命令行参数

| 参数              | 简写   | 说明                     |
| ----------------- | ------ | ------------------------ |
| `--model`       | `-m` | 指定使用的模型名称或别名 |
| `--list-models` | `-l` | 列出所有支持的模型别名   |
| `--continue`    | `-c` | 启用连续对话模式         |

### 使用示例

#### 单次对话

```bash
# 使用默认模型进行单次对话
pdm run ag "Python 中的列表和元组有什么区别？"

# 指定特定模型
pdm run ag -m "qwen-turbo" "请解释一下机器学习的基本概念"
```

#### 连续对话模式

```bash
# 进入连续对话模式
pdm run ag -c

# 带初始问题的连续对话
pdm run ag -c "请帮我分析这段代码"
```

#### 查看支持的模型

```bash
pdm run ag -l
```

## 项目结构

## 开发说明

### 添加新的模型支持

要添加新的模型支持，请编辑 `src/utils/models.py` 文件中的模型映射表。

### 调试模式

如果需要调试，可以直接运行：

```bash
python -m pdb src/main.py "测试问题"
```

## 故障排除

### 常见问题

1. **API 密钥错误**

   - 检查 `.env` 文件中的 `DASHSCOPE_API_KEY` 是否正确设置
   - 确认 API 密钥是否有效且有足够的额度
2. **依赖安装失败**

   - 确保使用 Python 3.14.* 版本
   - 尝试清理缓存：`pdm cache clear`
3. **命令找不到**

   - 确保已运行 `pdm install` 安装依赖
   - 检查虚拟环境是否正确激活

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## Tips

本项目绝大多数代码由**deepseek**生成
