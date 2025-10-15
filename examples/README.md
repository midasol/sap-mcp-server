# SAP MCP Client Examples

SAP MCP 서버와 통신하는 Stdio 기반 클라이언트 예제입니다.

## 📋 목차

- [연결 방식](#연결-방식)
- [예제 파일](#예제-파일)
- [실행 방법](#실행-방법)
- [문제 해결](#문제-해결)

## 🔌 연결 방식

### ⚡ Stdio (Standard Input/Output)

**이 프로젝트는 Stdio 방식만 지원합니다.**

Stdio 프로토콜은 클라이언트가 서버 프로세스를 자동으로 실행하고 stdin/stdout을 통해 통신하는 방식입니다.

**장점:**
- ✅ 안정적이고 간단한 구조
- 서버 프로세스 자동 관리
- Claude Desktop과 완벽 호환
- 별도의 네트워크 설정 불필요

**작동 방식:**
1. 클라이언트가 `python -m sap_mcp.stdio_server` 실행
2. stdin/stdout 파이프를 통한 JSON-RPC 통신
3. 클라이언트 종료 시 서버도 자동 종료

**사용 시나리오:**
- 로컬 개발 및 테스트
- Claude Desktop 통합
- 자동화 스크립트
- CI/CD 파이프라인

## 📁 예제 파일

### 1. `stdio_client.py` (메인 예제)

Stdio 방식으로 SAP MCP 서버와 통신하는 클라이언트

**기능:**
- SAP 인증 테스트
- 단일 엔티티 조회 (OrderID로 검색)
- 응답 파싱 및 포맷팅

**실행 방법:**

```bash
cd sap-mcp-client
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 서버 패키지 설치 (최초 1회)
pip install -e ../sap-mcp-server

python examples/stdio_client.py
```

### 2. `order_inquiry_chatbot.py`

주문 조회를 위한 대화형 챗봇

**기능:**
- 자연어로 주문 조회
- 대화 컨텍스트 유지
- 다양한 필터링 옵션

**실행 방법:**

```bash
python examples/order_inquiry_chatbot.py
```

### 3. `genai-example.py`

GenAI 통합 예제

## 🚀 실행 방법

### 사전 요구사항

**1. 서버 패키지 설치**

```bash
cd sap-mcp-server
pip install -e .
```

**2. SAP 인증 정보 설정**

⚠️ **중요**: `sap-mcp-server/.env.server` 파일에 **실제 SAP 서버 정보**를 입력해야 합니다.

기본 파일에는 플레이스홀더 값(`your-sap-server.com` 등)이 들어있으므로, 반드시 실제 값으로 변경하세요:

```env
# SAP Gateway Connection
SAP_HOST=actual-sap-server.company.com
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=actual_username
SAP_PASSWORD=actual_password

# Connection Settings
SAP_VERIFY_SSL=false
SAP_TIMEOUT=30
SAP_RETRY_ATTEMPTS=3
```

**설정 확인 (선택사항):**

```bash
cd sap-mcp-server
python test_env_loading.py
```

이 테스트는 `.env.server` 파일이 올바르게 로드되는지, 플레이스홀더 값이 남아있지 않은지 확인합니다.

### 기본 실행

```bash
cd sap-mcp-client
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python examples/stdio_client.py
```

**예상 출력:**

```
🚀 SAP MCP Client - Stdio Mode
============================================================
This client auto-spawns the server as a subprocess
============================================================

📡 Initializing MCP session...
✅ Session initialized

=== SAP Authentication ===
✅ Authentication successful

=== Get Entity (OrderID: 91000092) ===
✅ Entity retrieved successfully
{
  "OrderID": "91000092",
  "CustomerName": "...",
  ...
}

✅ Test completed
```

## ⚙️ Claude Desktop 통합

`.claude_desktop_config.json` 파일에 다음 설정 추가:

```json
{
  "mcpServers": {
    "sap-mcp": {
      "command": "python",
      "args": ["-m", "sap_mcp.stdio_server"],
      "env": {
        "SAP_HOST": "your-sap-server.com",
        "SAP_PORT": "44300",
        "SAP_CLIENT": "100",
        "SAP_USERNAME": "your_username",
        "SAP_PASSWORD": "your_password",
        "SAP_VERIFY_SSL": "false"
      }
    }
  }
}
```

**설정 파일 위치:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

## 🔧 문제 해결

### 1. `ModuleNotFoundError: No module named 'sap_mcp'`

**원인:** 서버 패키지가 설치되지 않음

**해결:**

```bash
cd sap-mcp-server
pip install -e .
```

### 2. `Authentication failed` - Validation errors

**원인:** SAP 인증 정보가 환경 변수에서 로드되지 않거나 플레이스홀더 값이 그대로 남아있음

**해결:**

1. `.env.server` 파일 위치 확인:
   ```bash
   ls -la sap-mcp-server/.env.server
   ```

2. 파일 내용 확인 및 **실제 값으로 변경 여부 확인**:
   ```bash
   cat sap-mcp-server/.env.server | grep SAP_
   ```

3. 플레이스홀더 값 확인:
   - ❌ `SAP_HOST=your-sap-server.com` (플레이스홀더 - 실제 값으로 변경 필요)
   - ✅ `SAP_HOST=actual-server.company.com` (실제 값)

4. 환경 변수 이름 확인:
   - ✅ `SAP_HOST` (올바름)
   - ❌ `SAP_BASE_URL` (잘못됨)

5. 올바른 형식 (실제 값 사용):
   ```env
   SAP_HOST=actual-sap-server.company.com
   SAP_PORT=44300
   SAP_CLIENT=100
   SAP_USERNAME=actual_username
   SAP_PASSWORD=actual_password
   ```

6. 주석이 값 뒤에 있지 않은지 확인:
   - ❌ `SAP_HOST=server.com  # 주석` (inline 주석은 파싱 오류 발생 가능)
   - ✅ `# 주석` 다음 줄에 `SAP_HOST=server.com` (별도 줄에 주석)

### 3. `Connection closed`

**원인:** 서버 프로세스 시작 실패

**해결:**

1. 서버 패키지 설치 확인:
   ```bash
   pip list | grep sap-mcp-server
   ```

2. 서버 직접 실행 테스트:
   ```bash
   python -m sap_mcp.stdio_server
   ```

3. 로그 확인하여 에러 메시지 확인

### 4. `SAP connection error`

**원인:** SAP 서버 연결 실패

**해결:**

1. SAP 서버 URL 확인
2. 네트워크 연결 확인
3. 방화벽 설정 확인
4. SSL 인증서 문제인 경우 `SAP_VERIFY_SSL=false` 설정

## 📚 추가 리소스

- [SAP MCP Server 문서](../../sap-mcp-server/README.md)
- [MCP 프로토콜 사양](https://spec.modelcontextprotocol.io/)
- [SAP Gateway 개발자 가이드](https://help.sap.com/docs/ABAP_PLATFORM/68bf513362174d54b58cddec28794093/3a8e3e2d21d84af9a92c00bd97a99433.html)

## 💡 팁

1. **환경 변수**: `.env.server` 파일을 사용하면 인증 정보를 안전하게 관리할 수 있습니다
2. **디버깅**: `MCP_LOG_LEVEL=DEBUG`로 설정하여 상세 로그 확인
3. **성능**: 대량 데이터 조회 시 `$top`과 `$skip` 파라미터 활용
4. **보안**: 프로덕션 환경에서는 `SAP_VERIFY_SSL=true` 사용 권장

## 🔐 보안 주의사항

- `.env.server` 파일은 git에 커밋하지 마세요 (.gitignore에 포함됨)
- 프로덕션 환경에서는 환경 변수나 시크릿 관리 도구 사용
- SSL 인증서 검증을 비활성화하지 마세요 (개발 환경 전용)
