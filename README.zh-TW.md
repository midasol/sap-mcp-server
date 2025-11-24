# SAP MCP - 透過 Model Context Protocol 整合 SAP Gateway

一個完整的 MCP 伺服器，用於整合 SAP Gateway，提供模組化工具讓 AI 代理執行 SAP OData 操作。

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

</div>

---

## 🎯 專案概覽

一個生產就緒的 Model Context Protocol (MCP) 伺服器，使 AI 代理和應用程式能夠透過乾淨、模組化的架構與 SAP Gateway 系統互動。專為可靠性、安全性和開發者體驗而建構。

**當前狀態**: ✅ **生產就緒** (所有 5 個階段已完成)

### 關鍵亮點

- 🔐 **安全的 SAP 整合**: 企業級驗證與 SSL/TLS 支援
- 🛠️ **4 個模組化工具**: 驗證、查詢、實體檢索、服務發現
- 🚀 **Stdio 傳輸**: 生產級 MCP 伺服器
- 📊 **結構化日誌**: JSON 和控制台格式，包含效能指標
- ✅ **驗證**: 全面的 OData 和安全驗證
- 🧪 **經過良好測試**: 56% 覆蓋率，44/45 測試通過 (98% 成功率)

---

## 📐 架構

### 系統概覽

<details>
<summary>📊 點擊查看系統概覽圖</summary>

```mermaid
graph TB
    subgraph clients["🎯 客戶端應用程式"]
        direction TB
        A1["AI Agent<br/><small>LLM/GenAI Integration</small>"]
        A2["Python Client<br/><small>SDK & Libraries</small>"]
        A3["Order Chatbot<br/><small>範例應用程式</small>"]
    end

    subgraph transport["🚀 MCP 伺服器層"]
        direction TB
        B1["Stdio Transport<br/><small>stdin/stdout Stream</small>"]
    end

    subgraph registry["🛠️ 工具註冊表"]
        direction LR
        C1["sap_authenticate<br/><small>驗證</small>"]
        C2["sap_query<br/><small>OData Queries</small>"]
        C3["sap_get_entity<br/><small>實體檢索</small>"]
        C4["sap_list_services<br/><small>服務發現</small>"]
    end

    subgraph core["⚡ 核心層"]
        direction LR
        D1["SAP Client<br/><small>OData Handler</small>"]
        D2["Auth Manager<br/><small>Credentials</small>"]
        D3["Config Loader<br/><small>YAML/ENV</small>"]
    end

    subgraph utils["🔧 工具程式"]
        direction LR
        E1["Validators<br/><small>Input/Security</small>"]
        E2["Logger<br/><small>Structured Logs</small>"]
        E3["Error Handler<br/><small>Production Grade</small>"]
    end

    subgraph sap["🏢 SAP Gateway"]
        direction TB
        F1["OData Services<br/><small>v2/v4 Protocol</small>"]
        F2["Business Data<br/><small>Orders/Sales/Inventory</small>"]
    end

    A1 & A2 & A3 -->|Active Connection| B1
    B1 -->|Tool Dispatch| C1 & C2 & C3 & C4
    C1 & C2 & C3 & C4 -->|Core Services| D1
    C1 -->|Auth Flow| D2
    C2 & C3 & C4 -->|Config Access| D3
    D1 & D2 & D3 -->|Validation & Logging| E1 & E2 & E3
    D1 -->|OData Protocol| F1
    F1 -->|Data Access| F2

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

### 元件詳情

<details>
<summary>🔧 點擊查看元件詳情圖</summary>

```mermaid
graph TB
    subgraph pkg["📦 packages/server/src/sap_mcp_server"]
        direction TB

        subgraph trans["🚀 transports/"]
            direction LR
            T1["stdio.py<br/><small>CLI Entry Point</small>"]
        end

        subgraph tools["🛠️ tools/"]
            direction TB
            TO5["base.py<br/><small>Tool Base Class</small>"]

            subgraph toolImpl["Tool Implementations"]
                direction LR
                TO1["auth_tool.py<br/><small>Authentication</small>"]
                TO2["query_tool.py<br/><small>OData Query</small>"]
                TO3["entity_tool.py<br/><small>Single Entity</small>"]
                TO4["service_tool.py<br/><small>Service List</small>"]
            end
        end

        subgraph core["⚡ core/"]
            direction LR
            C1["sap_client.py<br/><small>OData Client</small>"]
            C2["auth.py<br/><small>Auth Manager</small>"]
            C3["exceptions.py<br/><small>Custom Errors</small>"]
        end

        subgraph config["⚙️ config/"]
            direction LR
            CF1["settings.py<br/><small>Env Config</small>"]
            CF2["loader.py<br/><small>YAML Loader</small>"]
            CF3["schemas.py<br/><small>Pydantic Models</small>"]
        end

        subgraph utils["🔧 utils/"]
            direction LR
            U1["logger.py<br/><small>Structured Logs</small>"]
            U2["validators.py<br/><small>Input Validation</small>"]
        end

        subgraph protocol["📡 protocol/"]
            P1["schemas.py<br/><small>MCP Request/Response</small>"]
        end
    end

    T1 -->|Dispatches to| TO1 & TO2 & TO3 & TO4
    TO1 & TO2 & TO3 & TO4 -.->|Extends| TO5
    TO5 -->|Uses| C1 & C2
    C1 -->|Loads| CF1 & CF2
    C2 -->|Reads| CF1
    C1 & C2 -->|Validates & Logs| U1 & U2
    TO5 -.->|Implements| P1
    C3 -.->|Error Types| C1 & C2

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

### 資料流：訂單查詢範例

<details>
<summary>🔄 點擊查看資料流圖</summary>

```mermaid
sequenceDiagram
    autonumber
    box rgba(214, 234, 248, 0.3) Client Layer
        participant Client as 🤖<br/>AI Agent/Client
    end
    box rgba(213, 245, 227, 0.3) Transport Layer
        participant Transport as 📡<br/>Stdio Transport
        participant Registry as 📋<br/>Tool Registry
    end
    box rgba(252, 243, 207, 0.3) Tool Layer
        participant AuthTool as 🔐<br/>Auth Tool
        participant QueryTool as 🔍<br/>Query Tool
    end
    box rgba(250, 219, 216, 0.3) Core Layer
        participant SAPClient as 🔧<br/>SAP Client
    end
    box rgba(213, 245, 227, 0.3) Support Layer
        participant Validator as ✅<br/>Validator
        participant Logger as 📊<br/>Logger
    end
    box rgba(235, 222, 240, 0.3) External
        participant SAP as 🏢<br/>SAP Gateway
    end

    rect rgba(214, 234, 248, 0.15)
        Note over Client,Registry: ⚡ Phase 1: Session Initialization
        Client->>+Transport: Connect via stdio stream
        Transport->>+Registry: Initialize tool registry
        Registry-->>-Transport: ✅ 4 tools registered
        Transport-->>-Client: Connection established
    end

    rect rgba(213, 245, 227, 0.15)
        Note over Client,SAP: 🔐 Phase 2: Authentication
        Client->>+Transport: call_tool(sap_authenticate, {})
        Transport->>+Registry: Get tool: sap_authenticate
        Registry->>+AuthTool: Execute authentication
        AuthTool->>+Validator: Validate credentials
        Validator-->>-AuthTool: ✅ Credentials valid
        AuthTool->>+Logger: Log authentication attempt
        Logger-->>-AuthTool: Logged
        AuthTool->>+SAPClient: Authenticate with SAP
        SAPClient->>+SAP: POST /sap/opu/odata/auth
        SAP-->>-SAPClient: 200 OK + Session token
        SAPClient-->>-AuthTool: ✅ Authenticated successfully
        AuthTool-->>-Registry: Success response
        Registry-->>-Transport: Auth token + session ID
        Transport-->>-Client: ✅ Authentication complete
    end

    rect rgba(252, 243, 207, 0.15)
        Note over Client,SAP: 🔍 Phase 3: Query Execution
        Client->>+Transport: call_tool(sap_query, {filter: "OrderID eq '91000043'"})
        Transport->>+Registry: Get tool: sap_query
        Registry->>+QueryTool: Execute with parameters
        QueryTool->>+Validator: Validate OData filter syntax
        Validator-->>-QueryTool: ✅ Filter is safe
        QueryTool->>+Logger: Log query start
        Logger-->>-QueryTool: Logged
        QueryTool->>+SAPClient: Execute OData query
        SAPClient->>+SAP: GET /OrderSet?$filter=OrderID eq '91000043'
        SAP-->>-SAPClient: 200 OK + Order data (JSON)
        SAPClient->>SAPClient: Parse & transform response
        SAPClient-->>-QueryTool: ✅ Parsed order data
        QueryTool->>+Logger: Log query success + metrics
        Logger-->>-QueryTool: Logged
        QueryTool-->>-Registry: Order details
        Registry-->>-Transport: Formatted response
        Transport-->>-Client: ✅ Query complete
    end

    rect rgba(213, 245, 227, 0.15)
        Note over Logger: 📊 Phase 4: Performance Tracking
        Logger->>Logger: Calculate execution metrics
        Logger->>Logger: Write structured JSON log
        Logger->>Logger: Update performance counters
    end
```

</details>

### 工具執行流程

<details>
<summary>⚡ 點擊查看工具執行流程圖</summary>

```mermaid
flowchart TD
    Start([🚀 Client Request<br/><small>Tool invocation</small>])

    Start --> Validate{🔍 Validate Input<br/><small>Schema check</small><br/><small>Security scan</small>}

    Validate -->|❌ Invalid| Error1[🚫 Validation Error<br/><small>Return error details</small>]
    Validate -->|✅ Valid| Auth{🔐 Authenticated?<br/><small>Session check</small>}

    Auth -->|No| DoAuth[🔑 Execute Auth<br/><small>Credential validation</small><br/><small>SAP handshake</small>]
    DoAuth --> AuthCheck{✅ Auth Success?<br/><small>Token received</small>}

    AuthCheck -->|❌ Failed| Error2[🚫 Auth Error<br/><small>Invalid credentials</small>]
    AuthCheck -->|✅ Success| Execute

    Auth -->|Yes| Execute[⚡ Execute Tool<br/><small>Business logic</small><br/><small>Parameter processing</small>]

    Execute --> SAPCall[🌐 SAP OData Call<br/><small>HTTP request</small><br/><small>SSL/TLS encrypted</small>]

    SAPCall --> SAPCheck{📡 SAP Response<br/><small>Status check</small>}

    SAPCheck -->|❌ Error| Error3[🚫 SAP Error<br/><small>Service unavailable</small><br/><small>or data error</small>]
    SAPCheck -->|✅ 200 OK| Parse[📊 Parse Response<br/><small>XML/JSON parsing</small><br/><small>Data extraction</small>]

    Parse --> Transform[🔄 Transform Data<br/><small>MCP format</small><br/><small>Schema mapping</small>]

    Transform --> Log[📝 Log Metrics<br/><small>Performance data</small><br/><small>Audit trail</small>]

    Log --> Success([✅ Success Response<br/><small>Return to client</small>])

    Error1 & Error2 & Error3 --> LogError[📝 Log Error<br/><small>Error context</small><br/><small>Stack trace</small>]

    LogError --> End([❌ Error Response<br/><small>Return to client</small>])

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

### 安全架構

<details>
<summary>🔒 點擊查看安全架構圖</summary>

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'14px', 'fontFamily':'arial'}}}%%
graph TB
    subgraph security["🛡️ Defense in Depth Security Architecture"]
        direction TB

        subgraph layer1["Layer 1: Input Validation - Entry Point Security"]
            direction LR
            L1A["🔍 OData Filter<br/><br/>SQL injection<br/>prevention<br/><br/>Syntax validation"]
            L1B["🔑 Entity Key<br/><br/>Format<br/>validation<br/><br/>Type checking"]
            L1C["🧹 Sanitization<br/><br/>XSS<br/>prevention<br/><br/>Input cleaning"]
        end

        subgraph layer2["Layer 2: Authentication - Identity Verification"]
            direction LR
            L2A["✅ Credentials<br/><br/>User<br/>validation<br/><br/>Password checks"]
            L2B["🎫 Sessions<br/><br/>Session<br/>lifecycle<br/><br/>Timeout handling"]
            L2C["🔐 Tokens<br/><br/>JWT/Bearer<br/>tokens<br/><br/>Token rotation"]
        end

        subgraph layer3["Layer 3: Authorization - Access Control"]
            direction LR
            L3A["🚦 Service Access<br/><br/>Service-level<br/>RBAC<br/><br/>Permission matrix"]
            L3B["📋 Entity Permissions<br/><br/>Data-level<br/>access<br/><br/>Field filtering"]
        end

        subgraph layer4["Layer 4: Transport Security - Encryption Layer"]
            direction LR
            L4A["🔒 SSL/TLS<br/><br/>TLS 1.2+ only<br/><br/>Perfect forward<br/>secrecy"]
            L4B["📜 Certificates<br/><br/>Chain<br/>validation<br/><br/>Revocation check"]
        end

        subgraph layer5["Layer 5: Audit & Monitoring - Observability"]
            direction LR
            L5A["📊 Structured Logs<br/><br/>JSON logging<br/><br/>PII exclusion"]
            L5B["⚡ Performance<br/><br/>Metrics<br/>tracking<br/><br/>SLA monitoring"]
            L5C["🚨 Error Tracking<br/><br/>Exception<br/>logging<br/><br/>Alert triggers"]
        end
    end

    L1A & L1B & L1C -->|Validated Input| L2A
    L2A -->|Identity Verified| L2B
    L2B -->|Session Active| L2C
    L2C -->|Authenticated| L3A & L3B
    L3A & L3B -->|Authorized| L4A & L4B
    L4A & L4B -->|Encrypted| L5A & L5B & L5C

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

## 📦 儲存庫結構

```
sap-mcp/
├── packages/
│   └── server/                          ✅ Production-Ready MCP Server
│       ├── src/sap_mcp_server/
│       │   ├── core/                    # SAP client & auth (4 files)
│       │   │   ├── __init__.py          # Module initialization
│       │   │   ├── sap_client.py        # OData operations
│       │   │   ├── auth.py              # Credential management
│       │   │   └── exceptions.py        # Custom exceptions
│       │   ├── config/                  # Configuration (4 files)
│       │   │   ├── __init__.py          # Module initialization
│       │   │   ├── settings.py          # Environment config
│       │   │   ├── loader.py            # YAML loader
│       │   │   └── schemas.py           # Pydantic models
│       │   ├── protocol/                # MCP protocol (2 files)
│       │   │   ├── __init__.py          # Module initialization
│       │   │   └── schemas.py           # Request/Response schemas
│       │   ├── tools/                   # 4 modular SAP tools (6 files)
│       │   │   ├── __init__.py          # Tool registry
│       │   │   ├── base.py              # Tool base class
│       │   │   ├── auth_tool.py         # Authentication
│       │   │   ├── query_tool.py        # OData queries
│       │   │   ├── entity_tool.py       # Entity retrieval
│       │   │   └── service_tool.py      # Service discovery
│       │   ├── transports/              # Transport layer (2 files)
│       │   │   ├── __init__.py          # Module initialization
│       │   │   └── stdio.py             # Stdio transport ✅
│       │   ├── utils/                   # Utilities (3 files)
│       │   │   ├── __init__.py          # Module initialization
│       │   │   ├── logger.py            # Structured logging
│       │   │   └── validators.py        # Input validation
│       │   └── __init__.py              # Package initialization
│       ├── config/                      # Server configuration
│       │   ├── services.yaml            # SAP services config
│       │   └── services.yaml.example    # Configuration template
│       ├── tests/                       # Test suite (7 files, 56% coverage)
│       │   ├── __init__.py              # Test package initialization
│       │   ├── conftest.py              # Pytest fixtures
│       │   ├── unit/                    # Unit tests
│       │   │   ├── __init__.py          # Unit test package
│       │   │   ├── test_base.py         # Base tool tests
│       │   │   └── test_validators.py   # Validator tests
│       │   └── integration/             # Integration tests
│       │       ├── __init__.py          # Integration test package
│       │       └── test_tool_integration.py  # Tool integration tests
│       ├── pyproject.toml               # Package configuration
│       └── README.md                    # Server package documentation
│
├── docs/                                # Documentation
│   ├── architecture/                    # Architecture documentation
│   │   └── server.md                    # Server architecture
│   └── guides/                          # User guides
│       ├── configuration.md             # Configuration guide
│       ├── deployment.md                # Deployment guide
│       ├── troubleshooting.md           # Troubleshooting guide
│       ├── odata-service-creation-flight-demo.md  # OData service creation
│       └── sfight-demo-guide.md         # SFLIGHT demo guide
│
├── examples/                            # Example applications
│   ├── basic/                           # Basic examples
│   │   └── stdio_client.py              # Stdio client example
│   ├── chatbot/                         # Chatbot examples
│   │   └── order_inquiry_chatbot.py     # Order inquiry chatbot
│   └── README.md                        # Examples documentation
│
├── scripts/                             # Development scripts
│   ├── create_structure.sh              # Project structure creation
│   ├── migrate_code.sh                  # Code migration script
│   └── update_imports.py                # Import update script
│
├── .claude/                             # Claude Code configuration
│   └── settings.local.json              # Local settings
│
├── .env.server.example                  # Environment template
├── .gitignore                           # Git ignore rules
├── README.md                            # Main documentation (English)
├── README.ja.md                         # Japanese documentation
├── README.ko.md                         # Korean documentation
├── README.th.md                         # Thai documentation
├── README.zh-TW.md                      # Traditional Chinese documentation
└── README.zh-CN.md                      # Simplified Chinese documentation
```

---

## ✨ 功能

### 核心能力

<table>
<tr>
<td width="50%">

#### 🛠️ 工具
- ✅ **sap_authenticate**: 安全的 SAP 驗證
- ✅ **sap_query**: 帶過濾器的 OData 查詢
- ✅ **sap_get_entity**: 單一實體檢索
- ✅ **sap_list_services**: 服務發現

</td>
<td width="50%">

#### 🚀 傳輸
- ✅ **Stdio**: 生產級 stdin/stdout

</td>
</tr>
<tr>
<td>

#### 📊 日誌與監控
- ✅ **結構化日誌**: JSON + Console
- ✅ **效能指標**: 請求時間
- ✅ **錯誤追蹤**: 完整上下文
- ✅ **稽核軌跡**: 安全事件

</td>
<td>

#### 🔒 安全性
- ✅ **輸入驗證**: OData & 安全性
- ✅ **SSL/TLS 支援**: 安全連線
- ✅ **憑證管理**: .env.server
- ✅ **錯誤處理**: 生產級

</td>
</tr>
</table>

### 開發者體驗

- ✅ **模組化架構**: 每個工具一個檔案
- ✅ **型別安全**: 完整的型別提示
- ✅ **文件**: 全面的指南
- ✅ **簡易安裝**: `pip install -e .`
- ✅ **熱重載**: 開發模式
- ✅ **範例應用程式**: 3 個可運行的範例

---

## 🚀 快速開始

### 先決條件

#### 系統需求

- **Python 3.11 或更高版本**
- **pip** (Python 套件安裝程式)
- **Git** (用於複製儲存庫)
- SAP Gateway 存取憑證
- 虛擬環境支援

#### Python 安裝

<details>
<summary><b>🪟 Windows</b></summary>

**選項 1: Microsoft Store (推薦用於 Windows 10/11)**
```powershell
# 在 Microsoft Store 搜尋 "Python 3.11" 或 "Python 3.12"
# 或從 python.org 下載
```

**選項 2: Python.org 安裝程式**
1. 從 [python.org/downloads](https://www.python.org/downloads/) 下載
2. 執行安裝程式
3. ✅ **勾選 "Add Python to PATH"**
4. 點擊 "Install Now"

**驗證安裝:**
```powershell
python --version
# 應顯示: Python 3.11.x or higher

pip --version
# 應顯示: pip 23.x.x or higher
```

**常見問題:**
- 如果找不到 `python` 命令，請嘗試 `python3` 或 `py`
- 如果找不到 `pip`，請安裝: `python -m ensurepip --upgrade`

</details>

<details>
<summary><b>🍎 macOS</b></summary>

**選項 1: Homebrew (推薦)**
```bash
# 如果尚未安裝 Homebrew，請安裝
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Python
brew install python@3.11
# 或
brew install python@3.12
```

**選項 2: Python.org 安裝程式**
1. 從 [python.org/downloads/macos](https://www.python.org/downloads/macos/) 下載
2. 開啟 `.pkg` 檔案
3. 按照安裝精靈操作

**驗證安裝:**
```bash
python3 --version
# 應顯示: Python 3.11.x or higher

pip3 --version
# 應顯示: pip 23.x.x or higher
```

**注意:** macOS 可能預裝了 Python 2.7。請始終使用 `python3` 和 `pip3` 命令。

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Ubuntu/Debian:**
```bash
# 更新套件列表
sudo apt update

# 安裝 Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# 或安裝最新 Python
sudo apt install python3 python3-venv python3-pip
```

**Fedora/RHEL/CentOS:**
```bash
# 安裝 Python 3.11+
sudo dnf install python3.11 python3-pip

# 或
sudo yum install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**驗證安裝:**
```bash
python3 --version
# 應顯示: Python 3.11.x or higher

pip3 --version
# 應顯示: pip 23.x.x or higher
```

</details>

---

### 1. 安裝

#### 逐步安裝

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# 複製儲存庫
git clone <repository-url>
cd sap-mcp

# 建立虛擬環境
python -m venv .venv

# 啟用虛擬環境
.venv\Scripts\activate
# 或在 PowerShell 中:
# .venv\Scripts\Activate.ps1

# 如果在 PowerShell 中遇到執行策略錯誤:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 驗證啟用 (你應該在提示符中看到 (.venv))
# (.venv) PS C:\path\to\sap-mcp>

# 安裝伺服器套件
cd packages\server
pip install -e .

# 安裝開發依賴 (可選)
pip install -e ".[dev]"

# 驗證安裝
sap-mcp-server-stdio --help
```

**Windows 常見問題:**
- **找不到 `python`**: 嘗試 `python3` 或 `py`
- **存取被拒**: 以管理員身分執行 PowerShell
- **執行策略**: 執行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **長路徑支援**: 在 Windows 中啟用長路徑 (Settings > System > About > Advanced system settings)

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# 複製儲存庫
git clone <repository-url>
cd sap-mcp

# 建立虛擬環境
python3 -m venv .venv

# 啟用虛擬環境
source .venv/bin/activate

# 驗證啟用 (你應該在提示符中看到 (.venv))
# (.venv) user@macbook sap-mcp %

# 安裝伺服器套件
cd packages/server
pip install -e .

# 安裝開發依賴 (可選)
pip install -e ".[dev]"

# 驗證安裝
sap-mcp-server-stdio --help

# 檢查安裝路徑 (對 Gemini CLI 設定很有用)
which sap-mcp-server-stdio
# 範例輸出: /Users/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**macOS 常見問題:**
- **找不到 `python`**: 使用 `python3` 代替
- **找不到 `pip`**: 使用 `pip3` 代替
- **存取被拒**: 不要在虛擬環境中使用 `sudo`
- **安裝後找不到命令**: 確保已啟用虛擬環境

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 複製儲存庫
git clone <repository-url>
cd sap-mcp

# 建立虛擬環境
python3 -m venv .venv

# 啟用虛擬環境
source .venv/bin/activate

# 驗證啟用 (你應該在提示符中看到 (.venv))
# (.venv) user@linux:~/sap-mcp$

# 安裝伺服器套件
cd packages/server
pip install -e .

# 安裝開發依賴 (可選)
pip install -e ".[dev]"

# 驗證安裝
sap-mcp-server-stdio --help

# 檢查安裝路徑 (對 Gemini CLI 設定很有用)
which sap-mcp-server-stdio
# 範例輸出: /home/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**Linux 常見問題:**
- **找不到 `python3-venv`**: 使用 `sudo apt install python3-venv` 安裝
- **存取被拒**: 不要在虛擬環境中使用 `sudo`
- **SSL 錯誤**: 安裝證書: `sudo apt install ca-certificates`
- **缺少建置依賴**: 使用 `sudo apt install build-essential python3-dev` 安裝

</details>

---

### 2. 設定

SAP MCP 伺服器需要兩個設定檔：
1. **`.env.server`**: SAP 連線憑證 (單一 SAP 系統)
2. **`services.yaml`**: SAP Gateway 服務和驗證設定

#### 2.1. SAP 連線設定 (`.env.server`)

> **⚠️ 重要**: 自 v0.2.0 起，`.env.server` 已整合至 **專案根目錄**。之前的 `packages/server/.env.server` 位置已不再支援。

**檔案位置**: `.env.server` 必須位於 **專案根目錄**。

```
sap-mcp/
├── .env.server              ← 設定檔 (唯一位置 - 在此建立)
├── .env.server.example      ← 範例模板
├── packages/
│   └── server/
└── README.md
```

**設定步驟**:

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# 前往專案根目錄
cd C:\path\to\sap-mcp

# 複製環境模板
copy .env.server.example .env.server

# 使用 Notepad 編輯設定，填入你的 SAP 憑證
notepad .env.server

# 或使用你喜歡的編輯器:
# code .env.server (VS Code)
# notepad++ .env.server (Notepad++)

# 注意: Windows 中的檔案權限處理方式不同
# 確保檔案不在公共資料夾中
# 右鍵點擊 .env.server > Properties > Security 以限制存取
```

**Windows 特別說明:**
- Windows 路徑使用反斜線 (`\`)
- PowerShell 執行策略可能會阻擋腳本 (見安裝部分)
- 將 `.env.server` 存放在有存取限制的使用者資料夾中
- 如果防毒軟體阻擋檔案，請使用 Windows Defender 排除項目

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# 前往專案根目錄
cd /path/to/your/sap-mcp

# 複製環境模板
cp .env.server.example .env.server

# 編輯設定，填入你的 SAP 憑證
nano .env.server
# 或使用你喜歡的編輯器:
# vim .env.server
# code .env.server (VS Code)
# open -a TextEdit .env.server

# 設定適當的權限 (推薦用於安全性)
chmod 600 .env.server

# 驗證權限
ls -la .env.server
# 應顯示: -rw------- (僅擁有者可讀寫)
```

**macOS 特別說明:**
- 檔案權限為 Unix 風格 (與 Linux 相同)
- `chmod 600` 確保只有你的使用者可以讀寫檔案
- macOS 可能在首次存取時會有額外的安全提示
- 為了最大安全性，請存放在你的家目錄中

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 前往專案根目錄
cd /path/to/your/sap-mcp

# 複製環境模板
cp .env.server.example .env.server

# 編輯設定，填入你的 SAP 憑證
nano .env.server
# 或使用你喜歡的編輯器:
# vim .env.server
# code .env.server (VS Code)
# gedit .env.server (GNOME)

# 設定適當的權限 (安全性必需)
chmod 600 .env.server

# 驗證權限
ls -la .env.server
# 應顯示: -rw------- (僅擁有者可讀寫)

# 可選: 驗證檔案不可被所有人讀取
stat .env.server
```

**Linux 特別說明:**
- `chmod 600` 對於安全性至關重要 (僅擁有者可存取)
- SELinux/AppArmor 可能需要額外設定
- 檔案必須屬於執行伺服器的使用者
- 切勿使用 `sudo` 編輯或執行此檔案

</details>

---

**必要的環境變數**:
```bash
# SAP System Connection (Single SAP System)
SAP_HOST=your-sap-host.com          # SAP Gateway hostname
SAP_PORT=443                         # HTTPS port (usually 443 or 8443)
SAP_USERNAME=your-username           # SAP user ID
SAP_PASSWORD=your-password           # SAP password
SAP_CLIENT=100                       # SAP client number (e.g., 100, 800)

# Security Settings
SAP_VERIFY_SSL=true                  # Enable SSL certificate verification (recommended)
SAP_TIMEOUT=30                       # Request timeout in seconds

# Optional: Connection Pooling
SAP_MAX_CONNECTIONS=10               # Maximum concurrent connections (optional)
SAP_RETRY_ATTEMPTS=3                 # Number of retry attempts on failure (optional)
```

**安全最佳實踐**:
- ✅ 切勿將 `.env.server` 提交到版本控制 (已在 `.gitignore` 中)
- ✅ 使用強且獨特的密碼
- ✅ 在生產環境中啟用 SSL 驗證 (`SAP_VERIFY_SSL=true`)
- ✅ 限制檔案權限: `chmod 600 .env.server`

#### 2.2. SAP Gateway 服務設定 (`services.yaml`)

設定 MCP 伺服器可以存取的 SAP Gateway 服務 (OData 服務)。

**位置**: `packages/server/config/services.yaml`

```bash
# 複製範例設定
cp packages/server/config/services.yaml.example packages/server/config/services.yaml

# 編輯服務設定
vim packages/server/config/services.yaml
```

**基本設定範例**:

```yaml
# Gateway URL configuration
gateway:
  # Base URL pattern for OData services
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"

  # Metadata endpoint suffix
  metadata_suffix: "/$metadata"

  # Service catalog path
  service_catalog_path: "/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection"

  # Authentication endpoint configuration
  auth_endpoint:
    # RECOMMENDED: Use catalog metadata (works without specific service)
    use_catalog_metadata: true

    # Optional: Use specific service for authentication (if catalog unavailable)
    # use_catalog_metadata: false
    # service_id: Z_TRAVEL_RECOMMENDATIONS_SRV
    # entity_name: AirlineSet

# SAP OData Services
services:
  # SFLIGHT Demo Service (Travel Recommendations)
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

    # Optional: Custom headers for this service
    custom_headers: {}
```

#### 2.3. 驗證端點選項

`auth_endpoint` 設定控制 MCP 伺服器如何與 SAP 進行驗證。

**選項 1: Catalog Metadata (推薦)**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: true
```

**優點**:
- ✅ 無需特定的 SAP Gateway 服務即可運作
- ✅ 在不同 SAP 系統間更具彈性和可攜性
- ✅ 獨立於服務的驗證
- ✅ 不依賴自訂服務部署

**驗證流程**:
- CSRF Token: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection`
- Validation: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**選項 2: 特定服務驗證**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: false
    service_id: Z_TRAVEL_RECOMMENDATIONS_SRV    # 必須符合下方的服務 ID
    entity_name: AirlineSet                     # 必須是該服務中的實體
```

**優點**:
- ✅ 明確的基於服務的驗證
- ✅ 當目錄服務不可用時可運作 (罕見)

**缺點**:
- ❌ 需要部署特定服務
- ❌ 如果服務變更則彈性較低
- ❌ 如果服務名稱變更則需要更新設定

**驗證流程**:
- CSRF Token: `/SAP/Z_TRAVEL_RECOMMENDATIONS_SRV/AirlineSet`
- Validation: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**建議**: 除非你有特定理由使用特定服務進行驗證，否則請使用 **選項 1 (Catalog Metadata)**。

### 3. 執行伺服器

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# 啟用虛擬環境
.venv\Scripts\activate
# 或在 PowerShell 中:
# .venv\Scripts\Activate.ps1

# 執行 stdio 伺服器 (推薦)
sap-mcp-server-stdio

# 或直接使用 Python
python -m sap_mcp_server.transports.stdio

# 完成後停用
deactivate
```

**Windows 特別說明:**
- 路徑使用反斜線 (`\`)
- PowerShell 可能需要變更執行策略
- 伺服器在當前終端視窗中執行
- 按 `Ctrl+C` 停止伺服器

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# 啟用虛擬環境
source .venv/bin/activate

# 執行 stdio 伺服器 (推薦)
sap-mcp-server-stdio

# 或直接使用 Python
python3 -m sap_mcp_server.transports.stdio

# 完成後停用
deactivate
```

**macOS 特別說明:**
- 使用 `python3` 代替 `python`
- 伺服器在當前終端工作階段中執行
- 按 `Cmd+C` 或 `Ctrl+C` 停止伺服器
- 伺服器執行時終端機必須保持開啟

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 啟用虛擬環境
source .venv/bin/activate

# 執行 stdio 伺服器 (推薦)
sap-mcp-server-stdio

# 或直接使用 Python
python3 -m sap_mcp_server.transports.stdio

# 完成後停用
deactivate
```

**Linux 特別說明:**
- 使用 `python3` 代替 `python`
- 伺服器在當前終端工作階段中執行
- 按 `Ctrl+C` 停止伺服器
- 可以使用 `nohup` 或 `systemd` 服務在背景執行

</details>

---

## 🤖 與 Gemini CLI 整合

> **📖 官方文件**: 更多關於 Gemini CLI 的資訊，請訪問 <a href="https://geminicli.com/" target="_blank">https://geminicli.com/</a>

### 先決條件

- 已安裝 Node.js 18+ 和 npm
- 已安裝 SAP MCP Server (見上方快速開始)
- 用於存取 Gemini API 的 Google 帳戶

### 1. 安裝 Gemini CLI

```bash
# 全域安裝 Gemini CLI
npm install -g @google/gemini-cli

# 驗證安裝
gemini --version
```

### 2. 驗證 Gemini CLI

**選項 A: 使用 Gemini API Key (推薦用於入門)**

1. 從 [Google AI Studio](https://aistudio.google.com/apikey) 獲取你的 API key
2. 設定環境變數:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**選項 B: 使用 Google Cloud (用於生產)**

```bash
# 首先安裝 Google Cloud CLI
gcloud auth application-default login

# 設定你的專案
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### 3. 註冊 SAP MCP Server

**方法 A: 使用絕對路徑 (推薦用於虛擬環境)**

如果你在虛擬環境中安裝了伺服器，請使用可執行檔的絕對路徑：

1. **尋找絕對路徑**:
```bash
# 前往你的 SAP MCP 目錄
cd /path/to/your/sap-mcp

# 獲取完整路徑
pwd
# 範例輸出: /path/to/your/sap-mcp
```

2. **編輯 `~/.gemini/settings.json`**:
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

**將 `/path/to/your/sap-mcp` 替換為你的實際專案路徑**

> **📝 注意**: `cwd` (當前工作目錄) 參數對於定位 `.env.server` 檔案 **至關重要**。你 **必須** 將其設定為你的專案根目錄 (例如 `/Users/username/projects/sap-mcp`)。如果省略或不正確，伺服器將無法載入你的憑證。

3. **驗證路徑**:
```bash
# 測試命令是否有效
/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio --help

# 檢查註冊
gemini mcp list
# 預期: ✓ sap-server: ... (stdio) - Connected
```

---

**方法 B: 使用 CLI 命令 (如果全域安裝)**

如果 `sap-mcp-server-stdio` 在你的系統 PATH 中：

```bash
# 註冊伺服器
gemini mcp add sap-server sap-mcp-server-stdio

# 檢查註冊
gemini mcp list
```

**注意**: 此方法僅在你將虛擬環境新增到 PATH 或全域安裝套件時有效。

---

**方法 C: 使用 Python 模組路徑**

使用 Python 模組的替代方法：

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

### 4. 開始在 Gemini CLI 使用 SAP MCP

```bash
# 啟動 Gemini CLI
gemini

# 檢查 MCP 伺服器狀態
> /mcp

# 查看可用的 SAP 工具
> /mcp desc

# 範例: 查詢 SAP 航空公司
> 使用 SAP 工具進行驗證並向我顯示所有航空公司

# 範例: 列出可用的 SAP 服務
> 有哪些 SAP 服務可用？

# 範例: 獲取機場詳情
> 獲取法蘭克福機場 (FRA) 的詳情
```

### 進階設定

**啟用受信任伺服器的自動批准**

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

**注意**: 設定 `"trust": true` 以跳過每次工具呼叫的批准提示。僅對受信任的伺服器啟用。

---

**過濾特定工具**

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

**使用案例**:
- `includeTools`: 僅允許特定工具 (白名單)
- `excludeTools`: 封鎖特定工具 (黑名單)
- 不能同時使用兩者

---

**注入環境變數 (可選)**

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

**注意**: `settings.json` 中的環境變數會覆蓋 `.env.server` 中的值。出於安全原因不推薦 - 建議使用 `.env.server` 檔案。

---

**增加慢速網路的超時時間**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "timeout": 60000,  // 60 秒 (預設: 30000)
      "trust": false
    }
  }
}
```

**何時增加**:
- 網路連線緩慢
- 大型資料查詢
- 複雜的 SAP 操作
- 頻繁的超時錯誤

### 故障排除

**問題: 伺服器顯示 "Disconnected"**

```bash
# 檢查 MCP 伺服器狀態
gemini mcp list
# 如果你看到: ✗ sap-server: sap-mcp-server-stdio (stdio) - Disconnected
```

**解決方案 1: 使用絕對路徑 (最常見)**

命令可能位於虛擬環境中。更新 `~/.gemini/settings.json`:

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

**尋找你的絕對路徑**:
```bash
# 前往 SAP MCP 目錄
cd /path/to/your/sap-mcp

# 獲取完整路徑
pwd
# 範例: /path/to/your/sap-mcp

# 檢查命令是否存在
ls -la .venv/bin/sap-mcp-server-stdio
```

---

**問題: PATH 中找不到命令**

```bash
# 直接測試伺服器
sap-mcp-server-stdio
# 錯誤: command not found

# 檢查命令是否存在
which sap-mcp-server-stdio
# 返回: command not found
```

**解決方案 2: 檢查虛擬環境**

```bash
# 檢查虛擬環境是否存在
ls -la .venv/bin/sap-mcp-server-stdio

# 如果存在，在 settings.json 中使用絕對路徑
# 如果不存在，重新安裝:
cd packages/server
pip install -e .
```

---

**問題: 驗證錯誤或找不到 `.env.server`**

```bash
# 檢查 .env.server 是否存在於 PROJECT ROOT (不是在 packages/server/)
cat .env.server

# 必要欄位:
# SAP_HOST=your-host
# SAP_PORT=443
# SAP_USERNAME=your-username
# SAP_PASSWORD=your-password
# SAP_CLIENT=100
```

**解決方案 3: 檢查檔案位置和憑證**

```bash
# 1. 檢查 .env.server 是否在專案根目錄
ls -la .env.server
# 應存在於: /path/to/sap-mcp/.env.server

# 2. 檢查 Gemini CLI settings.json 是否有 "cwd" 參數
cat ~/.gemini/settings.json
# 必須包含: "cwd": "/path/to/sap-mcp"

# 3. 手動測試驗證
source .venv/bin/activate
python -c "from sap_mcp_server.config.settings import get_connection_config; print(get_connection_config())"
```

**常見問題**:

1. **"Field required" 錯誤**: `.env.server` 未載入。檢查:
   - 檔案存在於專案根目錄: `/path/to/your/sap-mcp/.env.server`
   - Gemini CLI `settings.json` 有正確的 `cwd` 參數
   - 檔案有適當的權限: `chmod 600 .env.server`

2. **401 Unauthorized 錯誤**: 在 v0.2.1 (2025-01-22) 已修復
   - **先前問題**: SAP Gateway 拒絕缺少 `sap-client` 參數的請求
   - **當前狀態**: 自動處理 - 所有請求都包含 `sap-client` 參數
   - **驗證**: 確保你已更新到 v0.2.1 或更新版本
   - **手動檢查**: 使用正確的憑證驗證應成功

---

**問題: 需要重新註冊伺服器**

```bash
# 移除現有的伺服器設定
rm ~/.gemini/settings.json

# 或手動編輯以移除 sap-server 項目
```

**解決方案 4: 全新註冊**

```bash
# 方法 1: 直接編輯設定
vim ~/.gemini/settings.json

# 方法 2: 使用絕對路徑 (推薦)
# 按照上方第 3 部分的 "方法 A: 使用絕對路徑" 操作
```

---

**快速診斷步驟**

1. **檢查伺服器可執行檔**:
```bash
/path/to/sap-mcp/.venv/bin/sap-mcp-server-stdio --help
# 應顯示伺服器啟動訊息
```

2. **檢查 Gemini CLI 設定**:
```bash
cat ~/.gemini/settings.json | grep -A 5 "sap-server"
# 驗證 "command" 路徑是否正確
```

3. **測試連線**:
```bash
gemini mcp list
# 應顯示: ✓ sap-server: ... - Connected
```

4. **在 Gemini CLI 中測試**:
```bash
gemini
> /mcp
> /mcp desc
# 應列出 SAP 工具
```

### Gemini CLI 中可用的 SAP 工具

註冊後，你可以透過自然語言使用這些 SAP 工具：

| 工具 | 描述 | 範例提示 |
|------|-------------|----------------|
| **sap_authenticate** | 向 SAP Gateway 驗證 | "向 SAP 驗證" |
| **sap_query** | 使用 OData 過濾器查詢 SAP 實體 | "使用旅遊推薦服務顯示所有航空公司" |
| **sap_get_entity** | 透過鍵值獲取特定實體 | "獲取法蘭克福機場 (FRA) 的詳情" |
| **sap_list_services** | 列出可用的 SAP 服務 | "有哪些 SAP 服務可用？" |

### 範例工作流程

**1. 航班查詢工作流程**

```bash
gemini

> 連線到 SAP 並尋找所有漢莎航空的航班
# Gemini 將會:
# 1. 呼叫 sap_authenticate
# 2. 在 FlightSet 上呼叫 sap_query，過濾器為 "CARRID eq 'LH'"
# 3. 格式化並呈現結果
```

**2. 機場分析**

```bash
> 獲取法蘭克福機場的詳情並顯示可用的連接
# Gemini 將會:
# 1. 驗證
# 2. 為 'FRA' 在 AirportSet 上呼叫 sap_get_entity
# 3. 在 ConnectionSet 上呼叫 sap_query
# 4. 呈現見解
```

**3. 服務發現**

```bash
> 系統中有哪些 SAP 服務和實體集？
# Gemini 將會:
# 1. 呼叫 sap_list_services
# 2. 格式化服務目錄
```

---

## 🔧 可用工具

### 1. SAP Authenticate

使用 `.env.server` 中的憑證向 SAP Gateway 系統進行驗證。

**請求**:
```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

**回應**:
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

### 2. SAP Query

使用 OData 過濾器、選擇、分頁查詢 SAP 實體。

**請求**:
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

**回應**:
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

### 3. SAP Get Entity

透過鍵值檢索單一特定實體。

**請求**:
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

**回應**:
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

### 4. SAP List Services

列出設定中所有可用的 SAP 服務。

**請求**:
```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

**回應**:
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

### 5. 新增工具

1. **建立工具檔案**: `packages/server/src/sap_mcp_server/tools/my_tool.py`

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
        # 實作
        return {"result": "success"}
```

2. **註冊工具**: 更新 `packages/server/src/sap_mcp_server/tools/__init__.py`

```python
from .my_tool import MyNewTool

# 新增到註冊表
tool_registry.register(MyNewTool())
```

3. **新增測試**: `tests/unit/test_my_tool.py`

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

## 📚 使用範例

### 使用工具註冊表

```python
from sap_mcp_server.tools import tool_registry
from sap_mcp_server.protocol.schemas import ToolCallRequest

# 列出可用工具
tools = tool_registry.list_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")

# 呼叫工具
request = ToolCallRequest(
    name="sap_list_services",
    arguments={}
)
result = await tool_registry.call_tool(request)
print(result)
```

### MCP 客戶端範例

```python
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    # 連線到 MCP 伺服器
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化工作階段
            await session.initialize()

            # 驗證
            auth_result = await session.call_tool("sap_authenticate", {})

            # 查詢航空公司
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

### 結構化日誌

```python
from sap_mcp_server.utils.logger import setup_logging, get_logger

# 生產環境 (JSON logs)
setup_logging(level="INFO", json_logs=True)

# 開發環境 (colored console)
setup_logging(level="DEBUG", json_logs=False)

# 使用 logger
logger = get_logger(__name__)
logger.info("Server started", port=8080, transport="stdio")
logger.error("Query failed", error=str(e), query=params)
```

### 輸入驗證

```python
from sap_mcp_server.utils.validators import (
    validate_odata_filter,
    validate_entity_key,
    sanitize_input
)

# 驗證 OData 過濾器
if validate_odata_filter("CARRID eq 'LH'"):
    # 安全執行
    pass

# 清理使用者輸入
safe_input = sanitize_input(user_data, max_length=1000)

# 驗證實體鍵值
if validate_entity_key(key):
    # 獲取實體
    pass
```

---

## 🔒 安全性

### 縱深防禦

| 層級 | 實作 | 狀態 |
|-------|---------------|--------|
| **Input Validation** | OData 語法, SQL injection 防護 | ✅ |
| **Authentication** | 憑證驗證, 工作階段管理 | ✅ |
| **Authorization** | 服務存取控制 | ✅ |
| **Transport Security** | SSL/TLS, 憑證驗證 | ✅ |
| **Audit Logging** | 結構化日誌, 排除敏感資料 | ✅ |

### 最佳實踐

1. **Credentials**: 儲存在 `.env.server`, 切勿提交到 git
2. **SSL/TLS**: 在生產環境中始終啟用 (`SAP_VERIFY_SSL=true`)
3. **Validation**: 在呼叫 SAP 之前驗證所有輸入
4. **Logging**: 敏感資料從日誌中排除
5. **Error Handling**: 為客戶端提供通用錯誤訊息

---

## 🎓 SAP SFLIGHT 演示場景

### 場景概覽

SFLIGHT 資料集是 SAP 提供的標準範例資料庫，包含航班時刻表、航空公司、機場和預訂的資料。這是測試和演示資料建模及服務建立的絕佳資源。

本指南假設你有一個公開此資料集的 OData 服務。目標是將我們的 SAP MCP 伺服器連接到此服務，並使用 AI 代理或其他客戶端與其互動。

**官方 SAP 文件:**
- [SAP Documentation - Flight Model](https://help.sap.com/SAPhelp_nw73/helpdata/en/cf/21f304446011d189700000e8322d00/frameset.htm)
- [SAP Help Portal - Flight Model](https://help.sap.com/docs/SAP_NETWEAVER_702/ff5206fc6c551014a1d28b076487e7df/cf21f304446011d189700000e8322d00.html)

---

### 先決條件

1. **已安裝 SAP MCP Server**: 你需要安裝 SAP MCP 伺服器並擁有可用的 Python 環境。有關完整說明，請參閱 [快速開始部分](#-quick-start)。

2. **SFLIGHT OData Service**: 必須在你的 SAP Gateway 系統上提供公開 SFLIGHT 資料集的活動 OData 服務。
   - 如果你需要建立此服務，可以按照我們的詳細指南操作: [OData Service Creation Guide: FLIGHT Demo Scenario](./docs/guides/odata-service-creation-flight-demo.md)
   - 對於本指南，我們將假設服務名稱為 `Z_TRAVEL_RECOMMENDATIONS_SRV`，如指南中所建立。

---

### OData 服務建立指南

本指南提供在 SAP 系統中使用 SAP Gateway Service Builder (`SEGW`) 建立 OData 服務的逐步說明，以公開 SAP S/4HANA Fully Activated Appliance (FAA) 版本中可用的 Flight 場景資料。

#### 場景概覽

* **目標:** 透過 OData 服務公開航班時刻表、預訂和相關主資料。
* **場景資料需求:** 航班時刻表、日期、時間、機場詳情、航空公司詳情、乘客詳情、價格等。
* **涉及的 SAP 資料表:** `SFLIGHT`, `SPFLI`, `SCARR`, `SAIRPORT`, `SBOOK`, `SCUSTOM`

---

#### 在 SEGW 中建立 OData 服務的步驟

##### 1. 存取 SAP Gateway Service Builder

前往 SAP 交易代碼 `SEGW`。

##### 2. 建立新專案

1. 點擊 "Create Project" 按鈕。
2. **Project Name:** 指定名稱 (例如 `Z_TRAVEL_RECOMMENDATIONS_SRV`)。
3. **Description:** 提供有意義的描述。
4. **Package:** 指派給一個套件 (例如 `$TMP` 用於本地開發或可傳輸的套件)。

##### 3. 從 DDIC 結構匯入資料模型

此步驟根據底層 SAP 資料表定義你的 OData 實體。

1. 右鍵點擊專案中的 "Data Model" 資料夾。
2. 選擇 **"Import" -> "DDIC Structure"**。
3. 為每個所需的資料表重複匯入過程，指定 **Entity Type Name** 並選擇所需欄位。

***必要操作:*** 確保在匯入過程中正確標記鍵值欄位。

| DDIC 結構 | 實體類型名稱 | 建議鍵值欄位 | 相關 Payload 欄位 (範例) |
| :---- | :---- | :---- | :---- |
| `SFLIGHT` | **Flight** | `CARRID`, `CONNID`, `FLDATE` | `PRICE`, `CURRENCY`, `PLANETYPE`, `SEATSMAX`, `SEATSOCC` |
| `SPFLI` | **Connection** | `CARRID`, `CONNID` | `COUNTRYFR`, `CITYFROM`, `AIRPFROM`, `COUNTRYTO`, `CITYTO`, `AIRPTO`, `DEPTIME`, `ARRTIME`, `DISTANCE` |
| `SCARR` | **Airline** | `CARRID` | `CARRNAME`, `CURRCODE`, `URL` |
| `SAIRPORT` | **Airport** | `ID` | `NAME`, `CITY`, `COUNTRY` |
| `SBOOK` | **Booking** | `CARRID`, `CONNID`, `FLDATE`, `BOOKID` | `CUSTOMID`, `CUSTTYPE`, `SMOKER`, `LUGGWEIGHT`, `WUNIT`, `INVOICE`, `CLASS`, `FORCURAM`, `ORDER_DATE` |
| `SCUSTOM` | **Passenger** | `ID` | `NAME`, `FORM`, `STREET`, `POSTCODE`, `CITY`, `COUNTRY`, `PHONE` |

##### 4. 定義 Associations 和 Navigation Properties

Associations 根據鍵值欄位連結實體。Navigation Properties 允許客戶端應用程式輕鬆遍歷這些關係 (例如使用 `$expand`)。

**邏輯關係:**

* **1:N:** Airline <-> Flights, Airline <-> Connections, Connection <-> Flights, Flight <-> Bookings, Passenger <-> Bookings
* **N:1:** Connection <-> Origin Airport, Connection <-> Destination Airport

**建立 Association 的步驟:**

1. 右鍵點擊 "Data Model" -> **"Create" -> "Association"**。
2. 定義 **Association Name**, **Principal Entity** ('一'端), **Dependent Entity** ('多'端), 和 **Cardinality** (例如 1:N)。
3. 在下一個畫面中，**Specify Key Mapping**，將 Principal 和 Dependent 實體之間的鍵值欄位對應起來。

**要建立的特定 Associations:**

| No. | Association 名稱 | Principal:Dependent | Cardinality | Key Mapping |
| :---- | :---- | :---- | :---- | :---- |
| 1 | `Assoc_Airline_Flights` | `Airline` : `Flight` | 1:N | `Airline.CARRID` <-> `Flight.CARRID` |
| 2 | `Assoc_Airline_Connections` | `Airline` : `Connection` | 1:N | `Airline.CARRID` <-> `Connection.CARRID` |
| 3 | `Assoc_Connection_Flights` | `Connection` : `Flight` | 1:N | `CARRID` & `CONNID` (雙向) |
| 4 | `Assoc_Flight_Bookings` | `Flight` : `Booking` | 1:N | `CARRID`, `CONNID`, `FLDATE` (三向) |
| 5 | `Assoc_Passenger_Bookings` | `Passenger` : `Booking` | 1:N | `Passenger.ID` <-> `Booking.CUSTOMID` |
| 6 | `Assoc_Connection_OriginAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPFROM` <-> `Airport.ID` |
| 7 | `Assoc_Connection_DestAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPTO` <-> `Airport.ID` |

**要建立的 Navigation Properties:**

| 實體 | Navigation Property 名稱 | 目標實體 | 使用的 Association |
| :---- | :---- | :---- | :---- |
| **Airline** | `ToFlights`, `ToConnections` | `Flight`, `Connection` | `Assoc_Airline_Flights`, `Assoc_Airline_Connections` |
| **Flight** | `ToAirline`, `ToConnection`, `ToBookings` | `Airline`, `Connection`, `Booking` | `Assoc_Airline_Flights`, `Assoc_Connection_Flights`, `Assoc_Flight_Bookings` |
| **Connection** | `ToAirline`, `ToFlights`, `ToOriginAirport`, `ToDestinationAirport` | `Airline`, `Flight`, `Airport`, `Airport` | `Assoc_Airline_Connections`, `Assoc_Connection_Flights`, `Assoc_Connection_OriginAirport`, `Assoc_Connection_DestAirport` |
| **Booking** | `ToFlight`, `ToPassenger` | `Flight`, `Passenger` | `Assoc_Flight_Bookings`, `Assoc_Passenger_Bookings` |
| **Passenger** | `ToBookings` | `Booking` | `Assoc_Passenger_Bookings` |

##### 5. 產生 Runtime Objects

1. 點擊 **"Generate Runtime Objects"** 按鈕 (魔術棒圖示)。
2. 這將建立 ABAP 類別: Model Provider Class (MPC) 和 Data Provider Class (DPC)。
3. 接受或調整預設類別名稱。

##### 6. 實作 Data Provider Class (DPC) 方法

產生的 DPC 擴充類別 (例如 `ZCL_Z_TRAVEL_RECOM_DPC_EXT`) 用於自訂邏輯。

* 如果直接資料表對應足夠，基本實作可能就足夠了。
* 對於自訂過濾、聯接、計算或複雜的 Read/Create/Update/Delete (CRUD) 操作，你需要在 DPC 擴充類別中重新定義方法，如 `*_GET_ENTITY` (單一記錄) 和 `*_GET_ENTITYSET` (集合)。

這是 AIRLINESET_GET_ENTITYSET 方法的範例：

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

##### 7. 註冊服務

1. 前往交易 `/IWFND/MAINT_SERVICE`。
2. 點擊 **"Add Service"**。
3. 輸入你的後端系統的 **System Alias** (例如 `LOCAL`)。
4. 透過 **Technical Service Name** (例如 `Z_TRAVEL_RECOMMENDATIONS_SRV`) 搜尋你的服務。
5. 選擇服務並點擊 **"Add Selected Services"**。
6. 指派套件並確認。

##### 8. 啟用並測試服務

1. 在 `/IWFND/MAINT_SERVICE` 中，找到你新註冊的服務。
2. 確保 **ICF node is active** (綠燈)。如果沒有，選擇服務，前往 **"ICF Node" -> "Activate"**。
3. 選擇服務並點擊 **"SAP Gateway Client"** 按鈕。
4. **在 Gateway Client 中測試:**
   * 測試實體集合檢索: 點擊 **"EntitySets"**，選擇 EntitySet (例如 `AirlineCollection`) 並點擊 **"Execute"**。
   * 測試 OData 功能: 嘗試查詢選項如 `$filter`，特別是 **`$expand`** 以驗證導航屬性是否正常運作 (例如 `/FlightSet(key)?$expand=ToAirline`)。

##### 9. 記下服務 URL

最終的 OData 服務 URL 顯示在 Gateway Client 中。它通常遵循以下結構：

`/sap/opu/odata/sap/Z_TRAVEL_RECOMMENDATIONS_SRV/.` 此 URL 是客戶端應用程式 (如 Fiori 或自訂行動應用程式) 用來使用 SFLIGHT 資料的網址。

---







---

## 📖 文件

- **[Server Package README](./packages/server/README.md)**: 詳細的伺服器文件
- **[Configuration Guide](./docs/guides/configuration.md)**: YAML 和環境設定
- **[Deployment Guide](./docs/guides/deployment.md)**: 生產部署
- **[Architecture Documentation](./docs/architecture/server.md)**: 系統架構詳情
- **[API Reference](./docs/api/)**: 工具和協議文件

---

## 📝 授權

MIT License - 詳情請見 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- **MCP Protocol**: Anthropic's Model Context Protocol
- **SAP Gateway**: OData v2/v4 整合
- **Community**: 貢獻者和測試者

---

<div align="center">

**Built with ❤️ for SAP integration via Model Context Protocol**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

**Production Ready** | **56% Coverage** | **98% Test Success**

</div>