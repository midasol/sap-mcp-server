# SAP MCP 리팩토링 요약

## 📋 실행 가이드

이 프로젝트를 새로운 모노레포 구조로 리팩토링하기 위한 단계별 가이드입니다.

## 🚀 빠른 시작

```bash
# 1. 백업 생성
git add .
git commit -m "Backup before refactoring"
git branch backup-pre-refactoring

# 2. 새 브랜치 생성
git checkout -b refactor/monorepo-structure

# 3. 구조 생성
./scripts/create_structure.sh

# 4. 코드 마이그레이션
./scripts/migrate_code.sh

# 5. Import 경로 수정
python scripts/update_imports.py

# 6. 검증
cd packages/server
pip install -e ".[dev]"
pytest tests/ -v
```

## 📂 새로운 구조 개요

### Before (현재 구조)
```
sap-mcp/
├── sap-mcp-server/
│   └── src/sap_mcp/
│       ├── sap/              # SAP 로직
│       ├── protocol/         # 불필요한 래퍼
│       ├── config/          # 설정
│       ├── server.py        # 미구현
│       └── stdio_server.py  # 현재 서버
└── sap-mcp-client/
    └── examples/            # 예제만 있음
```

### After (목표 구조)
```
sap-mcp/
├── packages/
│   ├── server/
│   │   ├── src/sap_mcp_server/
│   │   │   ├── core/        # SAP 클라이언트 로직
│   │   │   ├── tools/       # MCP 도구 (분리)
│   │   │   ├── config/      # 설정 관리
│   │   │   ├── transports/  # stdio, SSE
│   │   │   └── utils/       # 유틸리티
│   │   └── tests/           # 테스트
│   └── client/
│       ├── src/sap_mcp_client/  # 실제 클라이언트 라이브러리
│       └── tests/
├── examples/                # 통합 예제
├── docs/                    # 통합 문서
└── scripts/                 # 개발 스크립트
```

## ✨ 주요 개선 사항

### 1. 모듈 분리
- ✅ Core: SAP 클라이언트 로직
- ✅ Tools: MCP 도구들 (개별 파일)
- ✅ Config: 설정 관리
- ✅ Transports: 전송 계층 추상화
- ✅ Utils: 공통 유틸리티

### 2. 전송 계층 추상화
```python
# packages/server/src/sap_mcp_server/transports/stdio.py
class StdioTransport:
    async def start(self): ...

# packages/server/src/sap_mcp_server/transports/sse.py
class SSETransport:
    async def start(self): ...
```

### 3. 도구 분리
- `tools/base.py` - 기본 클래스
- `tools/auth_tool.py` - 인증
- `tools/query_tool.py` - 쿼리
- `tools/entity_tool.py` - 엔티티
- `tools/service_tool.py` - 서비스

### 4. 클라이언트 라이브러리 구현
```python
from sap_mcp_client import SAPMCPClient

async with SAPMCPClient() as client:
    await client.authenticate()
    order = await client.get_order("Z_ORDER_SRV", "OrderSet", "12345")
```

### 5. 테스트 구조
```
tests/
├── unit/
│   ├── test_sap_client.py
│   ├── test_auth.py
│   └── test_tools.py
├── integration/
│   └── test_sap_integration.py
└── conftest.py
```

## 📋 체크리스트

### 준비 단계
- [x] 코드베이스 분석 완료
- [x] 리팩토링 계획 수립
- [x] 스크립트 생성
- [ ] 백업 생성
- [ ] 새 브랜치 생성

### 실행 단계
- [ ] `./scripts/create_structure.sh` 실행
- [ ] `./scripts/migrate_code.sh` 실행
- [ ] `python scripts/update_imports.py` 실행
- [ ] Import 경로 수동 검토
- [ ] Tools 모듈 분리
- [ ] 전송 계층 구현

### 검증 단계
- [ ] 서버 패키지 설치
- [ ] 단위 테스트 작성 및 실행
- [ ] 통합 테스트 실행
- [ ] 예제 코드 실행 확인
- [ ] 문서 업데이트

### 완료 단계
- [ ] 이전 코드 제거
- [ ] 변경사항 커밋
- [ ] PR 생성 및 리뷰

## 🎯 마이그레이션 우선순위

### 높음 (필수)
1. Core 모듈 마이그레이션
2. Config 모듈 마이그레이션
3. Import 경로 수정
4. 기본 테스트 추가

### 중간 (권장)
1. Tools 모듈 분리
2. 전송 계층 구현
3. 클라이언트 라이브러리 구현
4. 예제 정리

### 낮음 (선택)
1. 문서 통합
2. CI/CD 설정
3. 고급 테스트
4. 성능 최적화

## 🔧 수동 작업 필요 항목

### 1. Tools 모듈 분리
`tools/tools_legacy.py`를 개별 파일로 분리:

```bash
# 각 Tool 클래스를 별도 파일로 분리
# tools/auth_tool.py - SAPAuthenticateTool
# tools/query_tool.py - SAPQueryTool
# tools/entity_tool.py - SAPGetEntityTool
# tools/service_tool.py - SAPListServicesTool
```

### 2. 전송 계층 구현

`packages/server/src/sap_mcp_server/transports/stdio.py`:
```python
from sap_mcp_server.tools import register_all_tools

class StdioTransport:
    async def start(self):
        # stdio 서버 구현
        pass
```

### 3. 클라이언트 라이브러리

`packages/client/src/sap_mcp_client/client.py`:
```python
class SAPMCPClient:
    async def authenticate(self) -> bool: ...
    async def get_order(self, ...) -> Dict: ...
    async def query_orders(self, ...) -> List: ...
```

### 4. pyproject.toml 업데이트

```toml
[project]
name = "sap-mcp-server"
version = "0.2.0"

[project.scripts]
sap-mcp-server-stdio = "sap_mcp_server.transports.stdio:main"
sap-mcp-server-sse = "sap_mcp_server.transports.sse:main"
```

## 📊 예상 소요 시간

| 단계 | 소요 시간 |
|-----|----------|
| 자동 마이그레이션 (스크립트) | 30분 |
| Import 경로 수동 검토 | 1시간 |
| Tools 모듈 분리 | 2시간 |
| 전송 계층 구현 | 2시간 |
| 클라이언트 구현 | 2시간 |
| 테스트 작성 | 2시간 |
| 검증 및 문서화 | 1시간 |
| **총계** | **약 10-11시간** |

## 🆘 문제 해결

### Import 오류
```bash
# Python 경로 확인
python -c "import sys; print('\n'.join(sys.path))"

# 패키지 재설치
cd packages/server
pip uninstall sap-mcp-server -y
pip install -e ".[dev]"
```

### 테스트 실패
```bash
# 상세 로그
pytest -vv --log-cli-level=DEBUG

# 특정 테스트만
pytest tests/unit/test_sap_client.py -k test_name
```

### 서버 시작 실패
```bash
# 환경 변수 확인
cd packages/server
cat .env.server

# 직접 실행
python -m sap_mcp_server.transports.stdio
```

## 📚 추가 리소스

- [REFACTORING_GUIDE.md](./REFACTORING_GUIDE.md) - 상세 가이드
- [scripts/create_structure.sh](./scripts/create_structure.sh) - 구조 생성 스크립트
- [scripts/migrate_code.sh](./scripts/migrate_code.sh) - 코드 마이그레이션 스크립트
- [scripts/update_imports.py](./scripts/update_imports.py) - Import 수정 스크립트

## ✅ 다음 단계

1. **지금 시작하기**:
   ```bash
   ./scripts/create_structure.sh
   ./scripts/migrate_code.sh
   python scripts/update_imports.py
   ```

2. **검증하기**:
   ```bash
   cd packages/server
   pip install -e ".[dev]"
   pytest tests/ -v
   ```

3. **문서 확인**:
   - [REFACTORING_GUIDE.md](./REFACTORING_GUIDE.md) 참조

---

**작성일**: 2025-01-15
**버전**: 1.0
