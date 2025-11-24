# SAP MCP - Model Context Protocol을 통한 SAP Gateway 통합

AI 에이전트와 애플리케이션이 깔끔한 모듈식 아키텍처를 통해 SAP Gateway 시스템과 상호 작용할 수 있도록 지원하는 프로덕션 등급의 MCP(Model Context Protocol) 서버입니다. 신뢰성, 보안 및 개발자 경험을 위해 구축되었습니다.

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-44%2F45%20passing-success.svg)]()

</div>

---

## 🎯 프로젝트 개요

AI 에이전트와 애플리케이션이 깔끔한 모듈식 아키텍처를 통해 SAP Gateway 시스템과 상호 작용할 수 있도록 지원하는 프로덕션 등급의 MCP(Model Context Protocol) 서버입니다. 신뢰성, 보안 및 개발자 경험을 위해 구축되었습니다.

**현재 상태**: ✅ **프로덕션 준비 완료** (5단계 모두 완료)

### 주요 특징

- 🔐 **안전한 SAP 통합**: 엔터프라이즈급 인증 및 SSL/TLS 지원
- 🛠️ **4가지 모듈식 도구**: 인증, 쿼리, 엔티티 조회, 서비스 검색
- 🚀 **Stdio 전송**: 프로덕션 등급 MCP 서버
- 📊 **구조화된 로깅**: 성능 지표를 포함한 JSON 및 콘솔 형식
- ✅ **검증된 입력**: 포괄적인 OData 및 보안 검증
- 🧪 **철저한 테스트**: 56% 커버리지, 44/45 테스트 통과 (98% 성공률)

---

## 📐 아키텍처

### 시스템 개요

<details>
<summary>📊 시스템 개요 다이어그램 보기 (클릭)</summary>

```mermaid
graph TB
    subgraph clients["🎯 Client Applications"]
        direction TB
        A1["AI Agent<br/><small>LLM/GenAI Integration</small>"]
        A2["Python Client<br/><small>SDK & Libraries</small>"]
        A3["Order Chatbot<br/><small>Example Application</small>"]
    end

    subgraph transport["🚀 MCP Server Layer"]
        direction TB
        B1["Stdio Transport<br/><small>stdin/stdout Stream</small>"]
    end

    subgraph registry["🛠️ Tool Registry"]
        direction LR
        C1["sap_authenticate<br/><small>Authentication</small>"]
        C2["sap_query<br/><small>OData Queries</small>"]
        C3["sap_get_entity<br/><small>Entity Retrieval</small>"]
        C4["sap_list_services<br/><small>Service Discovery</small>"]
    end

    subgraph core["⚡ Core Layer"]
        direction LR
        D1["SAP Client<br/><small>OData Handler</small>"]
        D2["Auth Manager<br/><small>Credentials</small>"]
        D3["Config Loader<br/><small>YAML/ENV</small>"]
    end

    subgraph utils["🔧 Utilities"]
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

### 컴포넌트 상세

<details>
<summary>🔧 컴포넌트 상세 다이어그램 보기 (클릭)</summary>

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

### 데이터 흐름: 주문 조회 예시

<details>
<summary>🔄 데이터 흐름 다이어그램 보기 (클릭)</summary>

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

### 도구 실행 흐름

<details>
<summary>⚡ 도구 실행 흐름 다이어그램 보기 (클릭)</summary>

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

### 보안 아키텍처

<details>
<summary>🔒 보안 아키텍처 다이어그램 보기 (클릭)</summary>

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

## 📦 저장소 구조

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

## ✨ 기능

### 핵심 기능

<table>
<tr>
<td width="50%">

#### 🛠️ 도구
- ✅ **sap_authenticate**: 안전한 SAP 인증
- ✅ **sap_query**: 필터가 있는 OData 쿼리
- ✅ **sap_get_entity**: 단일 엔티티 조회
- ✅ **sap_list_services**: 서비스 검색

</td>
<td width="50%">

#### 🚀 전송
- ✅ **Stdio**: 프로덕션 등급 stdin/stdout

</td>
</tr>
<tr>
<td>

#### 📊 로깅 및 모니터링
- ✅ **구조화된 로깅**: JSON + 콘솔
- ✅ **성능 지표**: 요청 타이밍
- ✅ **오류 추적**: 전체 컨텍스트
- ✅ **감사 추적**: 보안 이벤트

</td>
<td>

#### 🔒 보안
- ✅ **입력 검증**: OData 및 보안
- ✅ **SSL/TLS 지원**: 안전한 연결
- ✅ **자격 증명 관리**: .env.server
- ✅ **오류 처리**: 프로덕션 등급

</td>
</tr>
</table>

### 개발자 경험

- ✅ **모듈식 아키텍처**: 파일당 하나의 도구
- ✅ **타입 안전성**: 전체 타입 힌트
- ✅ **문서화**: 포괄적인 가이드
- ✅ **쉬운 설정**: `pip install -e .`
- ✅ **핫 리로드**: 개발 모드
- ✅ **예제 앱**: 3개의 작동 예제

---

## 📋 Preparation

### Prerequisites for MCP Server

#### 시스템 요구 사항

- **Python 3.11 이상**
- **pip** (Python 패키지 설치 관리자)
- **Git** (저장소 복제용)
- SAP Gateway 액세스 자격 증명
- 가상 환경 지원

#### Python 설치

<details>
<summary><b>🪟 Windows</b></summary>

**옵션 1: Microsoft Store (Windows 10/11 권장)**
```powershell
# Microsoft Store에서 "Python 3.11" 또는 "Python 3.12" 검색
# 또는 python.org에서 다운로드
```

**옵션 2: Python.org 설치 관리자**
1. [python.org/downloads](https://www.python.org/downloads/)에서 다운로드
2. 설치 관리자 실행
3. ✅ **"Add Python to PATH" 체크**
4. "Install Now" 클릭

**설치 확인:**
```powershell
python --version
# 표시되어야 함: Python 3.11.x or higher

pip --version
# 표시되어야 함: pip 23.x.x or higher
```

**일반적인 문제:**
- `python` 명령을 찾을 수 없는 경우 `python3` 또는 `py` 시도
- `pip`를 찾을 수 없는 경우 설치: `python -m ensurepip --upgrade`

</details>

<details>
<summary><b>🍎 macOS</b></summary>

**옵션 1: Homebrew (권장)**
```bash
# Homebrew가 설치되지 않은 경우 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.11
# 또는
brew install python@3.12
```

**옵션 2: Python.org 설치 관리자**
1. [python.org/downloads/macos](https://www.python.org/downloads/macos/)에서 다운로드
2. `.pkg` 파일 열기
3. 설치 마법사 따르기

**설치 확인:**
```bash
python3 --version
# 표시되어야 함: Python 3.11.x or higher

pip3 --version
# 표시되어야 함: pip 23.x.x or higher
```

**참고:** macOS에는 Python 2.7이 사전 설치되어 있을 수 있습니다. 항상 `python3` 및 `pip3` 명령을 사용하십시오.

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Ubuntu/Debian:**
```bash
# 패키지 목록 업데이트
sudo apt update

# Python 3.11+ 설치
sudo apt install python3.11 python3.11-venv python3-pip

# 또는 최신 Python 설치
sudo apt install python3 python3-venv python3-pip
```

**Fedora/RHEL/CentOS:**
```bash
# Python 3.11+ 설치
sudo dnf install python3.11 python3-pip

# 또는
sudo yum install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**설치 확인:**
```bash
python3 --version
# 표시되어야 함: Python 3.11.x or higher

pip3 --version
# 표시되어야 함: pip 23.x.x or higher
```

</details>

---

### 1. 설치

#### 단계별 설치

<details open>
<summary><b>🪟 Windows (PowerShell/명령 프롬프트)</b></summary>

```powershell
# 저장소 복제
git clone <repository-url>
cd sap-mcp

# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화
.venv\Scripts\activate
# 또는 PowerShell에서:
# .venv\Scripts\Activate.ps1

# PowerShell에서 실행 정책 오류가 발생하는 경우:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 활성화 확인 (프롬프트에 (.venv)가 표시되어야 함)
# (.venv) PS C:\path\to\sap-mcp>

# 서버 패키지 설치
cd packages\server
pip install -e .

# 개발 의존성 설치 (선택 사항)
pip install -e ".[dev]"

# 설치 확인
sap-mcp-server-stdio --help
```

**Windows 일반적인 문제:**
- **`python`을 찾을 수 없음**: `python3` 또는 `py` 시도
- **액세스 거부됨**: PowerShell을 관리자 권한으로 실행
- **실행 정책**: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 실행
- **긴 경로 지원**: Windows에서 긴 경로 활성화 (설정 > 시스템 > 정보 > 고급 시스템 설정)

</details>

<details>
<summary><b>🍎 macOS (터미널)</b></summary>

```bash
# 저장소 복제
git clone <repository-url>
cd sap-mcp

# 가상 환경 생성
python3 -m venv .venv

# 가상 환경 활성화
source .venv/bin/activate

# 활성화 확인 (프롬프트에 (.venv)가 표시되어야 함)
# (.venv) user@macbook sap-mcp %

# 서버 패키지 설치
cd packages/server
pip install -e .

# 개발 의존성 설치 (선택 사항)
pip install -e ".[dev]"

# 설치 확인
sap-mcp-server-stdio --help

# 설치 경로 확인 (Gemini CLI 설정에 유용)
which sap-mcp-server-stdio
# 예시 출력: /Users/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**macOS 일반적인 문제:**
- **`python`을 찾을 수 없음**: 대신 `python3` 사용
- **`pip`를 찾을 수 없음**: 대신 `pip3` 사용
- **액세스 거부됨**: 가상 환경에서 `sudo`를 사용하지 마십시오
- **설치 후 명령을 찾을 수 없음**: 가상 환경이 활성화되었는지 확인하십시오

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 저장소 복제
git clone <repository-url>
cd sap-mcp

# 가상 환경 생성
python3 -m venv .venv

# 가상 환경 활성화
source .venv/bin/activate

# 활성화 확인 (프롬프트에 (.venv)가 표시되어야 함)
# (.venv) user@linux:~/sap-mcp$

# 서버 패키지 설치
cd packages/server
pip install -e .

# 개발 의존성 설치 (선택 사항)
pip install -e ".[dev]"

# 설치 확인
sap-mcp-server-stdio --help

# 설치 경로 확인 (Gemini CLI 설정에 유용)
which sap-mcp-server-stdio
# 예시 출력: /home/username/sap-mcp/.venv/bin/sap-mcp-server-stdio
```

**Linux 일반적인 문제:**
- **`python3-venv`를 찾을 수 없음**: `sudo apt install python3-venv`로 설치
- **액세스 거부됨**: 가상 환경에서 `sudo`를 사용하지 마십시오
- **SSL 오류**: 인증서 설치: `sudo apt install ca-certificates`
- **빌드 의존성 누락**: `sudo apt install build-essential python3-dev`로 설치

</details>

---

### 2. 구성

SAP MCP 서버에는 두 개의 구성 파일이 필요합니다:
1. **`.env.server`**: SAP 연결 자격 증명 (단일 SAP 시스템)
2. **`services.yaml`**: SAP Gateway 서비스 및 인증 설정

#### 2.1. SAP 연결 구성 (`.env.server`)

> **⚠️ 중요**: v0.2.0부터 `.env.server`가 **프로젝트 루트 디렉토리**로 통합되었습니다. 이전 `packages/server/.env.server` 위치는 더 이상 지원되지 않습니다.

**파일 위치**: `.env.server`는 반드시 **프로젝트 루트 디렉토리**에 있어야 합니다.

```
sap-mcp/
├── .env.server              ← 구성 파일 (유일한 위치 - 여기에 생성)
├── .env.server.example      ← 예제 템플릿
├── packages/
├── server/
└── README.md
```

**설정 단계**:

<details open>
<summary><b>🪟 Windows (PowerShell/명령 프롬프트)</b></summary>

```powershell
# 프로젝트 루트로 이동
cd C:\path\to\sap-mcp

# 환경 템플릿 복사
copy .env.server.example .env.server

# 메모장으로 구성 편집 및 SAP 자격 증명 입력
notepad .env.server

# 또는 선호하는 편집기 사용:
# code .env.server (VS Code)
# notepad++ .env.server (Notepad++)

# 참고: Windows에서는 파일 권한이 다르게 관리됩니다
# 파일이 공용 폴더에 없는지 확인하십시오
# .env.server 우클릭 > 속성 > 보안에서 액세스 제한
```

**Windows 관련 참고 사항:**
- Windows 경로에는 백슬래시(`\`) 사용
- PowerShell 실행 정책이 스크립트를 차단할 수 있음 (설치 섹션 참조)
- `.env.server`를 액세스가 제한된 사용자 폴더에 저장
- 바이러스 백신이 파일을 차단하는 경우 Windows Defender 제외 사용

</details>

<details>
<summary><b>🍎 macOS (터미널)</b></summary>

```bash
# 프로젝트 루트로 이동
cd /path/to/your/sap-mcp

# 환경 템플릿 복사
cp .env.server.example .env.server

# 구성 편집 및 SAP 자격 증명 입력
nano .env.server
# 또는 선호하는 편집기 사용:
# vim .env.server
# code .env.server (VS Code)
# open -a TextEdit .env.server

# 적절한 권한 설정 (보안 권장)
chmod 600 .env.server

# 권한 확인
ls -la .env.server
# 표시되어야 함: -rw------- (소유자만 읽기/쓰기 가능)
```

**macOS 관련 참고 사항:**
- 파일 권한은 Unix 기반 (Linux와 동일)
- `chmod 600`은 사용자만 파일을 읽고 쓸 수 있도록 보장
- macOS는 처음 액세스할 때 추가 보안 프롬프트가 표시될 수 있음
- 최상의 보안을 위해 홈 디렉토리에 저장

</details>

<details>
<summary><b>🐧 Linux (Bash/Zsh)</b></summary>

```bash
# 프로젝트 루트로 이동
cd /path/to/your/sap-mcp

# 환경 템플릿 복사
cp .env.server.example .env.server

# 구성 편집 및 SAP 자격 증명 입력
nano .env.server
# 또는 선호하는 편집기 사용:
# vim .env.server
# code .env.server (VS Code)
# gedit .env.server (GNOME)

# 적절한 권한 설정 (보안 필수)
chmod 600 .env.server

# 권한 확인
ls -la .env.server
# 표시되어야 함: -rw------- (소유자만 읽기/쓰기 가능)

# 선택 사항: 파일이 전체 읽기 가능이 아닌지 확인
stat .env.server
```

**Linux 관련 참고 사항:**
- `chmod 600`은 보안에 중요 (소유자만 액세스 가능)
- SELinux/AppArmor에 추가 구성이 필요할 수 있음
- 파일은 서버를 실행하는 사용자가 소유해야 함
- 이 파일을 편집하거나 실행할 때 절대 `sudo`를 사용하지 마십시오

</details>

#### 2.2. 서비스 구성 (`services.yaml`)

`services.yaml` 파일은 SAP Gateway 서비스와 해당 인증 설정을 정의합니다.

**파일 위치**: `packages/server/config/services.yaml`

```yaml
# packages/server/config/services.yaml 예시

services:
  # 서비스 1: 비즈니스 파트너 (기본 인증)
  - name: "API_BUSINESS_PARTNER"
    path: "/sap/opu/odata/sap/API_BUSINESS_PARTNER"
    auth_config:
      auth_type: "basic"    # 사용자 이름/비밀번호 인증
      sap_client: "100"     # SAP 클라이언트 ID

  # 서비스 2: 판매 주문 (인증 없음/공개)
  - name: "API_SALES_ORDER_SRV"
    path: "/sap/opu/odata/sap/API_SALES_ORDER_SRV"
    auth_config:
      auth_type: "none"     # 인증 필요 없음

  # 서비스 3: 제품 마스터 (사용자 지정 클라이언트)
  - name: "API_PRODUCT_SRV"
    path: "/sap/opu/odata/sap/API_PRODUCT_SRV"
    auth_config:
      auth_type: "basic"
      sap_client: "200"     # 다른 클라이언트 ID
```

**구성 옵션:**
- `name`: 서비스의 고유 식별자 (도구 호출에 사용됨)
- `path`: SAP Gateway의 OData 서비스 경로
- `auth_config`:
  - `auth_type`: `basic` (사용자/비번) 또는 `none` (공개)
  - `sap_client`: (선택 사항) SAP 클라이언트 ID (예: 100, 200). 기본값은 `.env.server`의 설정입니다.

---

### 3. Gemini CLI 통합

Google Gemini CLI와 함께 SAP MCP 서버를 사용하여 AI 에이전트 기능을 활성화하십시오.

#### 구성 파일 (`gemini_config.yml`)

프로젝트 루트에 `gemini_config.yml` 파일을 생성하거나 업데이트하십시오:

<details open>
<summary><b>🪟 Windows (PowerShell)</b></summary>

```yaml
# gemini_config.yml
mcpServers:
  sap-mcp:
    command: "uv"
    args:
      - "run"
      - "--directory"
      - "C:\\path\\to\\sap-mcp\\packages\\server" # 절대 경로 사용
      - "sap-mcp-server-stdio"
    env:
      PYTHONPATH: "C:\\path\\to\\sap-mcp\\packages\\server\\src"
```

</details>

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```yaml
# gemini_config.yml
mcpServers:
  sap-mcp:
    command: "uv"
    args:
      - "run"
      - "--directory"
      - "/Users/username/sap-mcp/packages/server" # 절대 경로 사용
      - "sap-mcp-server-stdio"
    env:
      PYTHONPATH: "/Users/username/sap-mcp/packages/server/src"
```

</details>

**참고:** `uv`를 사용하지 않는 경우 `command`를 `python` 또는 `python3`로 변경하고 `args`를 조정하여 스크립트를 직접 실행하십시오. 하지만 의존성 관리를 위해 `uv`를 권장합니다.

---

### 4. 사용법

#### 사용 가능한 도구

| 도구 이름 | 설명 | 필수 매개변수 |
|-----------|-------------|---------------------|
| `sap_authenticate` | SAP Gateway 세션 설정 | 없음 (env의 자격 증명 사용) |
| `sap_query` | OData 쿼리 실행 (필터링, 선택) | `service_name`, `entity_set` |
| `sap_get_entity` | 키로 단일 엔티티 조회 | `service_name`, `entity_set`, `keys` |
| `sap_list_services` | 사용 가능한 SAP 서비스 나열 | 없음 |

#### 예시: AI 에이전트 프롬프트

Gemini CLI가 실행 중일 때 다음과 같이 자연어로 요청할 수 있습니다:

> "SAP에 로그인해서 비즈니스 파트너 목록을 보여줘."

> "주문 번호 1000의 상세 정보를 찾아줘."

> "제품 서비스에서 가격이 500 이상인 제품을 검색해줘."

#### 예시: Python 클라이언트

`examples/basic/stdio_client.py`를 참조하여 Python 코드에서 직접 MCP 서버와 통신하는 방법을 확인하십시오.

```python
# 클라이언트 초기화 및 연결
async with StdioServerParameters(command="...", args=[...]) as params:
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. 초기화
            await session.initialize()

            # 2. 도구 목록 조회
            tools = await session.list_tools()

            # 3. 인증 도구 호출
            await session.call_tool("sap_authenticate", {})

            # 4. 쿼리 도구 호출
            result = await session.call_tool("sap_query", {
                "service_name": "API_BUSINESS_PARTNER",
                "entity_set": "A_BusinessPartner",
                "top": 5
            })
```

---



---

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.

## 🙏 감사의 말

- [Model Context Protocol](https://modelcontextprotocol.io/) - 개방형 표준
- [SAP OData](https://www.sap.com/products/technology-platform/odata.html) - 표준 프로토콜