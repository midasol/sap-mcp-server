# SAP MCP 프로젝트 리팩토링 가이드

## 📋 개요

이 가이드는 SAP MCP 프로젝트를 모노레포 구조로 리팩토링하는 단계별 절차를 제공합니다.

## 🎯 리팩토링 목표

### 현재 구조의 문제점
- ❌ 불필요한 추상화 계층 (`protocol/`)
- ❌ 미구현 SSE 서버 (`server.py`)
- ❌ 단일 파일에 모든 도구 집중 (`sap/tools.py`)
- ❌ 테스트 커버리지 부재
- ❌ 클라이언트 라이브러리 미구현

### 목표 구조
- ✅ 명확한 모듈 분리 (core, tools, config, transports, utils)
- ✅ 전송 계층 추상화 (stdio, SSE)
- ✅ 도구별 파일 분리
- ✅ 포괄적인 테스트 구조
- ✅ 실제 클라이언트 라이브러리 구현

## 📂 새로운 디렉토리 구조

```
sap-mcp/
├── packages/
│   ├── server/                        # 서버 패키지
│   │   ├── src/sap_mcp_server/
│   │   │   ├── core/                  # 핵심 비즈니스 로직
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sap_client.py      # SAP 클라이언트
│   │   │   │   ├── auth.py            # 인증
│   │   │   │   └── exceptions.py      # 예외
│   │   │   ├── tools/                 # MCP 도구 (세분화)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── auth_tool.py
│   │   │   │   ├── query_tool.py
│   │   │   │   ├── entity_tool.py
│   │   │   │   └── service_tool.py
│   │   │   ├── config/                # 설정
│   │   │   ├── transports/            # 전송 계층
│   │   │   └── utils/                 # 유틸리티
│   │   ├── tests/
│   │   └── config/
│   └── client/                        # 클라이언트 패키지
│       └── src/sap_mcp_client/
├── examples/                          # 통합 예제
├── docs/                              # 통합 문서
└── scripts/                           # 개발 스크립트
```

## 🚀 리팩토링 단계

### Phase 1: 준비 및 백업

```bash
# 1. 현재 상태 백업
cd /Users/sanggyulee/my-project/python-project/sap-mcp
git add .
git commit -m "Backup before refactoring"
git branch backup-pre-refactoring

# 2. 새 브랜치 생성
git checkout -b refactor/monorepo-structure
```

### Phase 2: 새 구조 생성

```bash
# 스크립트 실행
chmod +x scripts/create_structure.sh
./scripts/create_structure.sh
```

### Phase 3: 서버 코드 마이그레이션

#### 3.1 Core 모듈 복사 및 수정

```bash
# Core 모듈 복사
cp sap-mcp-server/src/sap_mcp/sap/client.py packages/server/src/sap_mcp_server/core/sap_client.py
cp sap-mcp-server/src/sap_mcp/sap/auth.py packages/server/src/sap_mcp_server/core/auth.py
cp sap-mcp-server/src/sap_mcp/sap/exceptions.py packages/server/src/sap_mcp_server/core/exceptions.py
```

**Import 경로 수정 필요:**
```python
# Before
from ..config.settings import SAPConnectionConfig
from .auth import SAPAuthenticator

# After
from sap_mcp_server.config.settings import SAPConnectionConfig
from sap_mcp_server.core.auth import SAPAuthenticator
```

#### 3.2 Config 모듈 복사

```bash
cp sap-mcp-server/src/sap_mcp/config/*.py packages/server/src/sap_mcp_server/config/
mv packages/server/src/sap_mcp_server/config/services_loader.py packages/server/src/sap_mcp_server/config/loader.py
```

#### 3.3 Tools 모듈 분리

기존 `sap/tools.py`를 개별 파일로 분리:

```bash
# 실행 스크립트 사용
python scripts/split_tools.py
```

또는 수동 분리:
1. `tools/base.py` - BaseSAPTool 추상 클래스
2. `tools/auth_tool.py` - SAPAuthenticateTool
3. `tools/query_tool.py` - SAPQueryTool
4. `tools/entity_tool.py` - SAPGetEntityTool
5. `tools/service_tool.py` - SAPListServicesTool

### Phase 4: 전송 계층 구현

#### 4.1 Stdio Transport

`packages/server/src/sap_mcp_server/transports/stdio.py` 생성:

```python
"""Stdio transport for MCP server"""
import asyncio
import logging
from typing import Optional

import mcp.server.stdio
from mcp.server import Server

from sap_mcp_server.config.settings import get_config
from sap_mcp_server.tools import register_all_tools

logger = logging.getLogger(__name__)


class StdioTransport:
    """Stdio-based MCP transport"""

    def __init__(self, server: Optional[Server] = None):
        self.server = server or Server("sap-mcp-server")
        self.config = get_config()

    async def start(self) -> None:
        """Start stdio transport server"""
        logger.info("Starting SAP MCP Server (stdio)")

        # Register tools
        register_all_tools(self.server)

        # Start stdio server
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


async def main():
    """Main entry point for stdio server"""
    from dotenv import load_dotenv
    load_dotenv(".env.server")

    transport = StdioTransport()
    await transport.start()


if __name__ == "__main__":
    asyncio.run(main())
```

#### 4.2 SSE Transport (향후 구현)

`packages/server/src/sap_mcp_server/transports/sse.py`:

```python
"""SSE transport for MCP server (TODO)"""
# 향후 구현 예정
```

### Phase 5: 설정 통합

#### 5.1 서버 pyproject.toml

```toml
[project]
name = "sap-mcp-server"
version = "0.2.0"
description = "SAP MCP Server - Refactored monorepo version"

[project.scripts]
sap-mcp-server-stdio = "sap_mcp_server.transports.stdio:main"
```

#### 5.2 클라이언트 구현

`packages/client/src/sap_mcp_client/client.py`:

```python
"""High-level SAP MCP Client"""
from typing import Any, Dict, List, Optional
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

class SAPMCPClient:
    """High-level client for SAP MCP Server"""

    def __init__(self, server_command: str = "sap-mcp-server-stdio"):
        self.server_command = server_command
        self.session: Optional[ClientSession] = None

    async def __aenter__(self):
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "sap_mcp_server.transports.stdio"]
        )

        self.transport = await stdio_client(server_params).__aenter__()
        read, write = self.transport

        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()

        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.__aexit__(*args)
        await self.transport.__aexit__(*args)

    async def authenticate(self) -> bool:
        """Authenticate with SAP"""
        result = await self.session.call_tool("sap_authenticate", {})
        return bool(result)

    async def get_order(self, service: str, entity_set: str, order_id: str) -> Dict[str, Any]:
        """Get order by ID"""
        result = await self.session.call_tool(
            "sap_get_entity",
            {
                "service": service,
                "entity_set": entity_set,
                "entity_key": order_id
            }
        )
        return result
```

### Phase 6: 테스트 추가

#### 6.1 Unit Tests

`packages/server/tests/unit/test_sap_client.py`:

```python
import pytest
from sap_mcp_server.core.sap_client import SAPClient
from sap_mcp_server.config.settings import SAPConnectionConfig

@pytest.mark.asyncio
async def test_sap_client_initialization():
    config = SAPConnectionConfig(
        host="test-host",
        port=443,
        username="test",
        password="test",
        client="100"
    )

    async with SAPClient(config) as client:
        assert client.base_url == "https://test-host:443"
```

#### 6.2 Integration Tests

`packages/server/tests/integration/test_sap_integration.py`:

```python
import pytest
import os

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_sap_connection():
    """Test with real SAP system (requires env vars)"""
    if not os.getenv("SAP_HOST"):
        pytest.skip("SAP credentials not configured")

    # Test실제 SAP 연결
```

### Phase 7: 예제 및 문서 정리

#### 7.1 예제 이동

```bash
# 챗봇 예제
cp sap-mcp-client/examples/order_inquiry_chatbot.py examples/chatbot/
cp sap-mcp-client/examples/stdio_client.py examples/basic/
```

#### 7.2 문서 통합

```bash
# 아키텍처 문서
cp sap-mcp-server/ARCHITECTURE.md docs/architecture/server.md

# 가이드 문서
cp sap-mcp-server/CONFIGURATION_GUIDE.md docs/guides/configuration.md
cp sap-mcp-server/DEPLOYMENT.md docs/guides/deployment.md
```

### Phase 8: 검증 및 테스트

```bash
# 1. 서버 패키지 설치
cd packages/server
pip install -e ".[dev]"

# 2. 테스트 실행
pytest tests/

# 3. 서버 시작 테스트
python -m sap_mcp_server.transports.stdio

# 4. 클라이언트 테스트
cd ../client
pip install -e ".[dev]"
python -c "from sap_mcp_client import SAPMCPClient; print('OK')"
```

### Phase 9: 정리 및 커밋

```bash
# 1. 이전 디렉토리 제거
rm -rf sap-mcp-server/src/sap_mcp/sap
rm -rf sap-mcp-server/src/sap_mcp/protocol
rm sap-mcp-server/src/sap_mcp/server.py

# 2. 변경사항 커밋
git add .
git commit -m "refactor: Migrate to monorepo structure with separated concerns

- Split server into core, tools, config, transports, utils
- Implement transport layer abstraction
- Separate tools into individual files
- Add comprehensive test structure
- Implement high-level client library
- Reorganize examples and documentation
"

# 3. 메인 브랜치 병합
git checkout main
git merge refactor/monorepo-structure
```

## 🔧 유틸리티 스크립트

### scripts/create_structure.sh

```bash
#!/bin/bash
# 새 디렉토리 구조 생성 스크립트

echo "Creating new directory structure..."

# Server structure
mkdir -p packages/server/src/sap_mcp_server/{core,tools,config,transports,utils}
mkdir -p packages/server/tests/{unit,integration}
mkdir -p packages/server/config

# Client structure
mkdir -p packages/client/src/sap_mcp_client/transports
mkdir -p packages/client/tests/{unit,integration}

# Shared directories
mkdir -p examples/{basic,chatbot,advanced}
mkdir -p docs/{architecture,guides,api,examples}
mkdir -p scripts

# Create __init__.py files
find packages -type d -name "sap_mcp_server" -o -name "sap_mcp_client" | while read dir; do
    find "$dir" -type d -exec touch {}/__init__.py \;
done

echo "Directory structure created successfully!"
```

### scripts/update_imports.py

```python
#!/usr/bin/env python3
"""Update import statements in migrated files"""

import os
import re
from pathlib import Path

IMPORT_MAPPINGS = {
    r'from \.\.config\.': 'from sap_mcp_server.config.',
    r'from \.\.sap\.': 'from sap_mcp_server.core.',
    r'from \.auth import': 'from sap_mcp_server.core.auth import',
    r'from \.exceptions import': 'from sap_mcp_server.core.exceptions import',
    r'from \.\.protocol\.': 'from sap_mcp_server.tools.',
}

def update_file_imports(file_path: Path):
    """Update imports in a single file"""
    content = file_path.read_text()
    original = content

    for pattern, replacement in IMPORT_MAPPINGS.items():
        content = re.sub(pattern, replacement, content)

    if content != original:
        file_path.write_text(content)
        print(f"Updated: {file_path}")

def main():
    """Main function"""
    server_src = Path("packages/server/src/sap_mcp_server")

    for py_file in server_src.rglob("*.py"):
        if py_file.name != "__init__.py":
            update_file_imports(py_file)

if __name__ == "__main__":
    main()
```

## ✅ 체크리스트

### Phase 1: 준비
- [ ] 현재 코드 백업
- [ ] 새 브랜치 생성
- [ ] 의존성 목록 확인

### Phase 2: 구조 생성
- [ ] 디렉토리 구조 생성
- [ ] `__init__.py` 파일 생성

### Phase 3: 서버 마이그레이션
- [ ] Core 모듈 복사
- [ ] Import 경로 수정
- [ ] Config 모듈 복사
- [ ] Tools 분리

### Phase 4: 전송 계층
- [ ] Stdio transport 구현
- [ ] SSE transport 스텁 생성

### Phase 5: 클라이언트 구현
- [ ] 고수준 클라이언트 API
- [ ] 타입 정의
- [ ] 예외 처리

### Phase 6: 테스트
- [ ] Unit 테스트 추가
- [ ] Integration 테스트 추가
- [ ] pytest 설정

### Phase 7: 문서
- [ ] 예제 정리
- [ ] 문서 통합
- [ ] README 업데이트

### Phase 8: 검증
- [ ] 서버 시작 테스트
- [ ] 클라이언트 테스트
- [ ] 전체 테스트 실행

### Phase 9: 완료
- [ ] 이전 코드 제거
- [ ] 변경사항 커밋
- [ ] PR 생성

## 🚨 주의사항

1. **백업 필수**: 리팩토링 전 반드시 백업
2. **단계적 진행**: 한 번에 모든 것을 변경하지 말 것
3. **테스트 우선**: 각 단계마다 테스트 실행
4. **Import 경로**: 모든 import 경로 확인
5. **환경 변수**: `.env.server` 파일 경로 확인

## 📊 예상 소요 시간

| Phase | 작업 | 소요 시간 |
|-------|------|----------|
| 1-2 | 준비 및 구조 생성 | 30분 |
| 3 | 서버 마이그레이션 | 2시간 |
| 4 | 전송 계층 구현 | 1시간 |
| 5 | 클라이언트 구현 | 2시간 |
| 6 | 테스트 추가 | 2시간 |
| 7 | 문서 정리 | 1시간 |
| 8 | 검증 | 1시간 |
| 9 | 정리 | 30분 |
| **합계** | | **약 10시간** |

## 🎓 학습 자료

- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
- [Monorepo vs Polyrepo](https://monorepo.tools/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 🆘 문제 해결

### Import 오류
```bash
# Python 경로 확인
python -c "import sys; print('\n'.join(sys.path))"

# 패키지 설치 확인
pip show sap-mcp-server
```

### 테스트 실패
```bash
# 상세 로그 출력
pytest -vv --log-cli-level=DEBUG

# 특정 테스트만 실행
pytest tests/unit/test_sap_client.py::test_specific
```

---

**작성일**: 2025-01-15
**버전**: 1.0
**작성자**: Claude Code
