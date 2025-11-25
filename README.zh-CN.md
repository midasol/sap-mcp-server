# SAP MCP - 通过模型上下文协议 (MCP) 集成 SAP Gateway

用于 SAP Gateway 集成的完整 MCP 服务器，为 AI 代理和 SAP OData 操作提供模块化工具。

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

</div>

---
## 📑 目录

- [🎯 项目概述](#-项目概述)
- [📋 准备工作](#-准备工作)
- [📐 架构](#-架构)
  - [系统概览](#系统概览)
  - [组件详情](#组件详情)
  - [数据流](#数据流-订单查询示例)
  - [工具执行流](#工具执行流)
  - [安全架构](#安全架构)
- [📦 仓库结构](#-仓库结构)
- [✨ 功能](#-功能)
- [🎓 SAP SFLIGHT 演示场景](#-sap-sflight-演示场景)
  - [场景概览](#场景概览)
  - [OData 服务创建指南](#odata-服务创建指南)
- [🚀 快速开始](#-快速开始)
  - [MCP 服务器前提条件](#mcp-服务器前提条件)
  - [安装](#1-安装)
  - [配置](#2-配置)
  - [运行服务器](#3-运行服务器)
- [🤖 与 Gemini CLI 集成](#-与-gemini-cli-集成)
  - [前提条件](#前提条件)
  - [安装 Gemini CLI](#1-安装-gemini-cli)
  - [Gemini CLI 认证](#2-gemini-cli-认证)
  - [注册 SAP MCP 服务器](#3-注册-sap-mcp-服务器)
  - [开始使用](#4-开始在-gemini-cli-中使用-sap-mcp)
  - [高级配置](#高级配置)
  - [故障排除](#故障排除)
  - [可用工具](#gemini-cli-中可用的-sap-工具)
  - [工作流示例](#工作流示例)
- [🔧 可用工具](#-可用工具)
  - [SAP 认证 (sap_authenticate)](#1-sap-认证-sap_authenticate)
  - [SAP 查询 (sap_query)](#2-sap-查询-sap_query)
  - [SAP 实体获取 (sap_get_entity)](#3-sap-实体获取-sap_get_entity)
  - [SAP 服务列表 (sap_list_services)](#4-sap-服务列表-sap_list_services)
  - [添加新工具](#5-添加新工具)
- [📚 使用示例](#-使用示例)
- [🔒 安全](#-安全)
- [📖 文档](#-文档)
- [📝 许可证](#-许可证)
- [🙏 致谢](#-致谢)

---


## 🎯 项目概述

这是一个生产就绪的模型上下文协议 (MCP) 服务器，旨在通过清晰、模块化的架构使 AI 代理和应用程序能够与 SAP Gateway 系统进行交互。专为可靠性、安全性和开发者体验而构建。

**当前状态**: ✅ **生产就绪** (所有 5 个阶段已完成)

### 主要特性

- 🔐 **安全的 SAP 集成**: 企业级认证和 SSL/TLS 支持
- 🛠️ **4 个模块化工具**: 认证、查询、实体获取和服务发现
- 🚀 **Stdio 传输**: 生产级 MCP 服务器
- 📊 **结构化日志**: JSON 和控制台格式，包含性能指标
- ✅ **验证输入**: 全面的 OData 和安全验证
- 🧪 **充分测试**: 56% 覆盖率，44/45 测试通过 (98% 成功率)

---

---

## 📋 准备工作

在 5 分钟内开始使用 SAP MCP：

```bash
# 1. 克隆并进入项目
git clone <repository-url>
cd sap-mcp

# 2. 创建虚拟环境并安装
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
cd packages/server
pip install -e .

# 3. 配置 SAP 连接
cd ../..
cp .env.server.example .env.server
# 编辑 .env.server 填入您的 SAP 凭据

# 4. 配置服务
cp packages/server/config/services.yaml.example packages/server/config/services.yaml
# 编辑 services.yaml 配置您的 SAP 服务

# 5. 运行服务器
sap-mcp-server-stdio
```

**下一步：**
- 📖 详细安装说明，请参阅 [快速开始](#-快速开始)。
- 🤖 连接 AI 代理，请查看 [与 Gemini CLI 集成](#-与-gemini-cli-集成)。
- 🔧 API 文档，请浏览 [可用工具](#-可用工具)。

## 📐 架构

### 系统概览

<details>
<summary>📊 查看系统概览图（点击展开）</summary>

```mermaid
graph TB
    subgraph clients["🎯 客户端应用"]
        direction TB
        A1["AI 代理<br/><small>LLM/GenAI 集成</small>"]
        A2["Python 客户端<br/><small>SDK & 库</small>"]
        A3["订单聊天机器人<br/><small>示例应用</small>"]
    end

    subgraph transport["🚀 MCP 服务器层"]
        direction TB
        B1["Stdio 传输<br/><small>stdin/stdout 流</small>"]
    end

    subgraph registry["🛠️ 工具注册表"]
        direction LR
        C1["sap_authenticate<br/><small>认证</small>"]
        C2["sap_query<br/><small>OData 查询</small>"]
        C3["sap_get_entity<br/><small>实体获取</small>"]
        C4["sap_list_services<br/><small>服务发现</small>"]
    end

    subgraph core["⚡ 核心层"]
        direction LR
        D1["SAP 客户端<br/><small>OData 处理程序</small>"]
        D2["认证管理器<br/><small>凭据</small>"]
        D3["配置加载器<br/><small>YAML/ENV</small>"]
    end

    subgraph utils["🔧 工具类"]
        direction LR
        E1["验证器<br/><small>输入/安全</small>"]
        E2["日志记录器<br/><small>结构化日志</small>"]
        E3["错误处理程序<br/><small>生产级</small>"]
    end

    subgraph sap["🏢 SAP Gateway"]
        direction TB
        F1["OData 服务<br/><small>v2/v4 协议</small>"]
        F2["业务数据<br/><small>订单/销售/库存</small>"]
    end

    A1 & A2 & A3 -->|活动连接| B1
    B1 -->|工具分发| C1 & C2 & C3 & C4
    C1 & C2 & C3 & C4 -->|核心服务| D1
    C1 -->|认证流程| D2
    C2 & C3 & C4 -->|配置访问| D3
    D1 & D2 & D3 -->|验证 & 日志| E1 & E2 & E3
    D1 -->|OData 协议| F1
    F1 -->|数据访问| F2

    classDef clientNode fill:#D6EAF8,stroke:#3498DB,stroke-width:2px,padding:20px
    classDef transportNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:20px
    classDef futureNode fill:#E8E8E8,stroke:#999999,stroke-width:2px,stroke-dasharray:5 5
    classDef toolNode fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,padding:20px
    classDef coreNode fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,padding:20px
    classDef utilNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:20px
    classDef sapNode fill:#EBDEF0,stroke:#8E44AD,stroke-width:2px,padding:20px

    class A1,A2,A3 clientNode
    class B1 transportNode
    class C1,C2,C3,C4 toolNode
    class D1,D2,D3 coreNode
    class E1,E2,E3 utilNode
    class F1,F2 sapNode
```

</details>

### 组件详情

<details>
<summary>🔧 查看组件详情图（点击展开）</summary>

```mermaid
graph TB
    subgraph pkg["📦 packages/server/src/sap_mcp_server"]
        direction TB

        subgraph trans["🚀 transports/"]
            direction LR
            T1["stdio.py<br/><small>CLI 入口点</small>"]
        end

        subgraph tools["🛠️ tools/"]
            direction TB
            TO5["base.py<br/><small>工具基类</small>"]

            subgraph toolImpl["工具实现"]
                direction LR
                TO1["auth_tool.py<br/><small>认证</small>"]
                TO2["query_tool.py<br/><small>OData 查询</small>"]
                TO3["entity_tool.py<br/><small>单一实体</small>"]
                TO4["service_tool.py<br/><small>服务列表</small>"]
            end
        end

        subgraph core["⚡ core/"]
            direction LR
            C1["sap_client.py<br/><small>OData 客户端</small>"]
            C2["auth.py<br/><small>认证管理器</small>"]
            C3["exceptions.py<br/><small>自定义错误</small>"]
        end

        subgraph config["⚙️ config/"]
            direction LR
            CF1["settings.py<br/><small>环境设置</small>"]
            CF2["loader.py<br/><small>YAML 加载器</small>"]
            CF3["schemas.py<br/><small>Pydantic 模型</small>"]
        end

        subgraph utils["🔧 utils/"]
            direction LR
            U1["logger.py<br/><small>结构化日志</small>"]
            U2["validators.py<br/><small>输入验证</small>"]
        end

        subgraph protocol["📡 protocol/"]
            P1["schemas.py<br/><small>MCP 请求/响应</small>"]
        end
    end

    T1 -->|分发| TO1 & TO2 & TO3 & TO4
    TO1 & TO2 & TO3 & TO4 -.->|继承| TO5
    TO5 -->|使用| C1 & C2
    C1 -->|加载| CF1 & CF2
    C2 -->|读取| CF1
    C1 & C2 -->|验证 & 日志| U1 & U2
    TO5 -.->|实现| P1
    C3 -.->|错误类型| C1 & C2

    classDef transportNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:18px
    classDef futureNode fill:#E8E8E8,stroke:#999999,stroke-width:2px,stroke-dasharray:5 5
    classDef toolNode fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,padding:18px
    classDef baseNode fill:#D6EAF8,stroke:#3498DB,stroke-width:2px,padding:18px
    classDef coreNode fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,padding:18px
    classDef configNode fill:#D6EAF8,stroke:#3498DB,stroke-width:2px,padding:18px
    classDef utilNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:18px
    classDef protocolNode fill:#EBDEF0,stroke:#8E44AD,stroke-width:2px,padding:18px

    class T1 transportNode
    class TO1,TO2,TO3,TO4 toolNode
    class TO5 baseNode
    class C1,C2,C3 coreNode
    class CF1,CF2,CF3 configNode
    class U1,U2 utilNode
    class P1 protocolNode
```

</details>

### 数据流: 订单查询示例

<details>
<summary>🔄 查看数据流图（点击展开）</summary>

```mermaid
sequenceDiagram
    autonumber
    box rgba(214, 234, 248, 0.3) 客户端层
        participant Client as 🤖<br/>AI 代理/客户端
    end
    box rgba(213, 245, 227, 0.3) 传输层
        participant Transport as 📡<br/>Stdio 传输
        participant Registry as 📋<br/>工具注册表
    end
    box rgba(252, 243, 207, 0.3) 工具层
        participant AuthTool as 🔐<br/>认证工具
        participant QueryTool as 🔍<br/>查询工具
    end
    box rgba(250, 219, 216, 0.3) 核心层
        participant SAPClient as 🔧<br/>SAP 客户端
    end
    box rgba(213, 245, 227, 0.3) 支持层
        participant Validator as ✅<br/>验证器
        participant Logger as 📊<br/>日志记录器
    end
    box rgba(235, 222, 240, 0.3) 外部
        participant SAP as 🏢<br/>SAP Gateway
    end

    rect rgba(214, 234, 248, 0.15)
        Note over Client,Registry: ⚡ 阶段 1: 会话初始化
        Client->>+Transport: 通过 stdio 流连接
        Transport->>+Registry: 初始化工具注册表
        Registry-->>-Transport: ✅ 4 个工具已注册
        Transport-->>-Client: 连接建立
    end

    rect rgba(213, 245, 227, 0.15)
        Note over Client,SAP: 🔐 阶段 2: 认证
        Client->>+Transport: call_tool(sap_authenticate, {})
        Transport->>+Registry: 获取工具: sap_authenticate
        Registry->>+AuthTool: 执行认证
        AuthTool->>+Validator: 验证凭据
        Validator-->>-AuthTool: ✅ 凭据有效
        AuthTool->>+Logger: 记录认证尝试
        Logger-->>-AuthTool: 已记录
        AuthTool->>+SAPClient: 向 SAP 认证
        SAPClient->>+SAP: POST /sap/opu/odata/auth
        SAP-->>-SAPClient: 200 OK + 会话令牌
        SAPClient-->>-AuthTool: ✅ 认证成功
        AuthTool-->>-Registry: 成功响应
        Registry-->>-Transport: 认证令牌 + 会话 ID
        Transport-->>-Client: ✅ 认证完成
    end

    rect rgba(252, 243, 207, 0.15)
        Note over Client,SAP: 🔍 阶段 3: 执行查询
        Client->>+Transport: call_tool(sap_query, {filter: "OrderID eq '91000043'"})
        Transport->>+Registry: 获取工具: sap_query
        Registry->>+QueryTool: 带参数执行
        QueryTool->>+Validator: 验证 OData 过滤语法
        Validator-->>-QueryTool: ✅ 过滤器安全
        QueryTool->>+Logger: 记录查询开始
        Logger-->>-QueryTool: 已记录
        QueryTool->>+SAPClient: 执行 OData 查询
        SAPClient->>+SAP: GET /OrderSet?$filter=OrderID eq '91000043'
        SAP-->>-SAPClient: 200 OK + 订单数据 (JSON)
        SAPClient->>SAPClient: 解析响应 & 转换
        SAPClient-->>-QueryTool: ✅ 已解析的订单数据
        QueryTool->>+Logger: 记录查询成功 + 指标
        Logger-->>-QueryTool: 已记录
        QueryTool-->>-Registry: 订单详情
        Registry-->>-Transport: 格式化响应
        Transport-->>-Client: ✅ 查询完成
    end

    rect rgba(213, 245, 227, 0.15)
        Note over Logger: 📊 阶段 4: 性能追踪
        Logger->>Logger: 计算执行指标
        Logger->>Logger: 写入结构化 JSON 日志
        Logger->>Logger: 更新性能计数器
    end
```

</details>

### 工具执行流

<details>
<summary>⚡ 查看工具执行流图（点击展开）</summary>

```mermaid
flowchart TD
    Start([🚀 客户端请求<br/><small>工具调用</small>])

    Start --> Validate{🔍 输入验证<br/><small>模式检查</small><br/><small>安全扫描</small>}

    Validate -->|❌ 无效| Error1[🚫 验证错误<br/><small>返回错误详情</small>]
    Validate -->|✅ 有效| Auth{🔐 已认证?<br/><small>检查会话</small>}

    Auth -->|否| DoAuth[🔑 执行认证<br/><small>验证凭据</small><br/><small>SAP 握手</small>]
    DoAuth --> AuthCheck{✅ 认证成功?<br/><small>接收令牌</small>}

    AuthCheck -->|❌ 失败| Error2[🚫 认证错误<br/><small>凭据无效</small>]
    AuthCheck -->|✅ 成功| Execute

    Auth -->|是| Execute[⚡ 执行工具<br/><small>业务逻辑</small><br/><small>处理参数</small>]

    Execute --> SAPCall[🌐 SAP OData 调用<br/><small>HTTP 请求</small><br/><small>SSL/TLS 加密</small>]

    SAPCall --> SAPCheck{📡 SAP 响应<br/><small>检查状态</small>}

    SAPCheck -->|❌ 错误| Error3[🚫 SAP 错误<br/><small>服务不可用</small><br/><small>或数据错误</small>]
    SAPCheck -->|✅ 200 OK| Parse[📊 解析响应<br/><small>XML/JSON 解析</small><br/><small>提取数据</small>]

    Parse --> Transform[🔄 转换数据<br/><small>MCP 格式</small><br/><small>模式映射</small>]

    Transform --> Log[📝 记录指标<br/><small>性能数据</small><br/><small>审计跟踪</small>]

    Log --> Success([✅ 成功响应<br/><small>返回给客户端</small>])

    Error1 & Error2 & Error3 --> LogError[📝 记录错误<br/><small>错误上下文</small><br/><small>堆栈跟踪</small>]

    LogError --> End([❌ 错误响应<br/><small>返回给客户端</small>])

    classDef startNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:18px
    classDef decisionNode fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px,padding:18px
    classDef authNode fill:#EBDEF0,stroke:#8E44AD,stroke-width:2px,padding:18px
    classDef processNode fill:#D6EAF8,stroke:#3498DB,stroke-width:2px,padding:18px
    classDef sapNode fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,padding:18px
    classDef errorNode fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,padding:18px
    classDef logNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:18px
    classDef successNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px,padding:18px
    classDef endNode fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,padding:18px

    class Start startNode
    class Validate,SAPCheck,AuthCheck decisionNode
    class DoAuth authNode
    class Execute,Parse,Transform processNode
    class SAPCall sapNode
    class Error1,Error2,Error3 errorNode
    class Log,LogError logNode
    class Success successNode
    class End endNode
```

</details>

### 安全架构

<details>
<summary>🔒 查看安全架构图（点击展开）</summary>

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'14px', 'fontFamily':'arial'}}}%%
graph TB
    subgraph security["🛡️ 纵深防御安全架构"]
        direction TB

        subgraph layer1["层 1: 输入验证 - 入口点安全"]
            direction LR
            L1A["🔍 OData 过滤器<br/><br/>SQL 注入<br/>防护<br/><br/>语法验证"]
            L1B["🔑 实体键<br/><br/>格式<br/>验证<br/><br/>类型检查"]
            L1C["🧹 清理<br/><br/>XSS<br/>防护<br/><br/>输入清洗"]
        end

        subgraph layer2["层 2: 认证 - 身份验证"]
            direction LR
            L2A["✅ 凭据<br/><br/>用户<br/>验证<br/><br/>密码检查"]
            L2B["🎫 会话<br/><br/>会话<br/>生命周期<br/><br/>超时处理"]
            L2C["🔐 令牌<br/><br/>JWT/Bearer<br/>令牌<br/><br/>令牌轮换"]
        end

        subgraph layer3["层 3: 授权 - 访问控制"]
            direction LR
            L3A["🚦 服务访问<br/><br/>服务级<br/>RBAC<br/><br/>权限矩阵"]
            L3B["📋 实体权限<br/><br/>数据级<br/>访问<br/><br/>字段过滤"]
        end

        subgraph layer4["层 4: 传输安全 - 加密层"]
            direction LR
            L4A["🔒 SSL/TLS<br/><br/>仅 TLS 1.2+<br/><br/>完全前向<br/>保密"]
            L4B["📜 证书<br/><br/>链<br/>验证<br/><br/>吊销检查"]
        end

        subgraph layer5["层 5: 审计 & 监控 - 可观测性"]
            direction LR
            L5A["📊 结构化日志<br/><br/>JSON 日志<br/><br/>PII 编辑"]
            L5B["⚡ 性能<br/><br/>指标<br/>追踪<br/><br/>SLA 监控"]
            L5C["🚨 错误追踪<br/><br/>异常<br/>记录<br/><br/>警报触发"]
        end
    end

    L1A & L1B & L1C -->|已验证输入| L2A
    L2A -->|已验证身份| L2B
    L2B -->|会话活跃| L2C
    L2C -->|已认证| L3A & L3B
    L3A & L3B -->|已授权| L4A & L4B
    L4A & L4B -->|已加密| L5A & L5B & L5C

    classDef inputNode fill:#FADBD8,stroke:#E74C3C,stroke-width:3px,padding:25px
    classDef authNode fill:#FCF3CF,stroke:#F1C40F,stroke-width:3px,padding:25px
    classDef authzNode fill:#EBDEF0,stroke:#8E44AD,stroke-width:3px,padding:25px
    classDef transportNode fill:#D6EAF8,stroke:#3498DB,stroke-width:3px,padding:25px
    classDef auditNode fill:#D5F5E3,stroke:#2ECC71,stroke-width:3px,padding:25px

    class L1A,L1B,L1C inputNode
    class L2A,L2B,L2C authNode
    class L3A,L3B authzNode
    class L4A,L4B transportNode
    class L5A,L5B,L5C auditNode
```

</details>

---

## 📦 仓库结构

```
sap-mcp/
├── packages/
│   └── server/                          ✅ 生产就绪 MCP 服务器
│       ├── src/sap_mcp_server/
│       │   ├── core/                    # SAP 客户端 & 认证 (4 文件)
│       │   │   ├── __init__.py          # 模块初始化
│       │   │   ├── sap_client.py        # OData 操作
│       │   │   ├── auth.py              # 凭据管理
│       │   │   └── exceptions.py        # 自定义异常
│       │   ├── config/                  # 配置 (4 文件)
│       │   │   ├── __init__.py          # 模块初始化
│       │   │   ├── settings.py          # 环境设置
│       │   │   ├── loader.py            # YAML 加载器
│       │   │   └── schemas.py           # Pydantic 模型
│       │   ├── protocol/                # MCP 协议 (2 文件)
│       │   │   ├── __init__.py          # 模块初始化
│       │   │   └── schemas.py           # 请求/响应模式
│       │   ├── tools/                   # 4 个模块化 SAP 工具 (6 文件)
│       │   │   ├── __init__.py          # 工具注册表
│       │   │   ├── base.py              # 工具基类
│       │   │   ├── auth_tool.py         # 认证
│       │   │   ├── query_tool.py        # OData 查询
│       │   │   ├── entity_tool.py       # 实体获取
│       │   │   └── service_tool.py      # 服务发现
│       │   ├── transports/              # 传输层 (2 文件)
│       │   │   ├── __init__.py          # 模块初始化
│       │   │   └── stdio.py             # Stdio 传输 ✅
│       │   ├── utils/                   # 工具类 (3 文件)
│       │   │   ├── __init__.py          # 模块初始化
│       │   │   ├── logger.py            # 结构化日志
│       │   │   └── validators.py        # 输入验证
│       │   └── __init__.py              # 包初始化
│       ├── config/                      # 服务器配置
│       │   ├── services.yaml            # SAP 服务配置
│       │   └── services.yaml.example    # 配置模板
│       ├── tests/                       # 测试套件 (7 文件, 56% 覆盖率)
│       │   ├── __init__.py              # 测试包初始化
│       │   ├── conftest.py              # Pytest fixtures
│       │   ├── unit/                    # 单元测试
│       │   │   ├── __init__.py          # 单元测试包
│       │   │   ├── test_base.py         # 基础工具测试
│       │   │   └── test_validators.py   # 验证器测试
│       │   └── integration/             # 集成测试
│       │       ├── __init__.py          # 集成测试包
│       │       └── test_tool_integration.py  # 工具集成测试
│       ├── pyproject.toml               # 包配置
│       └── README.md                    # 服务器包文档
│
├── docs/                                # 文档
│   ├── architecture/                    # 架构文档
│   │   └── server.md                    # 服务器架构
│   └── guides/                          # 用户指南
│       ├── configuration.md             # 配置指南
│       ├── deployment.md                # 部署指南
│       ├── troubleshooting.md           # 故障排除指南
│       ├── odata-service-creation-flight-demo.md  # OData 服务创建
│       └── sfight-demo-guide.md         # SFLIGHT 演示指南
│
├── examples/                            # 示例应用
│   ├── basic/                           # 基础示例
│   │   └── stdio_client.py              # Stdio 客户端示例
│   ├── chatbot/                         # 聊天机器人示例
│   │   └── order_inquiry_chatbot.py     # 订单查询聊天机器人
│   └── README.md                        # 示例文档
│
├── scripts/                             # 开发脚本
│   ├── create_structure.sh              # 项目结构创建
│   ├── migrate_code.sh                  # 代码迁移脚本
│   └── update_imports.py                # 导入更新脚本
│
├── .env.server.example                  # 环境模板
├── README.md                            # 主文档 (英语)
├── README.ja.md                         # 日语文档
├── README.ko.md                         # 韩语文档
├── README.th.md                         # 泰语文档
├── README.zh-TW.md                      # 繁体中文文档
└── README.zh-CN.md                      # 简体中文文档
```

---

## ✨ 功能

### 核心功能

<table>
<tr>
<td width="50%">

#### 🛠️ 工具
- ✅ **sap_authenticate**: 安全的 SAP 认证
- ✅ **sap_query**: 带过滤器的 OData 查询
- ✅ **sap_get_entity**: 单一实体获取
- ✅ **sap_list_services**: 服务发现

</td>
<td width="50%">

#### 🚀 传输
- ✅ **Stdio**: 生产就绪 stdin/stdout

</td>
</tr>
<tr>
<td>

#### 📊 日志 & 监控
- ✅ **结构化日志**: JSON + 控制台
- ✅ **性能指标**: 请求计时
- ✅ **错误追踪**: 完整上下文
- ✅ **审计跟踪**: 安全事件

</td>
<td>

#### 🔒 安全
- ✅ **输入验证**: OData & 安全
- ✅ **SSL/TLS 支持**: 安全连接
- ✅ **凭据管理**: .env.server
- ✅ **错误处理**: 生产级

</td>
</tr>
</table>

### 开发者体验

- ✅ **模块化架构**: 每个工具一个文件
- ✅ **类型安全**: 完整的类型提示
- ✅ **文档**: 全面的指南
- ✅ **轻松设置**: `pip install -e .`
- ✅ **热重载**: 开发模式
- ✅ **示例应用**: 3 个工作示例

---

## 🎓 SAP SFLIGHT 演示场景

### 场景概览

为方便起见，本项目基于 SAP SFLIGHT 演示数据集。

SFLIGHT 数据集是 SAP 提供的标准示例数据库，包含航班时刻表、航空公司、机场和预订数据。它是测试和演示数据建模及服务创建的绝佳资源。

本指南假设您有一个公开此数据集的 OData 服务。目标是将 SAP MCP 服务器连接到此服务，并使用 AI 代理或其他客户端与其交互。

**SAP 官方文档:**
- [SAP 文档 - Flight Model](https://help.sap.com/SAPhelp_nw73/helpdata/en/cf/21f304446011d189700000e8322d00/frameset.htm)
- [SAP Help Portal - Flight Model](https://help.sap.com/docs/SAP_NETWEAVER_702/ff5206fc6c551014a1d28b076487e7df/cf21f304446011d189700000e8322d00.html)

---

### OData 服务创建指南

本指南将引导您使用 SAP Gateway Service Builder (`SEGW`) 在 SAP 系统中创建一个 OData 服务，以公开 Flight 场景数据，这些数据通常在 SAP S/4HANA Fully Activated Appliance (FAA) 版本中可用。

#### 场景概览

* **目标:** 通过 OData 服务公开航班时刻表、预订和相关主数据。
* **场景数据要求:** 航班时刻表、日期、时间、机场详情、航空公司详情、乘客详情、价格等。
* **相关 SAP 表:** `SFLIGHT`, `SPFLI`, `SCARR`, `SAIRPORT`, `SBOOK`, `SCUSTOM`.

---

#### 在 SEGW 中创建 OData 服务的步骤

##### 1. 访问 SAP Gateway Service Builder

转到 SAP 事务代码 `SEGW`。

##### 2. 创建新项目

1. 点击 "Create Project" 按钮。
2. **Project Name:** 分配一个名称 (例如 `Z_TRAVEL_RECOMMENDATIONS_SRV`)。
3. **Description:** 输入有意义的描述。
4. **Package:** 分配到一个包 (例如 `$TMP` 用于本地开发或可传输的包)。

##### 3. 从 DDIC 结构导入数据模型

此步骤根据底层 SAP 表定义 OData 实体。

1. 右键点击项目中的 "Data Model" 文件夹。
2. 选择 **"Import" -> "DDIC Structure"**。
3. 对每个所需的表重复导入过程，指定 **Entity Type Name** 并选择所需字段。

***所需操作:*** 确保在导入过程中正确标记键字段。

| DDIC 结构 | 实体类型名称 | 建议键字段 | 相关负载字段 (示例) |
| :---- | :---- | :---- | :---- |
| `SFLIGHT` | **Flight** | `CARRID`, `CONNID`, `FLDATE` | `PRICE`, `CURRENCY`, `PLANETYPE`, `SEATSMAX`, `SEATSOCC` |
| `SPFLI` | **Connection** | `CARRID`, `CONNID` | `COUNTRYFR`, `CITYFROM`, `AIRPFROM`, `COUNTRYTO`, `CITYTO`, `AIRPTO`, `DEPTIME`, `ARRTIME`, `DISTANCE` |
| `SCARR` | **Airline** | `CARRID` | `CARRNAME`, `CURRCODE`, `URL` |
| `SAIRPORT` | **Airport** | `ID` | `NAME`, `CITY`, `COUNTRY` |
| `SBOOK` | **Booking** | `CARRID`, `CONNID`, `FLDATE`, `BOOKID` | `CUSTOMID`, `CUSTTYPE`, `SMOKER`, `LUGGWEIGHT`, `WUNIT`, `INVOICE`, `CLASS`, `FORCURAM`, `ORDER_DATE` |
| `SCUSTOM` | **Passenger** | `ID` | `NAME`, `FORM`, `STREET`, `POSTCODE`, `CITY`, `COUNTRY`, `PHONE` |

##### 4. 定义关联和导航属性

关联基于键字段链接实体。导航属性允许客户端应用程序轻松遍历这些关系 (例如，使用 `$expand`)。

**逻辑关系:**

* **1:N:** 航空公司 <-> 航班, 航空公司 <-> 连接, 连接 <-> 航班, 航班 <-> 预订, 乘客 <-> 预订.
* **N:1:** 连接 <-> 出发机场, 连接 <-> 到达机场.

**创建关联的步骤:**

1. 右键点击 "Data Model" -> **"Create" -> "Association"**。
2. 定义 **Association Name**, **Principal Entity** ('1' 端), **Dependent Entity** ('多' 端), 和 **Cardinality** (例如 1:N)。
3. 在下一个屏幕中，通过匹配 Principal 和 Dependent 实体之间的键字段来进行 **Specify Key Mapping**。

**要创建的具体关联:**

| 序号 | 关联名称 | Principal:Dependent | 基数 | 键映射 |
| :---- | :---- | :---- | :---- | :---- |
| 1 | `Assoc_Airline_Flights` | `Airline` : `Flight` | 1:N | `Airline.CARRID` <-> `Flight.CARRID` |
| 2 | `Assoc_Airline_Connections` | `Airline` : `Connection` | 1:N | `Airline.CARRID` <-> `Connection.CARRID` |
| 3 | `Assoc_Connection_Flights` | `Connection` : `Flight` | 1:N | `CARRID` & `CONNID` (双向) |
| 4 | `Assoc_Flight_Bookings` | `Flight` : `Booking` | 1:N | `CARRID`, `CONNID`, `FLDATE` (全部 3 个) |
| 5 | `Assoc_Passenger_Bookings` | `Passenger` : `Booking` | 1:N | `Passenger.ID` <-> `Booking.CUSTOMID` |
| 6 | `Assoc_Connection_OriginAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPFROM` <-> `Airport.ID` |
| 7 | `Assoc_Connection_DestAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPTO` <-> `Airport.ID` |

**要创建的导航属性:**

| 实体 | 导航属性名称 | 目标实体 | 使用的关联 |
| :---- | :---- | :---- | :---- |
| **Airline** | `ToFlights`, `ToConnections` | `Flight`, `Connection` | `Assoc_Airline_Flights`, `Assoc_Airline_Connections` |
| **Flight** | `ToAirline`, `ToConnection`, `ToBookings` | `Airline`, `Connection`, `Booking` | `Assoc_Airline_Flights`, `Assoc_Connection_Flights`, `Assoc_Flight_Bookings` |
| **Connection** | `ToAirline`, `ToFlights`, `ToOriginAirport`, `ToDestinationAirport` | `Airline`, `Flight`, `Airport`, `Airport` | `Assoc_Airline_Connections`, `Assoc_Connection_Flights`, `Assoc_Connection_OriginAirport`, `Assoc_Connection_DestAirport` |
| **Booking** | `ToFlight`, `ToPassenger` | `Flight`, `Passenger` | `Assoc_Flight_Bookings`, `Assoc_Passenger_Bookings` |
| **Passenger** | `ToBookings` | `Booking` | `Assoc_Passenger_Bookings` |

##### 5. 生成运行时对象

1. 点击 **"Generate Runtime Objects"** 按钮 (魔术棒图标)。
2. 这将生成模型提供者类 (MPC) 和数据提供者类 (DPC)，它们是 ABAP 类。
3. 接受默认类名或进行调整。

##### 6. 实现数据提供者类 (DPC) 方法

生成的 DPC 扩展类 (例如 `ZCL_Z_TRAVEL_RECOM_DPC_EXT`) 用于您的自定义逻辑。

* 如果直接表映射足够，基本实现可能就足够了。
* 对于自定义过滤、连接、计算或复杂的读取/创建/更新/删除 (CRUD) 操作，您需要在 DPC 扩展类中重新定义方法，如 `*_GET_ENTITY` (单条记录) 和 `*_GET_ENTITYSET` (集合)。

AIRLINESET_GET_ENTITYSET 方法示例:

```abap
METHOD airlineset_get_entityset.
  DATA: lt_airlines TYPE TABLE OF scarr,
        ls_airline TYPE scarr,
        lv_filter_string TYPE string.

  TRY.
      lv_filter_string = io_tech_request_context->get_filter( )->get_filter_string( ).
    CATCH cx_sy_itab_line_not_found.
      CLEAR lv_filter_string.
  ENDTRY.

  " TODO: Apply filtering based on lv_filter_string"
  IF lv_filter_string IS NOT INITIAL.
    SELECT * FROM scarr INTO TABLE lt_airlines WHERE (lv_filter_string).
  ELSE.
    SELECT * FROM scarr INTO TABLE lt_airlines.
  ENDIF.

  LOOP AT lt_airlines INTO ls_airline.
    APPEND ls_airline TO et_entityset.
  ENDLOOP.
ENDMETHOD.
```

##### 7. 注册服务

1. 转到事务 `/IWFND/MAINT_SERVICE`。
2. 点击 **"Add Service"**。
3. 输入后端系统的 **System Alias** (例如 `LOCAL`)。
4. 搜索 **Technical Service Name** (例如 `Z_TRAVEL_RECOMMENDATIONS_SRV`)。
5. 选择服务并点击 **"Add Selected Services"**。
6. 分配包并确认。

##### 8. 激活并测试服务

1. 在 `/IWFND/MAINT_SERVICE` 中，找到新注册的服务。
2. 确保 **ICF Node is Active** (绿灯)。如果不是，选择服务并转到 **"ICF Node" -> "Activate"**。
3. 选择服务并点击 **"SAP Gateway Client"** 按钮。
4. **在 Gateway Client 中测试:**
   * 测试实体集合获取: 点击 **"EntitySets"**，选择一个 EntitySet (例如 `AirlineCollection`) 并点击 **"Execute"**。
   * 测试 OData 功能: 尝试查询选项如 `$filter`，特别是验证导航属性是否工作，使用 **`$expand`** (例如 `/FlightSet(key)?$expand=ToAirline`)。

##### 9. 验证服务 URL

最终的 OData 服务 URL 可以在 Gateway Client 中看到。它通常遵循以下结构:

`/sap/opu/odata/sap/Z_TRAVEL_RECOMMENDATIONS_SRV/.` 这是您的客户端应用程序 (如 Fiori 或自定义移动应用) 将用于使用 SFLIGHT 数据的 URL。

---

## 🚀 快速开始

### MCP 服务器前提条件

#### 系统要求

- **Python 3.11 或更高版本**
- **pip** (Python 包安装程序)
- **Git** (用于克隆仓库)
- SAP Gateway 访问凭据
- 虚拟环境支持

#### 安装 Python

<details>
<summary><b>🪟 Windows</b></summary>

**选项 1: Microsoft Store (推荐 Windows 10/11)**
```powershell
# 在 Microsoft Store 中搜索 "Python 3.11" 或 "Python 3.12"
# 或者从 python.org 下载
```

**选项 2: Python.org 安装程序**
1. 从 [python.org/downloads](https://www.python.org/downloads/) 下载
2. 运行安装程序
3. ✅ **勾选 "Add Python to PATH"**
4. 点击 "Install Now"

**验证安装:**
```powershell
python --version
# 输出: Python 3.11.x 或更高

pip --version
# 输出: pip 23.x.x 或更高
```

**常见问题:**
- 如果找不到 `python` 命令，尝试 `python3` 或 `py`
- 如果找不到 `pip`，安装它: `python -m ensurepip --upgrade`

</details>

<details>
<summary><b>🍎 macOS</b></summary>

**选项 1: Homebrew (推荐)**
```bash
# 如果未安装 Homebrew，请先安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.11
# 或者
brew install python@3.12
```

**选项 2: Python.org 安装程序**
1. 从 [python.org/downloads/macos](https://www.python.org/downloads/macos/) 下载
2. 打开 `.pkg` 文件
3. 按照安装向导操作

**验证安装:**
```bash
python3 --version
# 输出: Python 3.11.x 或更高

pip3 --version
# 输出: pip 23.x.x 或更高
```

**注意:** macOS 可能预装了 Python 2.7。请始终使用 `python3` 和 `pip3` 命令。

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Ubuntu/Debian:**
```bash
# 更新包列表
sudo apt update

# 安装 Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# 或者对于最新的 Python
sudo apt install python3 python3-venv python3-pip
```

**Fedora/RHEL/CentOS:**
```bash
# 安装 Python 3.11+
sudo dnf install python3.11 python3-pip

# 或者
sudo yum install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**验证安装:**
```bash
python3 --version
# 输出: Python 3.11.x 或更高

pip3 --version
# 输出: pip 23.x.x 或更高
```

</details>

---

### 1. 安装

#### 分步安装

<details open>
<summary><b>🪟 Windows (PowerShell/命令提示符)</b></summary>

```powershell
# 克隆仓库
git clone <repository-url>
cd sap-mcp

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate
# 或者在 PowerShell 中:
# .venv\Scripts\Activate.ps1

# 如果 PowerShell 出现执行策略错误:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 验证激活 (提示符中应显示 (.venv))
# (.venv) PS C:\path\to\sap-mcp>

# 安装服务器包
cd packages\server
pip install -e .

# 安装开发依赖 (可选)
pip install -e ".[dev]"

# 验证安装
sap-mcp-server-stdio --help
```

**常见 Windows 问题:**
- **找不到 `python`**: 尝试 `python3` 或 `py`
- **权限被拒绝**: 以管理员身份运行 PowerShell
- **执行策略**: 运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **长路径支持**: 在 Windows 中启用长路径 (设置 > 系统 > 关于 > 高级系统设置)

</details>

<details>
<summary><b>🍎 macOS (终端)</b></summary>

```bash
# 克隆仓库
git clone <repository-url>
cd sap-mcp

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 验证激活 (提示符中应显示 (.venv))
# (.venv) user@macbook sap-mcp %

# 安装服务器包
cd packages/server
pip install -e .

# 安装开发依赖 (可选)
pip install -e ".[dev]"

# 验证安装
sap-mcp-server-stdio --help

# 检查安装路径 (对 Gemini CLI 配置很有用)
which sap-mcp-server-stdio
# 示例输出: /Users/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**常见 macOS 问题:**
- **找不到 `python`**: 改用 `python3`
- **找不到 `pip`**: 改用 `pip3`
- **权限被拒绝**: 不要在虚拟环境中使用 `sudo`
- **安装后找不到命令**: 确保虚拟环境已激活

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 克隆仓库
git clone <repository-url>
cd sap-mcp

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 验证激活 (提示符中应显示 (.venv))
# (.venv) user@linux:~/sap-mcp$

# 安装服务器包
cd packages/server
pip install -e .

# 安装开发依赖 (可选)
pip install -e ".[dev]"

# 验证安装
sap-mcp-server-stdio --help

# 检查安装路径 (对 Gemini CLI 配置很有用)
which sap-mcp-server-stdio
# 示例输出: /home/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**常见 Linux 问题:**
- **找不到 `python3-venv`**: 安装它 `sudo apt install python3-venv`
- **权限被拒绝**: 不要在虚拟环境中使用 `sudo`
- **SSL 错误**: 安装证书: `sudo apt install ca-certificates`
- **缺少构建依赖**: 安装 `sudo apt install build-essential python3-dev`

</details>

---

### 2. 配置

SAP MCP 服务器需要两个配置文件：
1. **`.env.server`**: SAP 连接凭据 (单一 SAP 系统)
2. **`services.yaml`**: SAP Gateway 服务和认证配置

#### 2.1. SAP 连接配置 (`.env.server`)

> **⚠️ 重要**: 从 v0.2.0 开始，`.env.server` 已整合到 **项目根目录**。不再支持之前的 `packages/server/.env.server` 位置。

**文件位置**: `.env.server` 必须位于 **项目根目录**。

```
sap-mcp/
├── .env.server              ← 配置文件 (唯一位置 - 在此创建)
├── .env.server.example      ← 配置模板
├── packages/
│   └── server/
└── README.md
```

**配置步骤**:

<details open>
<summary><b>🪟 Windows (PowerShell/命令提示符)</b></summary>

```powershell
# 进入项目根目录
cd C:\path\to\sap-mcp

# 复制环境模板
copy .env.server.example .env.server

# 用记事本编辑 SAP 凭据
notepad .env.server

# 或者使用您喜欢的编辑器:
# code .env.server (VS Code)
# notepad++ .env.server (Notepad++)

# 注意: Windows 的文件权限管理不同
# 确保文件不在公共文件夹中
# 右键点击 .env.server > 属性 > 安全 以限制访问
```

**Windows 特定说明:**
- 路径使用反斜杠 (`\`)
- PowerShell 执行策略可能会阻止脚本 (见安装部分)
- 将 `.env.server` 保存在受限的用户文件夹中
- 如果防病毒软件阻止文件，请使用 Windows Defender 排除项

</details>

<details>
<summary><b>🍎 macOS (终端)</b></summary>

```bash
# 进入项目根目录
cd /path/to/your/sap-mcp

# 复制环境模板
cp .env.server.example .env.server

# 编辑配置填入 SAP 凭据
nano .env.server
# 或者使用您喜欢的编辑器:
# vim .env.server
# code .env.server (VS Code)
# open -a TextEdit .env.server

# 设置适当的权限 (安全推荐)
chmod 600 .env.server

# 验证权限
ls -la .env.server
# 结果: -rw------- (仅所有者可读写)
```

**macOS 特定说明:**
- 文件权限基于 Unix (与 Linux 相同)
- `chmod 600` 确保只有您的用户可以读写该文件
- macOS 可能会在首次访问时提示额外的安全提示
- 保存在您的主目录中以获得最佳安全性

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 进入项目根目录
cd /path/to/your/sap-mcp

# 复制环境模板
cp .env.server.example .env.server

# 编辑配置填入 SAP 凭据
nano .env.server
# 或者使用您喜欢的编辑器:
# vim .env.server
# code .env.server (VS Code)
# gedit .env.server (GNOME)

# 设置适当的权限 (安全必须)
chmod 600 .env.server

# 验证权限
ls -la .env.server
# 结果: -rw------- (仅所有者可读写)

# 可选: 确保文件不可被所有人读取
stat .env.server
```

**Linux 特定说明:**
- `chmod 600` 对安全性至关重要 (仅所有者可访问)
- SELinux/AppArmor 可能需要额外配置
- 文件应由运行服务器的用户拥有
- 编辑或运行此文件时不要使用 `sudo`

</details>

---

**必需的环境变量**:
```bash
# SAP 系统连接 (单一 SAP 系统)
SAP_HOST=your-sap-host.com          # SAP Gateway 主机名
SAP_PORT=443                         # HTTPS 端口 (通常为 443 或 8443)
SAP_USERNAME=your-username           # SAP 用户 ID
SAP_PASSWORD=your-password           # SAP 密码
SAP_CLIENT=100                       # SAP 客户端编号 (例如 100, 800)

# 安全设置
SAP_VERIFY_SSL=false                 # 启用 SSL 证书验证 (推荐)
SAP_TIMEOUT=30                       # 请求超时 (秒)

# 可选: 连接池
SAP_MAX_CONNECTIONS=10               # 最大并发连接数 (可选)
SAP_RETRY_ATTEMPTS=3                 # 失败重试次数 (可选)
```

**安全最佳实践**:
- ✅ 不要将 `.env.server` 提交到版本控制 (已在 `.gitignore` 中)
- ✅ 使用强且唯一的密码
- ✅ 在生产环境中启用 SSL 验证 (`SAP_VERIFY_SSL=true`)
- ✅ 限制文件权限: `chmod 600 .env.server`

#### 2.2. SAP Gateway 服务配置 (`services.yaml`)

配置 MCP 服务器可以访问哪些 SAP Gateway 服务 (OData 服务)。

**位置**: `packages/server/config/services.yaml`

```bash
# 复制示例配置
cp packages/server/config/services.yaml.example packages/server/config/services.yaml

# 编辑服务配置
vim packages/server/config/services.yaml
```

**基本配置示例**:

```yaml
# Gateway URL 配置
gateway:
  # OData 服务的基础 URL 模式
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"

  # 元数据端点后缀
  metadata_suffix: "/$metadata"

  # 服务目录路径
  service_catalog_path: "/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection"

  # 认证端点配置
  auth_endpoint:
    # 推荐: 使用目录元数据 (无需特定服务即可工作)
    use_catalog_metadata: true

    # 可选: 使用特定服务进行认证 (如果目录不可用)
    # use_catalog_metadata: false
    # service_id: Z_TRAVEL_RECOMMENDATIONS_SRV
    # entity_name: AirlineSet

# SAP OData 服务
services:
  # SFLIGHT 演示服务 (旅行推荐)
  - id: Z_TRAVEL_RECOMMENDATIONS_SRV
    name: "Travel Recommendations Service (SFLIGHT)"
    path: "/SAP/Z_TRAVEL_RECOMMENDATIONS_SRV"
    version: v2
    description: "OData service for the SFLIGHT demo dataset."
    entities:
      - name: AirlineSet
        key_field: CARRID
        description: "Airlines (e.g., LH, AA)"
        default_select:
          - CARRID
          - CARRNAME
          - CURRCODE
          - URL
      - name: AirportSet
        key_field: ID
        description: "Airports (e.g., FRA, JFK)"
        default_select:
          - ID
          - NAME
          - CITY
          - COUNTRY
      - name: FlightSet
        key_field: "CARRID='{CARRID}',CONNID='{CONNID}',FLDATE=datetime'{FLDATE}'"
        description: "Specific flights on a given date"
      - name: BookingSet
        key_field: "CARRID='{CARRID}',CONNID='{CONNID}',FLDATE=datetime'{FLDATE}',BOOKID='{BOOKID}'"
        description: "Individual flight bookings"

    # 可选: 此服务的自定义标头
    custom_headers: {}
```

#### 2.3. 认证端点选项

`auth_endpoint` 设置控制 MCP 服务器如何向 SAP 进行认证。

**选项 1: 目录元数据 (推荐)**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: true
```

**优点**:
- ✅ 无需特定 SAP Gateway 服务即可工作
- ✅ 跨 SAP 系统高度灵活和可移植
- ✅ 认证不依赖于服务
- ✅ 不依赖于自定义服务的部署

**认证流程**:
- CSRF 令牌: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection`
- 验证: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**选项 2: 特定服务认证**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: false
    service_id: Z_TRAVEL_RECOMMENDATIONS_SRV    # 必须匹配下面的服务 ID
    entity_name: AirlineSet                     # 必须是该服务的实体
```

**优点**:
- ✅ 明确的基于服务的认证
- ✅ 如果目录服务不可用 (罕见) 可以工作

**缺点**:
- ❌ 需要部署指定的服务
- ❌ 服务更改时灵活性较低
- ❌ 如果服务名称更改需要更新配置

**认证流程**:
- CSRF 令牌: `/SAP/Z_TRAVEL_RECOMMENDATIONS_SRV/AirlineSet`
- 验证: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**建议**: 除非有特定原因需要使用特定服务进行认证，否则请使用 **选项 1 (目录元数据)**。

### 3. 运行服务器

<details open>
<summary><b>🪟 Windows (PowerShell/命令提示符)</b></summary>

```powershell
# 激活虚拟环境
.venv\Scripts\activate
# 或者在 PowerShell 中:
# .venv\Scripts\Activate.ps1

# 运行 stdio 服务器 (推荐)
sap-mcp-server-stdio

# 或者直接用 python 运行
python -m sap_mcp_server.transports.stdio

# 完成后停用
deactivate
```

**Windows 特定说明:**
- 路径使用反斜杠 (`\`)
- 可能需要更改 PowerShell 执行策略
- 服务器在当前终端窗口中运行
- 按 `Ctrl+C` 停止服务器

</details>

<details>
<summary><b>🍎 macOS (终端)</b></summary>

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行 stdio 服务器 (推荐)
sap-mcp-server-stdio

# 或者直接用 python 运行
python3 -m sap_mcp_server.transports.stdio

# 完成后停用
deactivate
```

**macOS 特定说明:**
- 使用 `python3` 而不是 `python`
- 服务器在当前终端会话中运行
- 按 `Cmd+C` 或 `Ctrl+C` 停止服务器
- 服务器运行时必须保持终端打开

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行 stdio 服务器 (推荐)
sap-mcp-server-stdio

# 或者直接用 python 运行
python3 -m sap_mcp_server.transports.stdio

# 完成后停用
deactivate
```

**Linux 特定说明:**
- 使用 `python3` 而不是 `python`
- 服务器在当前终端会话中运行
- 按 `Ctrl+C` 停止服务器
- 可以使用 `nohup` 或 `systemd` 服务在后台运行

</details>

---

## 🤖 与 Gemini CLI 集成

> **📖 官方文档**: 有关 Gemini CLI 的更多信息，请访问 <a href="https://geminicli.com/" target="_blank">https://geminicli.com/</a>。

### 前提条件

- 已安装 Node.js 18+ 和 npm
- 已安装 SAP MCP 服务器 (见上文安装部分)
- 用于 Gemini API 访问的 Google 帐户

### 1. 安装 Gemini CLI

```bash
# 全局安装 Gemini CLI
npm install -g @google/gemini-cli

# 验证安装
gemini --version
```

### 2. Gemini CLI 认证

**选项 A: 使用 Gemini API 密钥 (推荐用于入门)**

1. 从 [Google AI Studio](https://aistudio.google.com/apikey) 获取 API 密钥
2. 设置环境变量:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**选项 B: 使用 Google Cloud (用于生产)**

```bash
# 首先安装 Google Cloud CLI
gcloud auth application-default login

# 设置项目
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### 3. 注册 SAP MCP 服务器

**方法 A: 使用绝对路径 (推荐用于虚拟环境)**

如果您在虚拟环境中安装了服务器，请使用可执行文件的绝对路径:

1. **查找绝对路径**:
```bash
# 进入 SAP MCP 目录
cd /path/to/your/sap-mcp

# 获取完整路径
pwd
# 示例输出: /path/to/your/sap-mcp
```

2. **编辑 `~/.gemini/settings.json`**:
```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "cwd": "/path/to/your/sap-mcp",
      "description": "SAP Gateway MCP Server for OData integration",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

**将 `/path/to/your/sap-mcp` 替换为您的实际项目路径。**

> **📝 注意**: `cwd` (当前工作目录) 参数对于定位 `.env.server` 文件 **至关重要**。您 **必须** 将其设置为项目根目录 (例如 `/Users/username/projects/sap-mcp`)。如果省略或错误，服务器将无法加载凭据。

3. **验证路径**:
```bash
# 测试命令是否工作
/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio --help

# 验证注册
gemini mcp list
# 预期结果: ✓ sap-server: ... (stdio) - Connected
```

---

**方法 B: 使用 CLI 命令 (如果全局安装)**

如果 `sap-mcp-server-stdio` 在您的系统 PATH 中:

```bash
# 注册服务器
gemini mcp add sap-server sap-mcp-server-stdio

# 验证注册
gemini mcp list
```

**注意**: 仅当您已将虚拟环境添加到 PATH 或全局安装了包时，此方法才有效。

---

**方法 C: 使用 Python 模块路径**

使用 Python 模块的替代方法:

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/python",
      "args": ["-m", "sap_mcp_server.transports.stdio"],
      "cwd": "/path/to/your/sap-mcp/packages/server",
      "description": "SAP Gateway MCP Server",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

### 4. 开始在 Gemini CLI 中使用 SAP MCP

```bash
# 启动 Gemini CLI
gemini

# 检查 MCP 服务器状态
> /mcp

# 列出可用 SAP 工具
> /mcp desc

# 示例: 查询 SAP 航空公司
> Use the SAP tools to authenticate and show me all airlines

# 示例: 列出可用 SAP 服务
> What SAP services are available?

# 示例: 获取机场详情
> Retrieve details for Frankfurt airport (FRA)
```

### 高级配置

**启用受信任服务器的自动批准**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "trust": true,
      "timeout": 30000
    }
  }
}
```

**注意**: 设置 `"trust": true` 以跳过每个工具调用的批准提示。仅对受信任的服务器启用。

---

**过滤特定工具**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "includeTools": ["sap_authenticate", "sap_query"],
      "excludeTools": ["sap_list_services"],
      "timeout": 30000
    }
  }
}
```

**用例**:
- `includeTools`: 仅允许特定工具 (白名单)
- `excludeTools`: 阻止特定工具 (黑名单)
- 不能同时使用

---

**添加环境变量 (可选)**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "env": {
        "SAP_HOST": "${SAP_HOST}",
        "SAP_USERNAME": "${SAP_USERNAME}",
        "SAP_PASSWORD": "${SAP_PASSWORD}"
      },
      "timeout": 30000
    }
  }
}
```

**注意**: `settings.json` 中的环境变量会覆盖 `.env.server` 中的值。出于安全原因不推荐 - 建议使用 `.env.server` 文件。

---

**增加慢速网络的超时时间**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "timeout": 60000,  // 60 秒 (默认: 30000)
      "trust": false
    }
  }
}
```

**何时增加**:
- 慢速网络连接
- 大型数据查询
- 复杂的 SAP 操作
- 频繁的超时错误

### 故障排除

**问题: 服务器显示 "Disconnected" 状态**

```bash
# 检查 MCP 服务器状态
gemini mcp list
# 显示: ✗ sap-server: sap-mcp-server-stdio (stdio) - Disconnected
```

**解决方案 1: 使用绝对路径 (最常见)**

命令可能在虚拟环境中。更新 `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "description": "SAP Gateway MCP Server",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

**查找绝对路径**:
```bash
# 进入 SAP MCP 目录
cd /path/to/your/sap-mcp

# 获取完整路径
pwd
# 示例: /path/to/your/sap-mcp

# 验证命令存在
ls -la .venv/bin/sap-mcp-server-stdio
```

---

**问题: PATH 中找不到命令**

```bash
# 直接测试服务器
sap-mcp-server-stdio
# 错误: command not found

# 检查命令位置
which sap-mcp-server-stdio
# 返回: command not found
```

**解决方案 2: 检查虚拟环境**

```bash
# 检查虚拟环境是否存在
ls -la .venv/bin/sap-mcp-server-stdio

# 如果存在，在 settings.json 中使用绝对路径
# 如果不存在，重新安装:
cd packages/server
pip install -e .
```

---

**问题: 认证错误或找不到 `.env.server`**

```bash
# 检查 .env.server 是否在项目根目录 (不是 packages/server/)
cat .env.server

# 必需字段:
# SAP_HOST=your-host
# SAP_PORT=443
# SAP_USERNAME=your-username
# SAP_PASSWORD=your-password
# SAP_CLIENT=100
```

**解决方案 3: 验证文件位置和凭据**

```bash
# 1. 验证 .env.server 在项目根目录
ls -la .env.server
# 应该在: /path/to/sap-mcp/.env.server

# 2. 检查 Gemini CLI settings.json 是否有 "cwd" 参数
cat ~/.gemini/settings.json
# 应该包含: "cwd": "/path/to/sap-mcp"

# 3. 手动测试认证
source .venv/bin/activate
python -c "from sap_mcp_server.config.settings import get_connection_config; print(get_connection_config())"
```

**常见问题**:

1. **"Field required" 错误**: `.env.server` 未加载。检查:
   - 文件在项目根目录: `/path/to/your/sap-mcp/.env.server`
   - Gemini CLI `settings.json` 有正确的 `cwd` 参数
   - 文件有适当的权限: `chmod 600 .env.server`

2. **401 Unauthorized 错误**: v0.2.1 (2025-01-22) 已修复
   - **以前的问题**: SAP Gateway 拒绝没有 `sap-client` 参数的请求
   - **当前状态**: 自动处理 - 所有请求都包含 `sap-client` 参数
   - **验证**: 确保您已更新到 v0.2.1 或更高版本
   - **手动检查**: 凭据有效时认证应该成功

---

**问题: 需要重新注册服务器**

```bash
# 删除现有服务器配置
rm ~/.gemini/settings.json

# 或者手动编辑并删除 sap-server 条目
```

**解决方案 4: 全新重新注册**

```bash
# 方法 1: 直接编辑设置
vim ~/.gemini/settings.json

# 方法 2: 使用绝对路径 (推荐)
# 遵循上面第 3 节 "方法 A: 使用绝对路径"
```

---

**快速诊断步骤**

1. **检查服务器可执行文件**:
```bash
/path/to/sap-mcp/.venv/bin/sap-mcp-server-stdio --help
# 应该显示服务器启动消息
```

2. **检查 Gemini CLI 设置**:
```bash
cat ~/.gemini/settings.json | grep -A 5 "sap-server"
# 验证 "command" 路径是否正确
```

3. **测试连接**:
```bash
gemini mcp list
# 显示: ✓ sap-server: ... - Connected
```

4. **在 Gemini CLI 中测试**:
```bash
gemini
> /mcp
> /mcp desc
# 应该列出 SAP 工具
```

### Gemini CLI 中可用的 SAP 工具

注册后，您可以通过自然语言使用以下 SAP 工具：

| 工具 | 描述 | 示例提示 |
|------|-------------|----------------|
| **sap_authenticate** | 在 SAP Gateway 系统中认证 | "Authenticate with SAP" |
| **sap_query** | 使用 OData 过滤器查询 SAP 实体 | "Use the travel recommendations service to show me all airlines" |
| **sap_get_entity** | 通过键获取特定实体 | "Retrieve details for Frankfurt airport (FRA)" |
| **sap_list_services** | 列出可用 SAP 服务 | "What SAP services are available?" |

### 工作流示例

**1. 航班查询工作流**

```bash
gemini

> Connect to SAP and find all Lufthansa flights
# Gemini 将执行:
# 1. 调用 sap_authenticate
# 2. 调用 sap_query 查询 FlightSet，过滤器为 "CARRID eq 'LH'"
# 3. 格式化并显示结果
```

**2. 机场分析**

```bash
> Get details for Frankfurt airport and show me available connections
# Gemini 将执行:
# 1. 认证
# 2. 调用 sap_get_entity 查询 AirportSet，键为 'FRA'
# 3. 调用 sap_query 查询 ConnectionSet
# 4. 呈现见解
```

**3. 服务发现**

```bash
> What SAP services and entity sets are available in the system?
# Gemini 将执行:
# 1. 调用 sap_list_services
# 2. 格式化服务目录
```

---

## 🔧 可用工具

### 1. SAP 认证 (sap_authenticate)

使用 `.env.server` 中的凭据在 SAP Gateway 系统中进行认证。

**请求**:
```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "abc123...",
  "message": "Successfully authenticated with SAP Gateway",
  "host": "example.sap.corp",
  "client": "100"
}
```

---

### 2. SAP 查询 (sap_query)

使用 OData 过滤器、选择和分页查询 SAP 实体。

**请求**:
```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_TRAVEL_RECOMMENDATIONS_SRV",
    "entity_set": "AirlineSet",
    "filter": "CARRID eq 'LH'",
    "select": "CARRID,CARRNAME,CURRCODE",
    "top": 10,
    "skip": 0
  }
}
```

**响应**:
```json
{
  "d": {
    "results": [
      {
        "CARRID": "LH",
        "CARRNAME": "Lufthansa",
        "CURRCODE": "EUR"
      }
    ]
  }
}
```

---

### 3. SAP 实体获取 (sap_get_entity)

通过键获取特定实体。

**请求**:
```json
{
  "name": "sap_get_entity",
  "arguments": {
    "service": "Z_TRAVEL_RECOMMENDATIONS_SRV",
    "entity_set": "AirportSet",
    "entity_key": "'FRA'"
  }
}
```

**响应**:
```json
{
  "success": true,
  "service": "Z_TRAVEL_RECOMMENDATIONS_SRV",
  "entity_set": "AirportSet",
  "entity_key": "'FRA'",
  "key_field": "ID",
  "data": {
    "d": {
      "ID": "FRA",
      "NAME": "Frankfurt International",
      "CITY": "Frankfurt",
      "COUNTRY": "DE",
      "TIME_ZONE": "CET"
    }
  }
}
```

---

### 4. SAP 服务列表 (sap_list_services)

列出配置中所有可用的 SAP 服务。

**请求**:
```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

**响应**:
```json
{
  "success": true,
  "count": 1,
  "services": [
    {
      "id": "Z_TRAVEL_RECOMMENDATIONS_SRV",
      "name": "Travel Recommendations Service (SFLIGHT)",
      "path": "/SAP/Z_TRAVEL_RECOMMENDATIONS_SRV",
      "version": "v2",
      "description": "OData service for the SFLIGHT demo dataset.",
      "entities": [
        {
          "name": "AirlineSet",
          "key_field": "CARRID",
          "description": "Airlines (e.g., LH, AA)"
        },
        {
          "name": "AirportSet",
          "key_field": "ID",
          "description": "Airports (e.g., FRA, JFK)"
        }
      ]
    }
  ],
  "source": "services.yaml configuration"
}
```

---

### 5. 添加新工具

1. **创建工具文件**: `packages/server/src/sap_mcp_server/tools/my_tool.py`

```python
from .base import MCPTool

class MyNewTool(MCPTool):
    @property
    def name(self) -> str:
        return "my_new_tool"

    @property
    def description(self) -> str:
        return "Description of my new tool"

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            },
            "required": ["param"]
        }

    async def execute(self, params: dict) -> dict:
        # Implementation
        return {"result": "success"}
```

2. **注册工具**: 更新 `packages/server/src/sap_mcp_server/tools/__init__.py`

```python
from .my_tool import MyNewTool

# Add to registry
tool_registry.register(MyNewTool())
```

3. **添加测试**: `tests/unit/test_my_tool.py`

```python
import pytest
from sap_mcp_server.tools.my_tool import MyNewTool

@pytest.mark.asyncio
async def test_my_tool():
    tool = MyNewTool()
    result = await tool.execute({"param": "value"})
    assert result["result"] == "success"
```

---

## 📚 使用示例

### 使用工具注册表

```python
from sap_mcp_server.tools import tool_registry
from sap_mcp_server.protocol.schemas import ToolCallRequest

# 列出可用工具
tools = tool_registry.list_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")

# 调用工具
request = ToolCallRequest(
    name="sap_list_services",
    arguments={}
)
result = await tool_registry.call_tool(request)
print(result)
```

### MCP 客户端示例

```python
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    # 连接到 MCP 服务器
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()

            # 认证
            auth_result = await session.call_tool("sap_authenticate", {})

            # 查询航空公司
            entity_result = await session.call_tool(
                "sap_query",
                {
                    "service": "Z_TRAVEL_RECOMMENDATIONS_SRV",
                    "entity_set": "AirlineSet",
                    "filter": "CARRID eq 'LH'"
                }
            )
            print(entity_result)
```

### 结构化日志

```python
from sap_mcp_server.utils.logger import setup_logging, get_logger

# 生产环境 (JSON 日志)
setup_logging(level="INFO", json_logs=True)

# 开发环境 (彩色控制台)
setup_logging(level="DEBUG", json_logs=False)

# 使用日志记录器
logger = get_logger(__name__)
logger.info("Server started", port=8080, transport="stdio")
logger.error("Query failed", error=str(e), query=params)
```

### 输入验证

```python
from sap_mcp_server.utils.validators import (
    validate_odata_filter,
    validate_entity_key,
    sanitize_input
)

# 验证 OData 过滤器
if validate_odata_filter("CARRID eq 'LH'"):
    # 执行安全
    pass

# 清理用户输入
safe_input = sanitize_input(user_data, max_length=1000)

# 验证实体键
if validate_entity_key(key):
    # 获取实体
    pass
```

---

## 🔒 安全

### 纵深防御

| 层 | 实现 | 状态 |
|-------|---------------|--------|
| **输入验证** | OData 语法, SQL 注入防护 | ✅ |
| **认证** | 凭据验证, 会话管理 | ✅ |
| **授权** | 服务访问控制 | ✅ |
| **传输安全** | SSL/TLS, 证书验证 | ✅ |
| **审计日志** | 结构化日志, 无敏感数据 | ✅ |

### 最佳实践

1. **凭据**: 存储在 `.env.server` 中，不要提交到 git
2. **SSL/TLS**: 在生产环境中始终启用 (`SAP_VERIFY_SSL=true`)
3. **验证**: 在 SAP 调用之前验证所有输入
4. **日志**: 从日志中排除敏感数据
5. **错误处理**: 向客户端提供通用错误消息

---

---

## 📖 文档

### 📚 指南

- **[配置指南](./docs/guides/configuration.md)**: YAML 和环境配置的完整指南
- **[部署指南](./docs/guides/deployment.md)**: 生产部署最佳实践
- **[故障排除指南](./docs/guides/troubleshooting.md)**: 常见问题和解决方案
- **[OData 服务创建指南](./docs/guides/odata-service-creation-flight-demo.md)**: SFLIGHT OData 服务创建分步指南
- **[SFLIGHT 演示指南](./docs/guides/sfight-demo-guide.md)**: 使用 SFLIGHT 演示场景

### 🏗️ 架构

- **[服务器架构](./docs/architecture/server.md)**: 详细的系统架构和设计模式

### 📦 包文档

- **[服务器包 README](./packages/server/README.md)**: 服务器包特定文档

### 🌐 多语言支持

- **[English](./README.md)**: 主文档 (本文档)
- **[日本語 (Japanese)](./README.ja.md)**: 日语文档
- **[한국어 (Korean)](./README.ko.md)**: 韩语文档
- **[ไทย (Thai)](./README.th.md)**: 泰语文档
- **[繁體中文 (Traditional Chinese)](./README.zh-TW.md)**: 繁体中文文档
- **[简体中文 (Simplified Chinese)](./README.zh-CN.md)**: 简体中文文档
- **[Español (Spanish)](./README.es.md)**: 西班牙语文档

---

## 📝 许可证

MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **MCP 协议**: Anthropic 的模型上下文协议
- **SAP Gateway**: OData v2/v4 集成
- **社区**: 贡献者和测试者

---

<div align="center">

**Built with ❤️ for SAP integration via Model Context Protocol**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

**Production Ready** | **56% Coverage** | **98% Test Success**

</div>

