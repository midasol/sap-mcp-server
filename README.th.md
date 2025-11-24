# SAP MCP - การรวม SAP Gateway ผ่าน Model Context Protocol

เซิร์ฟเวอร์ MCP ที่สมบูรณ์สำหรับการรวม SAP Gateway ให้เครื่องมือแบบแยกส่วนสำหรับการดำเนินการ SAP OData ด้วย AI agents

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

</div>

---

## 🎯 ภาพรวมโครงการ

เซิร์ฟเวอร์ MCP (Model Context Protocol) ที่พร้อมใช้งานจริง ซึ่งช่วยให้ AI agents และแอปพลิเคชันสามารถโต้ตอบกับระบบ SAP Gateway ผ่านสถาปัตยกรรมที่สะอาดและเป็นโมดูล สร้างขึ้นเพื่อความน่าเชื่อถือ ความปลอดภัย และประสบการณ์ของนักพัฒนา

**สถานะปัจจุบัน**: ✅ **พร้อมใช้งานจริง** (เสร็จสิ้นทั้ง 5 เฟส)

### จุดเด่นสำคัญ

- 🔐 **การรวม SAP ที่ปลอดภัย**: การตรวจสอบสิทธิ์ระดับองค์กรและการรองรับ SSL/TLS
- 🛠️ **4 เครื่องมือแบบโมดูล**: การตรวจสอบสิทธิ์, การสืบค้น, การดึงข้อมูลเอนทิตี, การค้นหาบริการ
- 🚀 **Stdio Transport**: เซิร์ฟเวอร์ MCP ที่พร้อมใช้งานจริง
- 📊 **การบันทึกแบบมีโครงสร้าง**: รูปแบบ JSON และคอนโซลพร้อมเมตริกประสิทธิภาพ
- ✅ **การตรวจสอบความถูกต้อง**: การตรวจสอบ OData และความปลอดภัยที่ครอบคลุม
- 🧪 **ทดสอบอย่างดี**: ความครอบคลุม 56%, ผ่านการทดสอบ 44/45 รายการ (อัตราความสำเร็จ 98%)

---

## 📐 สถาปัตยกรรม

### ภาพรวมระบบ

<details>
<summary>📊 คลิกเพื่อดูแผนภาพภาพรวมระบบ</summary>

```mermaid
graph TB
    subgraph clients["🎯 แอปพลิเคชันลูกค้า"]
        direction TB
        A1["AI Agent<br/><small>LLM/GenAI Integration</small>"]
        A2["Python Client<br/><small>SDK & Libraries</small>"]
        A3["Order Chatbot<br/><small>ตัวอย่างแอปพลิเคชัน</small>"]
    end

    subgraph transport["🚀 เลเยอร์เซิร์ฟเวอร์ MCP"]
        direction TB
        B1["Stdio Transport<br/><small>stdin/stdout Stream</small>"]
    end

    subgraph registry["🛠️ ทะเบียนเครื่องมือ"]
        direction LR
        C1["sap_authenticate<br/><small>การตรวจสอบสิทธิ์</small>"]
        C2["sap_query<br/><small>OData Queries</small>"]
        C3["sap_get_entity<br/><small>การดึงข้อมูลเอนทิตี</small>"]
        C4["sap_list_services<br/><small>การค้นหาบริการ</small>"]
    end

    subgraph core["⚡ เลเยอร์หลัก"]
        direction LR
        D1["SAP Client<br/><small>OData Handler</small>"]
        D2["Auth Manager<br/><small>Credentials</small>"]
        D3["Config Loader<br/><small>YAML/ENV</small>"]
    end

    subgraph utils["🔧 ยูทิลิตี้"]
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

### รายละเอียดส่วนประกอบ

<details>
<summary>🔧 คลิกเพื่อดูแผนภาพรายละเอียดส่วนประกอบ</summary>

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

### การไหลของข้อมูล: ตัวอย่างการสอบถามคำสั่งซื้อ

<details>
<summary>🔄 คลิกเพื่อดูแผนภาพการไหลของข้อมูล</summary>

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

### การไหลของการดำเนินการเครื่องมือ

<details>
<summary>⚡ คลิกเพื่อดูแผนภาพการไหลของการดำเนินการเครื่องมือ</summary>

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

### สถาปัตยกรรมความปลอดภัย

<details>
<summary>🔒 คลิกเพื่อดูแผนภาพสถาปัตยกรรมความปลอดภัย</summary>

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

## 📦 โครงสร้างที่เก็บข้อมูล

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
├── README.old.md                        # Previous README version
└── REFACTORING_SUMMARY.md               # Refactoring history
```

---

## ✨ คุณสมบัติ

### ความสามารถหลัก

<table>
<tr>
<td width="50%">

#### 🛠️ เครื่องมือ
- ✅ **sap_authenticate**: การตรวจสอบสิทธิ์ SAP ที่ปลอดภัย
- ✅ **sap_query**: การสืบค้น OData พร้อมตัวกรอง
- ✅ **sap_get_entity**: การดึงข้อมูลเอนทิตีเดียว
- ✅ **sap_list_services**: การค้นหาบริการ

</td>
<td width="50%">

#### 🚀 การขนส่ง
- ✅ **Stdio**: stdin/stdout ที่พร้อมใช้งานจริง

</td>
</tr>
<tr>
<td>

#### 📊 การบันทึกและการตรวจสอบ
- ✅ **การบันทึกแบบมีโครงสร้าง**: JSON + คอนโซล
- ✅ **เมตริกประสิทธิภาพ**: เวลาในการร้องขอ
- ✅ **การติดตามข้อผิดพลาด**: บริบทเต็มรูปแบบ
- ✅ **เส้นทางการตรวจสอบ**: เหตุการณ์ความปลอดภัย

</td>
<td>

#### 🔒 ความปลอดภัย
- ✅ **การตรวจสอบข้อมูลเข้า**: OData & ความปลอดภัย
- ✅ **การรองรับ SSL/TLS**: การเชื่อมต่อที่ปลอดภัย
- ✅ **การจัดการข้อมูลประจำตัว**: .env.server
- ✅ **การจัดการข้อผิดพลาด**: ระดับการผลิต

</td>
</tr>
</table>

### ประสบการณ์ของนักพัฒนา

- ✅ **สถาปัตยกรรมแบบโมดูล**: หนึ่งเครื่องมือต่อไฟล์
- ✅ **ความปลอดภัยของประเภท**: คำแนะนำประเภทเต็มรูปแบบ
- ✅ **เอกสารประกอบ**: คู่มือที่ครอบคลุม
- ✅ **ติดตั้งง่าย**: `pip install -e .`
- ✅ **Hot Reload**: โหมดการพัฒนา
- ✅ **แอปตัวอย่าง**: 3 ตัวอย่างที่ใช้งานได้

---

## 🚀 เริ่มต้นอย่างรวดเร็ว

### ข้อกำหนดเบื้องต้น

#### ความต้องการของระบบ

- **Python 3.11 หรือสูงกว่า**
- **pip** (ตัวติดตั้งแพ็คเกจ Python)
- **Git** (สำหรับการโคลนที่เก็บข้อมูล)
- ข้อมูลประจำตัวการเข้าถึง SAP Gateway
- การรองรับสภาพแวดล้อมเสมือน

#### การติดตั้ง Python

<details>
<summary><b>🪟 Windows</b></summary>

**ตัวเลือกที่ 1: Microsoft Store (แนะนำสำหรับ Windows 10/11)**
```powershell
# ค้นหา "Python 3.11" หรือ "Python 3.12" ใน Microsoft Store
# หรือดาวน์โหลดจาก python.org
```

**ตัวเลือกที่ 2: ตัวติดตั้ง Python.org**
1. ดาวน์โหลดจาก [python.org/downloads](https://www.python.org/downloads/)
2. รันตัวติดตั้ง
3. ✅ **ตรวจสอบ "Add Python to PATH"**
4. คลิก "Install Now"

**ตรวจสอบการติดตั้ง:**
```powershell
python --version
# ควรแสดง: Python 3.11.x or higher

pip --version
# ควรแสดง: pip 23.x.x or higher
```

**ปัญหาทั่วไป:**
- หากไม่พบคำสั่ง `python` ให้ใช้ `python3` หรือ `py`
- หากไม่พบ `pip` ให้ติดตั้งด้วย: `python -m ensurepip --upgrade`

</details>

<details>
<summary><b>🍎 macOS</b></summary>

**ตัวเลือกที่ 1: Homebrew (แนะนำ)**
```bash
# ติดตั้ง Homebrew หากยังไม่ได้ติดตั้ง
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# ติดตั้ง Python
brew install python@3.11
# หรือ
brew install python@3.12
```

**ตัวเลือกที่ 2: ตัวติดตั้ง Python.org**
1. ดาวน์โหลดจาก [python.org/downloads/macos](https://www.python.org/downloads/macos/)
2. เปิดไฟล์ `.pkg`
3. ทำตามตัวช่วยสร้างการติดตั้ง

**ตรวจสอบการติดตั้ง:**
```bash
python3 --version
# ควรแสดง: Python 3.11.x or higher

pip3 --version
# ควรแสดง: pip 23.x.x or higher
```

**หมายเหตุ:** macOS อาจมี Python 2.7 ติดตั้งไว้ล่วงหน้า ใช้คำสั่ง `python3` และ `pip3` เสมอ

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Ubuntu/Debian:**
```bash
# อัปเดตรายการแพ็คเกจ
sudo apt update

# ติดตั้ง Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# หรือสำหรับ Python ล่าสุด
sudo apt install python3 python3-venv python3-pip
```

**Fedora/RHEL/CentOS:**
```bash
# ติดตั้ง Python 3.11+
sudo dnf install python3.11 python3-pip

# หรือ
sudo yum install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**ตรวจสอบการติดตั้ง:**
```bash
python3 --version
# ควรแสดง: Python 3.11.x or higher

pip3 --version
# ควรแสดง: pip 23.x.x or higher
```

</details>

---

### 1. การติดตั้ง

#### การติดตั้งทีละขั้นตอน

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# โคลนที่เก็บข้อมูล
git clone <repository-url>
cd sap-mcp

# สร้างสภาพแวดล้อมเสมือน
python -m venv .venv

# เปิดใช้งานสภาพแวดล้อมเสมือน
.venv\Scripts\activate
# หรือใน PowerShell:
# .venv\Scripts\Activate.ps1

# หากคุณได้รับข้อผิดพลาดนโยบายการดำเนินการใน PowerShell:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# ตรวจสอบการเปิดใช้งาน (คุณควรเห็น (.venv) ในพรอมต์)
# (.venv) PS C:\path\to\sap-mcp>

# ติดตั้งแพ็คเกจเซิร์ฟเวอร์
cd packages\server
pip install -e .

# ติดตั้งการพึ่งพาการพัฒนา (ทางเลือก)
pip install -e ".[dev]"

# ตรวจสอบการติดตั้ง
sap-mcp-server-stdio --help
```

**ปัญหาทั่วไปของ Windows:**
- **ไม่พบ `python`**: ลอง `python3` หรือ `py`
- **ถูกปฏิเสธการเข้าถึง**: รัน PowerShell ในฐานะผู้ดูแลระบบ
- **นโยบายการดำเนินการ**: รัน `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **การรองรับเส้นทางยาว**: เปิดใช้งานเส้นทางยาวใน Windows (Settings > System > About > Advanced system settings)

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# โคลนที่เก็บข้อมูล
git clone <repository-url>
cd sap-mcp

# สร้างสภาพแวดล้อมเสมือน
python3 -m venv .venv

# เปิดใช้งานสภาพแวดล้อมเสมือน
source .venv/bin/activate

# ตรวจสอบการเปิดใช้งาน (คุณควรเห็น (.venv) ในพรอมต์)
# (.venv) user@macbook sap-mcp %

# ติดตั้งแพ็คเกจเซิร์ฟเวอร์
cd packages/server
pip install -e .

# ติดตั้งการพึ่งพาการพัฒนา (ทางเลือก)
pip install -e ".[dev]"

# ตรวจสอบการติดตั้ง
sap-mcp-server-stdio --help

# ตรวจสอบเส้นทางการติดตั้ง (มีประโยชน์สำหรับการตั้งค่า Gemini CLI)
which sap-mcp-server-stdio
# ตัวอย่างผลลัพธ์: /Users/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**ปัญหาทั่วไปของ macOS:**
- **ไม่พบ `python`**: ใช้ `python3` แทน
- **ไม่พบ `pip`**: ใช้ `pip3` แทน
- **ถูกปฏิเสธการเข้าถึง**: อย่าใช้ `sudo` กับสภาพแวดล้อมเสมือน
- **ไม่พบคำสั่งหลังการติดตั้ง**: ตรวจสอบให้แน่ใจว่าเปิดใช้งานสภาพแวดล้อมเสมือนแล้ว

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# โคลนที่เก็บข้อมูล
git clone <repository-url>
cd sap-mcp

# สร้างสภาพแวดล้อมเสมือน
python3 -m venv .venv

# เปิดใช้งานสภาพแวดล้อมเสมือน
source .venv/bin/activate

# ตรวจสอบการเปิดใช้งาน (คุณควรเห็น (.venv) ในพรอมต์)
# (.venv) user@linux:~/sap-mcp$

# ติดตั้งแพ็คเกจเซิร์ฟเวอร์
cd packages/server
pip install -e .

# ติดตั้งการพึ่งพาการพัฒนา (ทางเลือก)
pip install -e ".[dev]"

# ตรวจสอบการติดตั้ง
sap-mcp-server-stdio --help

# ตรวจสอบเส้นทางการติดตั้ง (มีประโยชน์สำหรับการตั้งค่า Gemini CLI)
which sap-mcp-server-stdio
# ตัวอย่างผลลัพธ์: /home/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**ปัญหาทั่วไปของ Linux:**
- **ไม่พบ `python3-venv`**: ติดตั้งด้วย `sudo apt install python3-venv`
- **ถูกปฏิเสธการเข้าถึง**: อย่าใช้ `sudo` กับสภาพแวดล้อมเสมือน
- **ข้อผิดพลาด SSL**: ติดตั้งใบรับรอง: `sudo apt install ca-certificates`
- **ขาดการพึ่งพาการสร้าง**: ติดตั้งด้วย `sudo apt install build-essential python3-dev`

</details>

---

### 2. การกำหนดค่า

เซิร์ฟเวอร์ SAP MCP ต้องการไฟล์การกำหนดค่าสองไฟล์:
1. **`.env.server`**: ข้อมูลประจำตัวการเชื่อมต่อ SAP (ระบบ SAP เดียว)
2. **`services.yaml`**: การตั้งค่า SAP Gateway Services และการตรวจสอบสิทธิ์

#### 2.1. การกำหนดค่าการเชื่อมต่อ SAP (`.env.server`)

> **⚠️ สำคัญ**: ณ v0.2.0, `.env.server` ได้ถูกรวมไว้ที่ **ไดเรกทอรีรากของโครงการเท่านั้น** ตำแหน่ง `packages/server/.env.server` ก่อนหน้านี้ไม่ได้รับการสนับสนุนอีกต่อไป

**ตำแหน่งไฟล์**: `.env.server` ต้องอยู่ใน **ไดเรกทอรีรากของโครงการ**

```
sap-mcp/
├── .env.server              ← ไฟล์การกำหนดค่า (ตำแหน่งเดียวเท่านั้น - สร้างที่นี่)
├── .env.server.example      ← เทมเพลตตัวอย่าง
├── packages/
│   └── server/
└── README.md
```

**ขั้นตอนการตั้งค่า**:

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# ไปที่รากของโครงการ
cd C:\path\to\sap-mcp

# คัดลอกเทมเพลตสภาพแวดล้อม
copy .env.server.example .env.server

# แก้ไขการกำหนดค่าด้วยข้อมูลประจำตัว SAP ของคุณโดยใช้ Notepad
notepad .env.server

# หรือใช้โปรแกรมแก้ไขที่คุณต้องการ:
# code .env.server (VS Code)
# notepad++ .env.server (Notepad++)

# หมายเหตุ: สิทธิ์ของไฟล์ได้รับการจัดการแตกต่างกันใน Windows
# ตรวจสอบให้แน่ใจว่าไฟล์ไม่ได้อยู่ในโฟลเดอร์สาธารณะ
# คลิกขวา .env.server > Properties > Security เพื่อจำกัดการเข้าถึง
```

**หมายเหตุเฉพาะของ Windows:**
- ใช้ backslashes (`\`) สำหรับเส้นทางใน Windows
- นโยบายการดำเนินการของ PowerShell อาจบล็อกสคริปต์ (ดูส่วนการติดตั้ง)
- เก็บ `.env.server` ในโฟลเดอร์ผู้ใช้ที่มีการจำกัดการเข้าถึง
- ใช้ข้อยกเว้น Windows Defender หากโปรแกรมป้องกันไวรัสบล็อกไฟล์

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# ไปที่รากของโครงการ
cd /path/to/your/sap-mcp

# คัดลอกเทมเพลตสภาพแวดล้อม
cp .env.server.example .env.server

# แก้ไขการกำหนดค่าด้วยข้อมูลประจำตัว SAP ของคุณ
nano .env.server
# หรือใช้โปรแกรมแก้ไขที่คุณต้องการ:
# vim .env.server
# code .env.server (VS Code)
# open -a TextEdit .env.server

# ตั้งค่าสิทธิ์ที่เหมาะสม (แนะนำเพื่อความปลอดภัย)
chmod 600 .env.server

# ตรวจสอบสิทธิ์
ls -la .env.server
# ควรแสดง: -rw------- (เจ้าของเท่านั้นที่สามารถอ่าน/เขียนได้)
```

**หมายเหตุเฉพาะของ macOS:**
- สิทธิ์ของไฟล์เป็นแบบ Unix (เหมือนกับ Linux)
- `chmod 600` ช่วยให้มั่นใจว่ามีเพียงผู้ใช้ของคุณเท่านั้นที่สามารถอ่าน/เขียนไฟล์ได้
- macOS อาจมีพรอมต์ความปลอดภัยเพิ่มเติมสำหรับการเข้าถึงครั้งแรก
- เก็บไว้ในโฮมไดเรกทอรีของคุณเพื่อความปลอดภัยสูงสุด

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# ไปที่รากของโครงการ
cd /path/to/your/sap-mcp

# คัดลอกเทมเพลตสภาพแวดล้อม
cp .env.server.example .env.server

# แก้ไขการกำหนดค่าด้วยข้อมูลประจำตัว SAP ของคุณ
nano .env.server
# หรือใช้โปรแกรมแก้ไขที่คุณต้องการ:
# vim .env.server
# code .env.server (VS Code)
# gedit .env.server (GNOME)

# ตั้งค่าสิทธิ์ที่เหมาะสม (จำเป็นเพื่อความปลอดภัย)
chmod 600 .env.server

# ตรวจสอบสิทธิ์
ls -la .env.server
# ควรแสดง: -rw------- (เจ้าของเท่านั้นที่สามารถอ่าน/เขียนได้)

# ทางเลือก: ตรวจสอบว่าไฟล์ไม่สามารถอ่านได้โดยทุกคน
stat .env.server
```

**หมายเหตุเฉพาะของ Linux:**
- `chmod 600` มีความสำคัญต่อความปลอดภัย (เจ้าของเท่านั้นที่เข้าถึงได้)
- SELinux/AppArmor อาจต้องการการกำหนดค่าเพิ่มเติม
- ไฟล์ต้องเป็นของผู้ใช้ที่รันเซิร์ฟเวอร์
- ห้ามใช้ `sudo` เพื่อแก้ไขหรือรันด้วยไฟล์นี้

</details>

---

**ตัวแปรสภาพแวดล้อมที่จำเป็น**:
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

**แนวทางปฏิบัติที่ดีที่สุดด้านความปลอดภัย**:
- ✅ ห้าม commit `.env.server` ลงใน version control (มีอยู่ใน `.gitignore` แล้ว)
- ✅ ใช้รหัสผ่านที่รัดกุมและไม่ซ้ำกัน
- ✅ เปิดใช้งานการตรวจสอบ SSL ในการผลิต (`SAP_VERIFY_SSL=true`)
- ✅ จำกัดสิทธิ์ของไฟล์: `chmod 600 .env.server`

#### 2.2. การกำหนดค่า SAP Gateway Services (`services.yaml`)

กำหนดค่า SAP Gateway Services (OData services) ที่เซิร์ฟเวอร์ MCP สามารถเข้าถึงได้

**ตำแหน่ง**: `packages/server/config/services.yaml`

```bash
# คัดลอกการกำหนดค่าตัวอย่าง
cp packages/server/config/services.yaml.example packages/server/config/services.yaml

# แก้ไขการกำหนดค่าบริการ
vim packages/server/config/services.yaml
```

**ตัวอย่างการกำหนดค่าพื้นฐาน**:

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

#### 2.3. ตัวเลือกจุดสิ้นสุดการตรวจสอบสิทธิ์

การกำหนดค่า `auth_endpoint` ควบคุมวิธีที่เซิร์ฟเวอร์ MCP ตรวจสอบสิทธิ์กับ SAP

**ตัวเลือกที่ 1: Catalog Metadata (แนะนำ)**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: true
```

**ข้อดี**:
- ✅ ทำงานโดยไม่ต้องใช้ SAP Gateway Services เฉพาะ
- ✅ ยืดหยุ่นและพกพาได้มากขึ้นในระบบ SAP ต่างๆ
- ✅ การตรวจสอบสิทธิ์ที่ไม่ขึ้นกับบริการ
- ✅ ไม่ต้องพึ่งพาการปรับใช้บริการที่กำหนดเอง

**ขั้นตอนการตรวจสอบสิทธิ์**:
- CSRF Token: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection`
- Validation: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**ตัวเลือกที่ 2: การตรวจสอบสิทธิ์เฉพาะบริการ**

```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: false
    service_id: Z_TRAVEL_RECOMMENDATIONS_SRV    # ต้องตรงกับ ID บริการด้านล่าง
    entity_name: AirlineSet                     # ต้องเป็นเอนทิตีในบริการนั้น
```

**ข้อดี**:
- ✅ การตรวจสอบสิทธิ์ตามบริการที่ชัดเจน
- ✅ ทำงานเมื่อบริการแคตตาล็อกไม่พร้อมใช้งาน (หายาก)

**ข้อเสีย**:
- ❌ ต้องการให้บริการที่ระบุถูกปรับใช้
- ❌ ยืดหยุ่นน้อยลงหากบริการเปลี่ยนแปลง
- ❌ ต้องอัปเดตการกำหนดค่าหากชื่อบริการเปลี่ยนแปลง

**ขั้นตอนการตรวจสอบสิทธิ์**:
- CSRF Token: `/SAP/Z_TRAVEL_RECOMMENDATIONS_SRV/AirlineSet`
- Validation: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

**คำแนะนำ**: ใช้ **ตัวเลือกที่ 1 (Catalog Metadata)** เว้นแต่คุณจะมีเหตุผลเฉพาะในการใช้บริการใดบริการหนึ่งสำหรับการตรวจสอบสิทธิ์

### 3. รันเซิร์ฟเวอร์

<details open>
<summary><b>🪟 Windows (PowerShell/Command Prompt)</b></summary>

```powershell
# เปิดใช้งานสภาพแวดล้อมเสมือน
.venv\Scripts\activate
# หรือใน PowerShell:
# .venv\Scripts\Activate.ps1

# รันเซิร์ฟเวอร์ stdio (แนะนำ)
sap-mcp-server-stdio

# หรือโดยตรงด้วย Python
python -m sap_mcp_server.transports.stdio

# หากต้องการปิดใช้งานเมื่อเสร็จสิ้น
deactivate
```

**หมายเหตุเฉพาะของ Windows:**
- ใช้ backslash (`\`) สำหรับเส้นทาง
- PowerShell อาจต้องมีการเปลี่ยนแปลงนโยบายการดำเนินการ
- เซิร์ฟเวอร์ทำงานในหน้าต่างเทอร์มินัลปัจจุบัน
- กด `Ctrl+C` เพื่อหยุดเซิร์ฟเวอร์

</details>

<details>
<summary><b>🍎 macOS (Terminal)</b></summary>

```bash
# เปิดใช้งานสภาพแวดล้อมเสมือน
source .venv/bin/activate

# รันเซิร์ฟเวอร์ stdio (แนะนำ)
sap-mcp-server-stdio

# หรือโดยตรงด้วย Python
python3 -m sap_mcp_server.transports.stdio

# หากต้องการปิดใช้งานเมื่อเสร็จสิ้น
deactivate
```

**หมายเหตุเฉพาะของ macOS:**
- ใช้ `python3` แทน `python`
- เซิร์ฟเวอร์ทำงานในเซสชันเทอร์มินัลปัจจุบัน
- กด `Cmd+C` หรือ `Ctrl+C` เพื่อหยุดเซิร์ฟเวอร์
- เทอร์มินัลต้องเปิดอยู่ขณะที่เซิร์ฟเวอร์ทำงาน

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# เปิดใช้งานสภาพแวดล้อมเสมือน
source .venv/bin/activate

# รันเซิร์ฟเวอร์ stdio (แนะนำ)
sap-mcp-server-stdio

# หรือโดยตรงด้วย Python
python3 -m sap_mcp_server.transports.stdio

# หากต้องการปิดใช้งานเมื่อเสร็จสิ้น
deactivate
```

**หมายเหตุเฉพาะของ Linux:**
- ใช้ `python3` แทน `python`
- เซิร์ฟเวอร์ทำงานในเซสชันเทอร์มินัลปัจจุบัน
- กด `Ctrl+C` เพื่อหยุดเซิร์ฟเวอร์
- สามารถรันในพื้นหลังด้วย `nohup` หรือบริการ `systemd`

</details>

---

## 🤖 การรวมกับ Gemini CLI

> **📖 เอกสารอย่างเป็นทางการ**: สำหรับข้อมูลเพิ่มเติมเกี่ยวกับ Gemini CLI โปรดไปที่ <a href="https://geminicli.com/" target="_blank">https://geminicli.com/</a>

### ข้อกำหนดเบื้องต้น

- ติดตั้ง Node.js 18+ และ npm แล้ว
- ติดตั้ง SAP MCP Server แล้ว (ดู Quick Start ด้านบน)
- บัญชี Google สำหรับการเข้าถึง Gemini API

### 1. ติดตั้ง Gemini CLI

```bash
# ติดตั้ง Gemini CLI ทั่วโลก
npm install -g @google/gemini-cli

# ตรวจสอบการติดตั้ง
gemini --version
```

### 2. ตรวจสอบสิทธิ์ Gemini CLI

**ตัวเลือก A: การใช้ Gemini API Key (แนะนำสำหรับการเริ่มต้น)**

1. รับ API key ของคุณจาก [Google AI Studio](https://aistudio.google.com/apikey)
2. ตั้งค่าตัวแปรสภาพแวดล้อม:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**ตัวเลือก B: การใช้ Google Cloud (สำหรับการผลิต)**

```bash
# ติดตั้ง Google Cloud CLI ก่อน
gcloud auth application-default login

# ตั้งค่าโครงการของคุณ
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### 3. ลงทะเบียน SAP MCP Server

**วิธี A: การใช้เส้นทางสัมบูรณ์ (แนะนำสำหรับสภาพแวดล้อมเสมือน)**

หากคุณติดตั้งเซิร์ฟเวอร์ในสภาพแวดล้อมเสมือน ให้ใช้เส้นทางสัมบูรณ์ไปยังไฟล์เรียกทำงาน:

1. **ค้นหาเส้นทางสัมบูรณ์**:
```bash
# ไปที่ไดเรกทอรี SAP MCP ของคุณ
cd /path/to/your/sap-mcp

# รับเส้นทางเต็ม
pwd
# ตัวอย่างผลลัพธ์: /path/to/your/sap-mcp
```

2. **แก้ไข `~/.gemini/settings.json`**:
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

**แทนที่ `/path/to/your/sap-mcp` ด้วยเส้นทางโครงการจริงของคุณ**

> **📝 หมายเหตุ**: พารามิเตอร์ `cwd` (ไดเรกทอรีการทำงานปัจจุบัน) มีความสำคัญ **อย่างยิ่ง** สำหรับการค้นหาไฟล์ `.env.server` คุณ **ต้อง** ตั้งค่านี้เป็นไดเรกทอรีรากของโครงการของคุณ (เช่น `/Users/username/projects/sap-mcp`) หากละเว้นหรือไม่ถูกต้อง เซิร์ฟเวอร์จะไม่สามารถโหลดข้อมูลประจำตัวของคุณได้

3. **ตรวจสอบเส้นทาง**:
```bash
# ทดสอบว่าคำสั่งทำงานได้
/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio --help

# ตรวจสอบการลงทะเบียน
gemini mcp list
# คาดหวัง: ✓ sap-server: ... (stdio) - Connected
```

---

**วิธี B: การใช้คำสั่ง CLI (หากติดตั้งทั่วโลก)**

หาก `sap-mcp-server-stdio` อยู่ใน PATH ของระบบของคุณ:

```bash
# ลงทะเบียนเซิร์ฟเวอร์
gemini mcp add sap-server sap-mcp-server-stdio

# ตรวจสอบการลงทะเบียน
gemini mcp list
```

**หมายเหตุ**: วิธีนี้ใช้ได้เฉพาะเมื่อคุณเพิ่มสภาพแวดล้อมเสมือนลงใน PATH หรือติดตั้งแพ็คเกจทั่วโลก

---

**วิธี C: การใช้เส้นทางโมดูล Python**

แนวทางทางเลือกโดยใช้โมดูล Python:

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

### 4. เริ่มใช้ SAP MCP กับ Gemini CLI

```bash
# เริ่ม Gemini CLI
gemini

# ตรวจสอบสถานะเซิร์ฟเวอร์ MCP
> /mcp

# ดูเครื่องมือ SAP ที่มีอยู่
> /mcp desc

# ตัวอย่าง: สืบค้นสายการบิน SAP
> ใช้เครื่องมือ SAP เพื่อตรวจสอบสิทธิ์และแสดงสายการบินทั้งหมดให้ฉันดู

# ตัวอย่าง: รายการบริการ SAP ที่มีอยู่
> มีบริการ SAP อะไรบ้าง?

# ตัวอย่าง: รับรายละเอียดสนามบิน
> ดึงรายละเอียดสำหรับสนามบินแฟรงค์เฟิร์ต (FRA)
```

### การกำหนดค่าขั้นสูง

**เปิดใช้งานการอนุมัติอัตโนมัติสำหรับเซิร์ฟเวอร์ที่เชื่อถือได้**

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

**หมายเหตุ**: ตั้งค่า `"trust": true` เพื่อข้ามพรอมต์การอนุมัติสำหรับการเรียกใช้เครื่องมือแต่ละครั้ง เปิดใช้งานสำหรับเซิร์ฟเวอร์ที่เชื่อถือได้เท่านั้น

---

**กรองเครื่องมือเฉพาะ**

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

**กรณีการใช้งาน**:
- `includeTools`: อนุญาตเฉพาะเครื่องมือที่ระบุ (whitelist)
- `excludeTools`: บล็อกเครื่องมือที่ระบุ (blacklist)
- ไม่สามารถใช้ทั้งสองอย่างพร้อมกันได้

---

**เพิ่มตัวแปรสภาพแวดล้อม (ทางเลือก)**

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

**หมายเหตุ**: ตัวแปรสภาพแวดล้อมใน `settings.json` จะแทนที่ค่าจาก `.env.server` ไม่แนะนำด้วยเหตุผลด้านความปลอดภัย - แนะนำให้ใช้ไฟล์ `.env.server` แทน

---

**เพิ่ม Timeout สำหรับเครือข่ายช้า**

```json
{
  "mcpServers": {
    "sap-server": {
      "command": "/path/to/your/sap-mcp/.venv/bin/sap-mcp-server-stdio",
      "timeout": 60000,  // 60 วินาที (ค่าเริ่มต้น: 30000)
      "trust": false
    }
  }
}
```

**เมื่อใดควรเพิ่ม**:
- การเชื่อมต่อเครือข่ายช้า
- การสืบค้นข้อมูลขนาดใหญ่
- การดำเนินการ SAP ที่ซับซ้อน
- ข้อผิดพลาด timeout บ่อยครั้ง

### การแก้ไขปัญหา

**ปัญหา: เซิร์ฟเวอร์แสดงสถานะ "Disconnected"**

```bash
# ตรวจสอบสถานะเซิร์ฟเวอร์ MCP
gemini mcp list
# หากคุณเห็น: ✗ sap-server: sap-mcp-server-stdio (stdio) - Disconnected
```

**วิธีแก้ปัญหา 1: ใช้เส้นทางสัมบูรณ์ (พบบ่อยที่สุด)**

คำสั่งอาจอยู่ในสภาพแวดล้อมเสมือน อัปเดต `~/.gemini/settings.json`:

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

**ค้นหาเส้นทางสัมบูรณ์ของคุณ**:
```bash
# ไปที่ไดเรกทอรี SAP MCP
cd /path/to/your/sap-mcp

# รับเส้นทางเต็ม
pwd
# ตัวอย่าง: /path/to/your/sap-mcp

# ตรวจสอบว่าคำสั่งมีอยู่
ls -la .venv/bin/sap-mcp-server-stdio
```

---

**ปัญหา: ไม่พบคำสั่งใน PATH**

```bash
# ทดสอบเซิร์ฟเวอร์โดยตรง
sap-mcp-server-stdio
# ข้อผิดพลาด: command not found

# ตรวจสอบว่าคำสั่งมีอยู่หรือไม่
which sap-mcp-server-stdio
# ส่งคืน: command not found
```

**วิธีแก้ปัญหา 2: ตรวจสอบสภาพแวดล้อมเสมือน**

```bash
# ตรวจสอบว่าสภาพแวดล้อมเสมือนมีอยู่หรือไม่
ls -la .venv/bin/sap-mcp-server-stdio

# หากมี ให้ใช้เส้นทางสัมบูรณ์ใน settings.json
# หากไม่มี ให้ติดตั้งใหม่:
cd packages/server
pip install -e .
```

---

**ปัญหา: ข้อผิดพลาดการตรวจสอบสิทธิ์หรือหา `.env.server` ไม่พบ**

```bash
# ตรวจสอบว่า .env.server มีอยู่ใน PROJECT ROOT (ไม่ใช่ใน packages/server/)
cat .env.server

# ฟิลด์ที่จำเป็น:
# SAP_HOST=your-host
# SAP_PORT=443
# SAP_USERNAME=your-username
# SAP_PASSWORD=your-password
# SAP_CLIENT=100
```

**วิธีแก้ปัญหา 3: ตรวจสอบตำแหน่งไฟล์และข้อมูลประจำตัว**

```bash
# 1. ตรวจสอบว่า .env.server อยู่ในรากของโครงการหรือไม่
ls -la .env.server
# ควรมีอยู่ใน: /path/to/sap-mcp/.env.server

# 2. ตรวจสอบว่า Gemini CLI settings.json มีพารามิเตอร์ "cwd" หรือไม่
cat ~/.gemini/settings.json
# ต้องรวม: "cwd": "/path/to/sap-mcp"

# 3. ทดสอบการตรวจสอบสิทธิ์ด้วยตนเอง
source .venv/bin/activate
python -c "from sap_mcp_server.config.settings import get_connection_config; print(get_connection_config())"
```

**ปัญหาทั่วไป**:

1. **ข้อผิดพลาด "Field required"**: `.env.server` ไม่ถูกโหลด ตรวจสอบ:
   - ไฟล์มีอยู่ในรากของโครงการ: `/path/to/your/sap-mcp/.env.server`
   - Gemini CLI `settings.json` มีพารามิเตอร์ `cwd` ที่ถูกต้อง
   - ไฟล์มีสิทธิ์ที่เหมาะสม: `chmod 600 .env.server`

2. **ข้อผิดพลาด 401 Unauthorized**: แก้ไขแล้วใน v0.2.1 (2025-01-22)
   - **ปัญหาก่อนหน้า**: SAP Gateway ปฏิเสธคำขอที่ไม่มีพารามิเตอร์ `sap-client`
   - **สถานะปัจจุบัน**: จัดการโดยอัตโนมัติ - คำขอทั้งหมดรวมพารามิเตอร์ `sap-client`
   - **การตรวจสอบ**: ตรวจสอบให้แน่ใจว่าคุณได้อัปเดตเป็น v0.2.1 หรือใหม่กว่า
   - **ตรวจสอบด้วยตนเอง**: การตรวจสอบสิทธิ์ควรสำเร็จด้วยข้อมูลประจำตัวที่ถูกต้อง

---

**ปัญหา: จำเป็นต้องลงทะเบียนเซิร์ฟเวอร์ใหม่**

```bash
# ลบการกำหนดค่าเซิร์ฟเวอร์ที่มีอยู่
rm ~/.gemini/settings.json

# หรือแก้ไขด้วยตนเองเพื่อลบรายการ sap-server
```

**วิธีแก้ปัญหา 4: การลงทะเบียนใหม่ทั้งหมด**

```bash
# วิธี 1: แก้ไขการตั้งค่าโดยตรง
vim ~/.gemini/settings.json

# วิธี 2: ใช้เส้นทางสัมบูรณ์ (แนะนำ)
# ทำตาม "วิธี A: การใช้เส้นทางสัมบูรณ์" ในส่วนที่ 3 ด้านบน
```

---

**ขั้นตอนการวินิจฉัยด่วน**

1. **ตรวจสอบไฟล์เรียกทำงานของเซิร์ฟเวอร์**:
```bash
/path/to/sap-mcp/.venv/bin/sap-mcp-server-stdio --help
# ควรแสดงข้อความเริ่มต้นเซิร์ฟเวอร์
```

2. **ตรวจสอบการตั้งค่า Gemini CLI**:
```bash
cat ~/.gemini/settings.json | grep -A 5 "sap-server"
# ตรวจสอบว่าเส้นทาง "command" ถูกต้อง
```

3. **ทดสอบการเชื่อมต่อ**:
```bash
gemini mcp list
# ควรแสดง: ✓ sap-server: ... - Connected
```

4. **ทดสอบใน Gemini CLI**:
```bash
gemini
> /mcp
> /mcp desc
# ควรแสดงรายการเครื่องมือ SAP
```

### เครื่องมือ SAP ที่มีอยู่ใน Gemini CLI

เมื่อลงทะเบียนแล้ว คุณสามารถใช้เครื่องมือ SAP เหล่านี้ผ่านภาษาธรรมชาติ:

| เครื่องมือ | คำอธิบาย | ตัวอย่างพรอมต์ |
|------|-------------|----------------|
| **sap_authenticate** | ตรวจสอบสิทธิ์กับ SAP Gateway | "ตรวจสอบสิทธิ์กับ SAP" |
| **sap_query** | สืบค้นเอนทิตี SAP ด้วยตัวกรอง OData | "แสดงสายการบินทั้งหมดโดยใช้บริการแนะนำการเดินทาง" |
| **sap_get_entity** | ดึงข้อมูลเอนทิตีเฉพาะด้วยคีย์ | "รับรายละเอียดสำหรับสนามบินแฟรงค์เฟิร์ต (FRA)" |
| **sap_list_services** | รายการบริการ SAP ที่มีอยู่ | "มีบริการ SAP อะไรบ้าง?" |

### ตัวอย่างเวิร์กโฟลว์

**1. เวิร์กโฟลว์การสอบถามเที่ยวบิน**

```bash
gemini

> เชื่อมต่อกับ SAP และค้นหาเที่ยวบิน Lufthansa ทั้งหมด
# Gemini จะ:
# 1. เรียก sap_authenticate
# 2. เรียก sap_query บน FlightSet ด้วยตัวกรอง "CARRID eq 'LH'"
# 3. จัดรูปแบบและนำเสนอผลลัพธ์
```

**2. การวิเคราะห์สนามบิน**

```bash
> รับรายละเอียดสำหรับสนามบินแฟรงค์เฟิร์ตและแสดงการเชื่อมต่อที่มีอยู่ให้ฉันดู
# Gemini จะ:
# 1. ตรวจสอบสิทธิ์
# 2. เรียก sap_get_entity สำหรับ 'FRA' บน AirportSet
# 3. เรียก sap_query บน ConnectionSet
# 4. นำเสนอข้อมูลเชิงลึก
```

**3. การค้นหาบริการ**

```bash
> บริการ SAP และชุดเอนทิตีใดบ้างที่มีอยู่ในระบบ?
# Gemini จะ:
# 1. เรียก sap_list_services
# 2. จัดรูปแบบแคตตาล็อกบริการ
```

---

## 🔧 เครื่องมือที่มีอยู่

### 1. SAP Authenticate

ตรวจสอบสิทธิ์กับระบบ SAP Gateway โดยใช้ข้อมูลประจำตัวจาก `.env.server`

**คำขอ**:
```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

**การตอบกลับ**:
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

สืบค้นเอนทิตี SAP ด้วยตัวกรอง OData, การเลือก, การแบ่งหน้า

**คำขอ**:
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

**การตอบกลับ**:
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

ดึงข้อมูลเอนทิตีเฉพาะด้วยคีย์

**คำขอ**:
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

**การตอบกลับ**:
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

รายการบริการ SAP ที่มีอยู่ทั้งหมดจากการกำหนดค่า

**คำขอ**:
```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

**การตอบกลับ**:
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

## 📚 ตัวอย่างการใช้งาน

### การใช้ Tool Registry

```python
from sap_mcp_server.tools import tool_registry
from sap_mcp_server.protocol.schemas import ToolCallRequest

# รายการเครื่องมือที่มีอยู่
tools = tool_registry.list_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")

# เรียกใช้เครื่องมือ
request = ToolCallRequest(
    name="sap_list_services",
    arguments={}
)
result = await tool_registry.call_tool(request)
print(result)
```

### ตัวอย่าง MCP Client

```python
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    # เชื่อมต่อกับเซิร์ฟเวอร์ MCP
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # เริ่มต้นเซสชัน
            await session.initialize()

            # ตรวจสอบสิทธิ์
            auth_result = await session.call_tool("sap_authenticate", {})

            # สืบค้นสายการบิน
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

### การบันทึกแบบมีโครงสร้าง

```python
from sap_mcp_server.utils.logger import setup_logging, get_logger

# การผลิต (JSON logs)
setup_logging(level="INFO", json_logs=True)

# การพัฒนา (colored console)
setup_logging(level="DEBUG", json_logs=False)

# ใช้ logger
logger = get_logger(__name__)
logger.info("Server started", port=8080, transport="stdio")
logger.error("Query failed", error=str(e), query=params)
```

### การตรวจสอบข้อมูลเข้า

```python
from sap_mcp_server.utils.validators import (
    validate_odata_filter,
    validate_entity_key,
    sanitize_input
)

# ตรวจสอบตัวกรอง OData
if validate_odata_filter("CARRID eq 'LH'"):
    # ปลอดภัยในการดำเนินการ
    pass

# ทำความสะอาดข้อมูลผู้ใช้
safe_input = sanitize_input(user_data, max_length=1000)

# ตรวจสอบคีย์เอนทิตี
if validate_entity_key(key):
    # ดึงข้อมูลเอนทิตี
    pass
```

---

## 🔒 ความปลอดภัย

### การป้องกันเชิงลึก

| เลเยอร์ | การดำเนินการ | สถานะ |
|-------|---------------|--------|
| **Input Validation** | ไวยากรณ์ OData, การป้องกัน SQL injection | ✅ |
| **Authentication** | การตรวจสอบข้อมูลประจำตัว, การจัดการเซสชัน | ✅ |
| **Authorization** | การควบคุมการเข้าถึงบริการ | ✅ |
| **Transport Security** | SSL/TLS, การตรวจสอบใบรับรอง | ✅ |
| **Audit Logging** | บันทึกแบบมีโครงสร้าง, ไม่มีข้อมูลที่ละเอียดอ่อน | ✅ |

### แนวทางปฏิบัติที่ดีที่สุด

1. **Credentials**: เก็บใน `.env.server`, ห้าม commit ลง git
2. **SSL/TLS**: เปิดใช้งานเสมอในการผลิต (`SAP_VERIFY_SSL=true`)
3. **Validation**: ตรวจสอบข้อมูลเข้าทั้งหมดก่อนเรียก SAP
4. **Logging**: ข้อมูลที่ละเอียดอ่อนถูกแยกออกจากบันทึก
5. **Error Handling**: ข้อความแสดงข้อผิดพลาดทั่วไปสำหรับลูกค้า

---

## 🎓 สถานการณ์สาธิต SAP SFLIGHT

### ภาพรวมสถานการณ์

ชุดข้อมูล SFLIGHT เป็นฐานข้อมูลตัวอย่างที่จัดทำโดย SAP ซึ่งรวมถึงข้อมูลสำหรับตารางการบิน สายการบิน สนามบิน และการจอง เป็นทรัพยากรที่ยอดเยี่ยมสำหรับการทดสอบและสาธิตการสร้างแบบจำลองข้อมูลและการสร้างบริการ

คู่มือนี้ถือว่าคุณมีบริการ OData ที่เปิดเผยชุดข้อมูลนี้ เป้าหมายคือการเชื่อมต่อเซิร์ฟเวอร์ SAP MCP ของเรากับบริการนี้และโต้ตอบกับมันโดยใช้ AI agents หรือลูกค้าอื่นๆ

**เอกสาร SAP อย่างเป็นทางการ:**
- [SAP Documentation - Flight Model](https://help.sap.com/SAPhelp_nw73/helpdata/en/cf/21f304446011d189700000e8322d00/frameset.htm)
- [SAP Help Portal - Flight Model](https://help.sap.com/docs/SAP_NETWEAVER_702/ff5206fc6c551014a1d28b076487e7df/cf21f304446011d189700000e8322d00.html)

---

### ข้อกำหนดเบื้องต้น

1. **ติดตั้ง SAP MCP Server แล้ว**: คุณต้องติดตั้งเซิร์ฟเวอร์ SAP MCP และมีสภาพแวดล้อม Python ที่ใช้งานได้ สำหรับคำแนะนำฉบับสมบูรณ์ โปรดดูที่ [ส่วนเริ่มต้นอย่างรวดเร็ว](#-quick-start)

2. **SFLIGHT OData Service**: บริการ OData ที่ใช้งานอยู่ที่เปิดเผยชุดข้อมูล SFLIGHT ต้องพร้อมใช้งานบนระบบ SAP Gateway ของคุณ
   - หากคุณต้องการสร้างบริการนี้ คุณสามารถทำตามคำแนะนำโดยละเอียดของเรา: [OData Service Creation Guide: FLIGHT Demo Scenario](./docs/guides/odata-service-creation-flight-demo.md)
   - สำหรับคู่มือนี้ เราจะถือว่าบริการชื่อ `Z_TRAVEL_RECOMMENDATIONS_SRV` ตามที่สร้างในคู่มือ

---

### คู่มือการสร้างบริการ OData

คู่มือนี้ให้คำแนะนำทีละขั้นตอนสำหรับการสร้างบริการ OData ในระบบ SAP โดยใช้ SAP Gateway Service Builder (`SEGW`) เพื่อเปิดเผยข้อมูลสถานการณ์ Flight ที่มีอยู่ในเวอร์ชัน SAP S/4HANA Fully Activated Appliance (FAA)

#### ภาพรวมสถานการณ์

* **เป้าหมาย:** เปิดเผยตารางการบิน การจอง และข้อมูลหลักที่เกี่ยวข้องผ่านบริการ OData
* **ความต้องการข้อมูลสถานการณ์:** ตารางการบิน, วันที่, เวลา, รายละเอียดสนามบิน, รายละเอียดสายการบิน, รายละเอียดผู้โดยสาร, ราคา ฯลฯ
* **ตาราง SAP ที่เกี่ยวข้อง:** `SFLIGHT`, `SPFLI`, `SCARR`, `SAIRPORT`, `SBOOK`, `SCUSTOM`

---

#### ขั้นตอนในการสร้างบริการ OData ใน SEGW

##### 1. เข้าถึง SAP Gateway Service Builder

ไปที่รหัสธุรกรรม SAP `SEGW`

##### 2. สร้างโครงการใหม่

1. คลิกปุ่ม "Create Project"
2. **Project Name:** กำหนดชื่อ (เช่น `Z_TRAVEL_RECOMMENDATIONS_SRV`)
3. **Description:** ระบุคำอธิบายที่มีความหมาย
4. **Package:** กำหนดให้กับแพ็คเกจ (เช่น `$TMP` สำหรับการพัฒนาในท้องถิ่นหรือแพ็คเกจที่ขนส่งได้)

##### 3. นำเข้าแบบจำลองข้อมูลจากโครงสร้าง DDIC

ขั้นตอนนี้กำหนดเอนทิตี OData ของคุณตามตาราง SAP พื้นฐาน

1. คลิกขวาที่โฟลเดอร์ "Data Model" ภายในโครงการของคุณ
2. เลือก **"Import" -> "DDIC Structure"**
3. ทำซ้ำขั้นตอนการนำเข้าสำหรับแต่ละตารางที่ต้องการ โดยระบุ **Entity Type Name** และเลือกฟิลด์ที่จำเป็น

***การดำเนินการที่จำเป็น:*** ตรวจสอบให้แน่ใจว่าฟิลด์คีย์ถูกทำเครื่องหมายอย่างถูกต้องในระหว่างกระบวนการนำเข้า

| โครงสร้าง DDIC | ชื่อประเภทเอนทิตี | ฟิลด์คีย์ที่แนะนำ | ฟิลด์ Payload ที่เกี่ยวข้อง (ตัวอย่าง) |
| :---- | :---- | :---- | :---- |
| `SFLIGHT` | **Flight** | `CARRID`, `CONNID`, `FLDATE` | `PRICE`, `CURRENCY`, `PLANETYPE`, `SEATSMAX`, `SEATSOCC` |
| `SPFLI` | **Connection** | `CARRID`, `CONNID` | `COUNTRYFR`, `CITYFROM`, `AIRPFROM`, `COUNTRYTO`, `CITYTO`, `AIRPTO`, `DEPTIME`, `ARRTIME`, `DISTANCE` |
| `SCARR` | **Airline** | `CARRID` | `CARRNAME`, `CURRCODE`, `URL` |
| `SAIRPORT` | **Airport** | `ID` | `NAME`, `CITY`, `COUNTRY` |
| `SBOOK` | **Booking** | `CARRID`, `CONNID`, `FLDATE`, `BOOKID` | `CUSTOMID`, `CUSTTYPE`, `SMOKER`, `LUGGWEIGHT`, `WUNIT`, `INVOICE`, `CLASS`, `FORCURAM`, `ORDER_DATE` |
| `SCUSTOM` | **Passenger** | `ID` | `NAME`, `FORM`, `STREET`, `POSTCODE`, `CITY`, `COUNTRY`, `PHONE` |

##### 4. กำหนด Associations และ Navigation Properties

Associations เชื่อมโยงเอนทิตีตามฟิลด์คีย์ Navigation Properties ช่วยให้แอปพลิเคชันไคลเอนต์สามารถข้ามความสัมพันธ์เหล่านี้ได้อย่างง่ายดาย (เช่น การใช้ `$expand`)

**ความสัมพันธ์เชิงตรรกะ:**

* **1:N:** Airline <-> Flights, Airline <-> Connections, Connection <-> Flights, Flight <-> Bookings, Passenger <-> Bookings
* **N:1:** Connection <-> Origin Airport, Connection <-> Destination Airport

**ขั้นตอนในการสร้าง Association:**

1. คลิกขวาที่ "Data Model" -> **"Create" -> "Association"**
2. กำหนด **Association Name**, **Principal Entity** (ฝั่ง 'หนึ่ง'), **Dependent Entity** (ฝั่ง 'หลาย'), และ **Cardinality** (เช่น 1:N)
3. ในหน้าจอถัดไป **Specify Key Mapping** โดยจับคู่ฟิลด์คีย์ระหว่าง Principal และ Dependent entities

**Associations เฉพาะที่จะสร้าง:**

| No. | ชื่อ Association | Principal:Dependent | Cardinality | Key Mapping |
| :---- | :---- | :---- | :---- | :---- |
| 1 | `Assoc_Airline_Flights` | `Airline` : `Flight` | 1:N | `Airline.CARRID` <-> `Flight.CARRID` |
| 2 | `Assoc_Airline_Connections` | `Airline` : `Connection` | 1:N | `Airline.CARRID` <-> `Connection.CARRID` |
| 3 | `Assoc_Connection_Flights` | `Connection` : `Flight` | 1:N | `CARRID` & `CONNID` (ทั้งสองทาง) |
| 4 | `Assoc_Flight_Bookings` | `Flight` : `Booking` | 1:N | `CARRID`, `CONNID`, `FLDATE` (ทั้งสามทาง) |
| 5 | `Assoc_Passenger_Bookings` | `Passenger` : `Booking` | 1:N | `Passenger.ID` <-> `Booking.CUSTOMID` |
| 6 | `Assoc_Connection_OriginAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPFROM` <-> `Airport.ID` |
| 7 | `Assoc_Connection_DestAirport` | `Connection` : `Airport` | N:1 | `Connection.AIRPTO` <-> `Airport.ID` |

**Navigation Properties ที่จะสร้าง:**

| เอนทิตี | ชื่อ Navigation Property | เอนทิตีเป้าหมาย | Association ที่ใช้ |
| :---- | :---- | :---- | :---- |
| **Airline** | `ToFlights`, `ToConnections` | `Flight`, `Connection` | `Assoc_Airline_Flights`, `Assoc_Airline_Connections` |
| **Flight** | `ToAirline`, `ToConnection`, `ToBookings` | `Airline`, `Connection`, `Booking` | `Assoc_Airline_Flights`, `Assoc_Connection_Flights`, `Assoc_Flight_Bookings` |
| **Connection** | `ToAirline`, `ToFlights`, `ToOriginAirport`, `ToDestinationAirport` | `Airline`, `Flight`, `Airport`, `Airport` | `Assoc_Airline_Connections`, `Assoc_Connection_Flights`, `Assoc_Connection_OriginAirport`, `Assoc_Connection_DestAirport` |
| **Booking** | `ToFlight`, `ToPassenger` | `Flight`, `Passenger` | `Assoc_Flight_Bookings`, `Assoc_Passenger_Bookings` |
| **Passenger** | `ToBookings` | `Booking` | `Assoc_Passenger_Bookings` |

##### 5. สร้าง Runtime Objects

1. คลิกปุ่ม **"Generate Runtime Objects"** (ไอคอนไม้กายสิทธิ์)
2. สิ่งนี้จะสร้างคลาส ABAP: Model Provider Class (MPC) และ Data Provider Class (DPC)
3. ยอมรับหรือปรับชื่อคลาสเริ่มต้น

##### 6. ใช้เมธอด Data Provider Class (DPC)

คลาสส่วนขยาย DPC ที่สร้างขึ้น (เช่น `ZCL_Z_TRAVEL_RECOM_DPC_EXT`) ใช้สำหรับตรรกะที่กำหนดเอง

* หากการจับคู่ตารางโดยตรงเพียงพอ การใช้งานพื้นฐานอาจเพียงพอ
* สำหรับการกรองที่กำหนดเอง การรวม การคำนวณ หรือการดำเนินการ Read/Create/Update/Delete (CRUD) ที่ซับซ้อน คุณต้องกำหนดเมธอดใหม่ เช่น `*_GET_ENTITY` (ระเบียนเดียว) และ `*_GET_ENTITYSET` (คอลเลกชัน) ในคลาสส่วนขยาย DPC

นี่คือตัวอย่างของเมธอด AIRLINESET_GET_ENTITYSET:

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

##### 7. ลงทะเบียนบริการ

1. ไปที่ธุรกรรม `/IWFND/MAINT_SERVICE`
2. คลิก **"Add Service"**
3. ป้อน **System Alias** สำหรับระบบแบ็กเอนด์ของคุณ (เช่น `LOCAL`)
4. ค้นหาบริการของคุณโดย **Technical Service Name** (เช่น `Z_TRAVEL_RECOMMENDATIONS_SRV`)
5. เลือกบริการและคลิก **"Add Selected Services"**
6. กำหนดแพ็คเกจและยืนยัน

##### 8. เปิดใช้งานและทดสอบบริการ

1. ใน `/IWFND/MAINT_SERVICE` ค้นหาบริการที่ลงทะเบียนใหม่ของคุณ
2. ตรวจสอบให้แน่ใจว่า **ICF node is active** (ไฟเขียว) หากไม่ ให้เลือกบริการ ไปที่ **"ICF Node" -> "Activate"**
3. เลือกบริการและคลิกปุ่ม **"SAP Gateway Client"**
4. **การทดสอบใน Gateway Client:**
   * ทดสอบการดึงข้อมูลคอลเลกชันเอนทิตี: คลิก **"EntitySets"** เลือก EntitySet (เช่น `AirlineCollection`) และคลิก **"Execute"**
   * ทดสอบคุณสมบัติ OData: ลองตัวเลือกการสืบค้นเช่น `$filter` และโดยเฉพาะ **`$expand`** เพื่อตรวจสอบว่าคุณสมบัติการนำทางทำงานอยู่ (เช่น `/FlightSet(key)?$expand=ToAirline`)

##### 9. จดบันทึก URL ของบริการ

URL บริการ OData สุดท้ายจะปรากฏใน Gateway Client โดยทั่วไปจะเป็นไปตามโครงสร้าง:

`/sap/opu/odata/sap/Z_TRAVEL_RECOMMENDATIONS_SRV/.` URL นี้คือสิ่งที่แอปพลิเคชันไคลเอนต์ (เช่น Fiori หรือแอปมือถือที่กำหนดเอง) จะใช้เพื่อใช้ข้อมูล SFLIGHT

---

## 🛠️ การพัฒนา

### การตั้งค่าโครงการ

```bash
# โคลนและตั้งค่า
git clone <repository-url>
cd sap-mcp

# สร้างสภาพแวดล้อมเสมือน
python3 -m venv .venv
source .venv/bin/activate

# ติดตั้งในโหมดการพัฒนา
cd packages/server
pip install -e ".[dev]"
```

### การเพิ่มเครื่องมือใหม่

1. **สร้างไฟล์เครื่องมือ**: `packages/server/src/sap_mcp_server/tools/my_tool.py`

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
        # การใช้งาน
        return {"result": "success"}
```

2. **ลงทะเบียนเครื่องมือ**: อัปเดต `packages/server/src/sap_mcp_server/tools/__init__.py`

```python
from .my_tool import MyNewTool

# เพิ่มลงในรีจิสทรี
tool_registry.register(MyNewTool())
```

3. **เพิ่มการทดสอบ**: `tests/unit/test_my_tool.py`

```python
import pytest
from sap_mcp_server.tools.my_tool import MyNewTool

@pytest.mark.asyncio
async def test_my_tool():
    tool = MyNewTool()
    result = await tool.execute({"param": "value"})
    assert result["result"] == "success"
```

### คุณภาพโค้ด

```bash
# จัดรูปแบบโค้ด
black packages/server/src

# เรียงลำดับการนำเข้า
isort packages/server/src

# Lint
flake8 packages/server/src

# ตรวจสอบประเภท
mypy packages/server/src

# สแกนความปลอดภัย
bandit -r packages/server/src

# ตรวจสอบคุณภาพทั้งหมด
black . && isort . && flake8 . && mypy . && bandit -r src/
```

---

## 📖 เอกสารประกอบ

- **[Server Package README](./packages/server/README.md)**: เอกสารประกอบเซิร์ฟเวอร์โดยละเอียด
- **[Configuration Guide](./docs/guides/configuration.md)**: การตั้งค่า YAML และสภาพแวดล้อม
- **[Deployment Guide](./docs/guides/deployment.md)**: การปรับใช้การผลิต
- **[Architecture Documentation](./docs/architecture/server.md)**: รายละเอียดสถาปัตยกรรมระบบ
- **[API Reference](./docs/api/)**: เอกสารประกอบเครื่องมือและโปรโตคอล

---

## 📝 ใบอนุญาต

MIT License - ดูไฟล์ [LICENSE](LICENSE) สำหรับรายละเอียด

---

## 🙏 กิตติกรรมประกาศ

- **MCP Protocol**: Anthropic's Model Context Protocol
- **SAP Gateway**: การรวม OData v2/v4
- **Community**: ผู้ร่วมสมทบและผู้ทดสอบ

---

<div align="center">

**Built with ❤️ for SAP integration via Model Context Protocol**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

**Production Ready** | **56% Coverage** | **98% Test Success**

</div>