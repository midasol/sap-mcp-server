# SAP MCP 리팩토링 완료 보고서

## 📋 개요

SAP Gateway Service 하드코딩을 제거하고 YAML 설정 파일 기반으로 전환하는 리팩토링을 완료했습니다.

### 변경 사항 요약
- **Python 코드에서 하드코딩 제거**: `auth.py`의 `Z_SALES_ORDER_GENAI_SRV/zsd004Set` 하드코딩 제거
- **설정 파일 기반 인증**: `services.yaml`에서 인증 엔드포인트 설정 관리
- **유연성 향상**: 여러 SAP Gateway Service를 services.yaml에서 정의하고 사용 가능
- **하위 호환성**: 기존 설정도 그대로 작동

---

## 🔧 변경된 파일

### 1. `schemas.py` - 새 설정 모델 추가
**위치**: `packages/server/src/sap_mcp_server/config/schemas.py`

**추가된 모델**:
```python
class AuthEndpointConfig(BaseModel):
    """SAP 인증 엔드포인트 설정"""
    service_id: Optional[str]          # 인증에 사용할 서비스 ID
    entity_name: Optional[str]         # CSRF 토큰 요청용 엔티티 이름
    use_catalog_metadata: bool = True  # 카탈로그 메타데이터 사용 여부
```

**업데이트된 모델**:
- `GatewayConfig`에 `auth_endpoint: AuthEndpointConfig` 필드 추가

**주요 기능**:
- `build_csrf_path()`: CSRF 토큰 요청 경로 동적 생성
- `build_auth_validation_path()`: 인증 검증 경로 생성

---

### 2. `auth.py` - 하드코딩 제거 및 설정 기반 인증
**위치**: `packages/server/src/sap_mcp_server/core/auth.py`

**변경 전**:
```python
# 하드코딩된 URL
url = f"{self.base_url}/sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV/zsd004Set"
```

**변경 후**:
```python
# 설정 기반 URL
csrf_path = self._get_csrf_endpoint_path()
url = f"{self.base_url}{csrf_path}"
```

**추가된 메서드**:
- `_get_csrf_endpoint_path()`: 설정에서 CSRF 엔드포인트 경로 가져오기
- `_get_auth_validation_path()`: 설정에서 인증 검증 경로 가져오기

**생성자 변경**:
```python
def __init__(
    self,
    config: SAPConnectionConfig,
    auth_endpoint: Optional["AuthEndpointConfig"] = None,  # 🆕 추가
    services_config: Optional["ServicesYAMLConfig"] = None,  # 🆕 추가
):
```

---

### 3. `sap_client.py` - auth_endpoint 전달
**위치**: `packages/server/src/sap_mcp_server/core/sap_client.py`

**변경 사항**:
```python
# Authenticator 초기화 시 auth_endpoint와 services_config 전달
self.authenticator = SAPAuthenticator(
    config=config,
    auth_endpoint=self.gateway_config.auth_endpoint,  # 🆕 추가
    services_config=self.services_config,              # 🆕 추가
)
```

---

### 4. `services.yaml` - 인증 엔드포인트 설정 추가
**위치**: `packages/server/config/services.yaml`

**추가된 설정**:
```yaml
gateway:
  # ... 기존 설정 ...

  # 🆕 인증 엔드포인트 설정
  auth_endpoint:
    # 카탈로그 메타데이터 사용 (권장 - 특정 서비스 필요 없음)
    use_catalog_metadata: true

    # 옵션: 특정 서비스로 인증 (필요시 주석 해제)
    # service_id: Z_SALES_ORDER_GENAI_SRV
    # entity_name: zsd004Set
```

---

### 5. `services.yaml.example` - 상세 예제 및 주석 추가
**위치**: `packages/server/config/services.yaml.example`

**추가된 내용**:
- 인증 엔드포인트 설정 옵션 2가지 설명
- 각 옵션의 장단점 및 사용 시나리오 주석
- 여러 서비스 예제 유지 (6개 서비스)

---

### 6. `loader.py` - 기본값 업데이트
**위치**: `packages/server/src/sap_mcp_server/config/loader.py`

**변경 사항**:
```python
# 기본 설정에 AuthEndpointConfig 추가
gateway=GatewayConfig(
    # ... 기존 설정 ...
    auth_endpoint=AuthEndpointConfig(
        use_catalog_metadata=True,  # 🆕 기본값: 카탈로그 사용
        service_id=None,
        entity_name=None,
    ),
)
```

---

## ✅ 달성된 목표

### 1. 하드코딩 제거 ✅
- ✅ `auth.py`에서 `Z_SALES_ORDER_GENAI_SRV` 하드코딩 제거
- ✅ `zsd004Set` 엔티티 이름 하드코딩 제거
- ✅ 모든 인증 관련 경로를 설정 파일에서 관리

### 2. 설정 파일 기반 관리 ✅
- ✅ `services.yaml`에서 인증 엔드포인트 설정
- ✅ 여러 SAP Gateway Service 정의 가능
- ✅ 각 서비스별 독립적인 설정 관리

### 3. 유연성 향상 ✅
- ✅ 카탈로그 메타데이터 사용 (기본값, 권장)
- ✅ 특정 서비스 기반 인증 (옵션)
- ✅ 동적 엔드포인트 경로 생성

### 4. 하위 호환성 유지 ✅
- ✅ 기존 설정 파일도 작동 (기본값으로 카탈로그 사용)
- ✅ 환경 변수 (.env) 기반 연결 정보 유지
- ✅ 기존 도구 (tools) 동작 변경 없음

---

## 🔍 인증 방식 비교

### Option 1: 카탈로그 메타데이터 (권장) ⭐
```yaml
auth_endpoint:
  use_catalog_metadata: true
```

**장점**:
- ✅ 특정 서비스에 의존하지 않음
- ✅ 모든 SAP 시스템에서 작동
- ✅ 유연성 최대
- ✅ 서비스 배포 상태와 무관

**단점**:
- ⚠️ 카탈로그 서비스가 없는 경우 사용 불가 (드물음)

**사용 시나리오**:
- 대부분의 경우 (기본값)
- 여러 서비스를 사용하는 환경
- 서비스 독립적인 인증 필요

---

### Option 2: 특정 서비스 기반 인증
```yaml
auth_endpoint:
  use_catalog_metadata: false
  service_id: Z_SALES_ORDER_GENAI_SRV
  entity_name: zsd004Set
```

**장점**:
- ✅ 특정 서비스에 대한 명시적 인증
- ✅ 서비스별 커스텀 인증 로직 가능

**단점**:
- ❌ 해당 서비스가 배포되어 있어야 함
- ❌ 서비스 변경 시 설정 업데이트 필요
- ❌ 유연성 낮음

**사용 시나리오**:
- 카탈로그 서비스를 사용할 수 없는 경우
- 특정 서비스에 대한 인증이 필요한 경우
- 레거시 시스템 호환성

---

## 📊 아키텍처 변경 사항

### 이전 아키텍처
```
auth.py
  └─> 하드코딩: "/sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV/zsd004Set"
```

### 새 아키텍처
```
services.yaml
  └─> gateway.auth_endpoint (설정)
        └─> AuthEndpointConfig (Pydantic 모델)
              └─> build_csrf_path() (동적 경로 생성)
                    └─> auth.py (설정 기반 인증)
```

---

## 🚀 사용 방법

### 기본 사용 (권장)
**services.yaml**:
```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: true  # 이것만 설정하면 됨!
```

**결과**:
- CSRF 토큰: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection`
- 인증 검증: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

### 특정 서비스 사용 (필요시)
**services.yaml**:
```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: false
    service_id: Z_SALES_ORDER_GENAI_SRV
    entity_name: zsd004Set

services:
  - id: Z_SALES_ORDER_GENAI_SRV  # 위에서 참조한 서비스 정의 필요
    path: "/SAP/Z_SALES_ORDER_GENAI_SRV"
    entities:
      - name: zsd004Set
        key_field: Vbeln
```

**결과**:
- CSRF 토큰: `/SAP/Z_SALES_ORDER_GENAI_SRV/zsd004Set`
- 인증 검증: `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata`

---

## 🧪 테스트 방법

### 1. 기존 설정 테스트 (하위 호환성)
```bash
# 기존 services.yaml 파일 그대로 사용
sap-mcp-server-stdio
```
**예상 결과**: 정상 작동 (카탈로그 메타데이터로 자동 인증)

### 2. 새 설정 테스트
```bash
# services.yaml에 auth_endpoint 추가 후
sap-mcp-server-stdio
```
**예상 결과**:
- 로그에 "Getting CSRF token from: /sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection" 출력
- 정상 인증 및 서비스 호출

### 3. 여러 서비스 테스트
```bash
# services.yaml에 여러 서비스 추가 후
# 각 서비스별로 sap_get_entity, sap_query 도구 사용
```

---

## 📝 마이그레이션 가이드

### 기존 사용자 (변경 불필요)
기존 `services.yaml` 파일을 그대로 사용하면 자동으로 카탈로그 메타데이터를 사용합니다.

### 새 사용자 (권장 설정)
**services.yaml** 파일에 다음 설정 추가:
```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: true
```

### 고급 사용자 (특정 서비스 인증)
**services.yaml** 파일:
```yaml
gateway:
  auth_endpoint:
    use_catalog_metadata: false
    service_id: YOUR_SERVICE_ID
    entity_name: YOUR_ENTITY_NAME
```

---

## 🎯 향후 개선 사항

### 완료된 항목 ✅
- [x] Python 코드에서 하드코딩 제거
- [x] 설정 파일 기반 인증 엔드포인트 관리
- [x] 여러 SAP Gateway Service 지원
- [x] 하위 호환성 유지
- [x] 상세 문서 및 예제 작성

### 향후 개선 (선택 사항) 📋
- [ ] 환경 변수로 인증 엔드포인트 오버라이드 (예: `SAP_AUTH_SERVICE_ID`)
- [ ] 서비스별 커스텀 인증 엔드포인트 설정 (서비스 레벨 `auth_endpoint`)
- [ ] 다중 SAP 시스템 연결 (여러 호스트/포트)
- [ ] 인증 방식 확장 (OAuth, SAML 등)

---

## 📚 참고 자료

### 주요 파일
- **설정 스키마**: `packages/server/src/sap_mcp_server/config/schemas.py`
- **인증 로직**: `packages/server/src/sap_mcp_server/core/auth.py`
- **SAP 클라이언트**: `packages/server/src/sap_mcp_server/core/sap_client.py`
- **설정 예제**: `packages/server/config/services.yaml.example`

### 설정 파일
- **실제 설정**: `packages/server/config/services.yaml`
- **환경 변수**: `.env.server` (SAP 연결 정보)

---

## ✨ 요약

이번 리팩토링을 통해:
1. **Python 코드 품질 향상**: 하드코딩 제거, 설정 기반 관리
2. **유연성 증대**: 여러 SAP Gateway Service 지원
3. **유지보수성 개선**: 설정 파일에서 중앙 관리
4. **하위 호환성**: 기존 설정도 그대로 작동

이제 SAP MCP 서버는 **설정 파일 기반**으로 여러 SAP Gateway Service를 유연하게 관리할 수 있습니다! 🎉
