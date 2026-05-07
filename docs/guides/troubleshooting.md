# SAP MCP Server 문제 해결 가이드

이 문서는 SAP MCP Server 사용 중 발생할 수 있는 일반적인 문제와 해결 방법을 다룹니다.

## Query Tool Mock Response 문제

### 문제 증상

`sap_query` 툴 실행 시 다음과 같은 mock response가 반환되는 경우:

```json
{
  "message": "Query would be executed (mock response)",
  "query": "your_odata_query",
  "service": "your_service_name"
}
```

**주요 증상:**
- [`sap_authenticate`](../../packages/server/src/sap_mcp_server/tools/auth_tool.py) 툴은 정상 작동
- [`sap_query`](../../packages/server/src/sap_mcp_server/tools/query_tool.py) 툴만 mock response 반환
- 실제 SAP 데이터가 조회되지 않음
- 에러 메시지는 발생하지 않음

### 원인

이 문제는 **Python 패키지 캐싱** 때문에 발생합니다.

**기술적 배경:**
- [`query_tool.py`](../../packages/server/src/sap_mcp_server/tools/query_tool.py) 파일에는 실제 SAP Gateway 통합 코드가 구현되어 있음
- 그러나 Python이 이전에 설치된 패키지의 캐시된 버전(`.pyc` 파일)을 사용
- 캐시된 버전은 mock response만 반환하는 이전 구현

**왜 auth_tool은 작동하는가?**
- `auth_tool.py`는 처음부터 완전히 구현되어 업데이트가 없었음
- `query_tool.py`는 개발 과정에서 mock → 실제 구현으로 변경됨
- 변경 후 패키지를 재설치하지 않아 이전 캐시가 실행됨

**영향 받는 파일:**
- `__pycache__/*.pyc` - 바이트코드 캐시 파일
- `site-packages/sap_mcp_server/` - 설치된 패키지 디렉토리

### 해결 방법

#### 방법 1: 빠른 해결 (권장)

가장 빠르고 간단한 해결 방법입니다.

1. **현재 설치된 패키지 제거**
   ```bash
   pip uninstall sap-mcp-server -y
   ```

2. **캐시 제거**
   ```bash
   # 프로젝트 루트에서 실행
   find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
   find . -type f -name "*.pyc" -delete
   ```

3. **패키지 재설치 (editable 모드)**
   ```bash
   cd packages/server
   pip install -e .
   ```

4. **서버 재시작**
   ```bash
   # 기존 서버 프로세스 종료 후
   python -m sap_mcp_server.transports.stdio
   ```

> **참고:** editable 모드(`-e`)로 설치하면 코드 변경 시 자동으로 반영됩니다.

#### 방법 2: 완전 재설치

더 철저한 정리가 필요한 경우 사용합니다.

1. **패키지 완전 제거**
   ```bash
   pip uninstall sap-mcp-server -y
   pip cache purge
   ```

2. **Python 캐시 완전 제거**
   ```bash
   # 프로젝트의 모든 캐시 제거
   cd /Users/sanggyulee/my-project/python-project/sap-mcp
   find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
   find . -type f -name "*.pyc" -delete
   find . -type f -name "*.pyo" -delete
   ```

3. **site-packages에서 이전 설치 확인 및 제거**
   ```bash
   # 설치 위치 확인
   pip show sap-mcp-server
   
   # 수동 제거가 필요한 경우
   # 위 명령어의 Location 경로를 확인 후
   rm -rf {Location}/sap_mcp_server*
   ```

4. **새로 설치**
   ```bash
   cd packages/server
   pip install -e .
   ```

5. **설치 검증**
   ```bash
   # 올바른 경로가 표시되는지 확인
   python -c "import sap_mcp_server.tools.query_tool; print(sap_mcp_server.tools.query_tool.__file__)"
   ```
   
   **예상 출력:** 프로젝트 디렉토리 내 경로가 표시되어야 함
   ```
   /Users/sanggyulee/my-project/python-project/sap-mcp/packages/server/src/sap_mcp_server/tools/query_tool.py
   ```

#### 방법 3: 개발 환경 재구성

가상환경에 문제가 있는 경우 사용합니다.

1. **현재 가상환경 비활성화**
   ```bash
   deactivate  # 가상환경 사용 중인 경우
   ```

2. **기존 가상환경 삭제**
   ```bash
   # 프로젝트 루트에서
   rm -rf venv  # 또는 사용 중인 가상환경 디렉토리명
   ```

3. **새 가상환경 생성**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **필수 패키지 설치**
   ```bash
   pip install --upgrade pip
   pip install -e packages/server
   ```

5. **서버 실행**
   ```bash
   python -m sap_mcp_server.transports.stdio
   ```

### 검증 방법

문제가 해결되었는지 확인하는 방법:

1. **모듈 경로 확인**
   ```bash
   python -c "import sap_mcp_server.tools.query_tool as qt; print(qt.__file__)"
   ```
   
   ✅ **성공:** 프로젝트 소스 디렉토리 경로 표시
   ```
   /path/to/sap-mcp/packages/server/src/sap_mcp_server/tools/query_tool.py
   ```
   
   ❌ **실패:** site-packages 경로 표시
   ```
   /path/to/site-packages/sap_mcp_server/tools/query_tool.py
   ```

2. **Query Tool 코드 확인**
   ```bash
   python -c "import inspect; import sap_mcp_server.tools.query_tool as qt; print(inspect.getsource(qt.QueryTool.execute))" | grep -i "mock"
   ```
   
   ✅ **성공:** 아무 출력도 없음 (mock 코드 없음)
   
   ❌ **실패:** "mock response" 관련 코드가 출력됨

3. **실제 쿼리 테스트**
   
   서버 실행 후 실제 SAP 쿼리를 수행하여:
   
   ✅ **성공:** SAP에서 실제 데이터가 반환됨
   
   ❌ **실패:** "Query would be executed (mock response)" 메시지 반환

### 예방 방법

향후 이러한 문제를 예방하기 위한 best practices:

**개발 중:**

1. **항상 editable 모드로 설치**
   ```bash
   pip install -e packages/server
   ```
   
   이렇게 하면 코드 변경 시 재설치 없이 즉시 반영됩니다.

2. **코드 변경 후 확인 사항**
   ```bash
   # 변경한 파일이 올바른 위치인지 확인
   python -c "import sap_mcp_server.tools.query_tool; print(sap_mcp_server.tools.query_tool.__file__)"
   ```

3. **의심스러운 경우 캐시 제거**
   ```bash
   find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
   ```

**배포 시:**

1. **깨끗한 환경에서 테스트**
   ```bash
   # 새 가상환경 생성
   python3 -m venv test-env
   source test-env/bin/activate
   pip install -e packages/server
   ```

2. **패키지 빌드 전 확인**
   ```bash
   # 소스 디렉토리 정리
   python setup.py clean --all
   find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
   ```

**일반 규칙:**

> **중요:** Python 패키지 코드를 수정한 후에는 항상 다음 중 하나를 수행하세요:
> - editable 모드로 설치된 경우: Python 인터프리터/서버 재시작
> - 일반 모드로 설치된 경우: `pip install -e .`로 재설치
> - 의심스러운 경우: 캐시 제거 + 재설치

---

## 일반적인 문제들

### 인증 실패

> 🚧 **준비 중** - 이 섹션은 향후 추가될 예정입니다.

**예정 내용:**
- SAP 시스템 연결 실패
- 인증서 관련 문제
- 자격 증명 오류

### 네트워크 연결 문제

> 🚧 **준비 중** - 이 섹션은 향후 추가될 예정입니다.

**예정 내용:**
- 타임아웃 문제
- 프록시 설정
- 방화벽 이슈

### 설정 파일 오류

> 🚧 **준비 중** - 이 섹션은 향후 추가될 예정입니다.

**예정 내용:**
- services.yaml 구문 오류
- 환경 변수 설정
- 경로 문제

---

## 도움이 더 필요하신가요?

문제가 계속되거나 이 가이드에 없는 문제를 겪고 계신가요?

1. **로그 확인:** 상세한 에러 로그는 문제 진단에 도움이 됩니다
   ```bash
   # 디버그 모드로 실행
   DEBUG=1 python -m sap_mcp_server.transports.stdio
   ```

2. **이슈 제기:** GitHub Issues에 다음 정보와 함께 문제를 보고해주세요:
   - 문제 증상
   - 재현 단계
   - 에러 로그
   - 환경 정보 (OS, Python 버전 등)

3. **관련 문서:**
   - [설정 가이드](configuration.md)
   - [README](../../README.md)