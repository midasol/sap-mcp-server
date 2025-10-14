# SAP MCP Server Configuration Guide

## Overview

SAP MCP Server uses YAML-based configuration to define SAP Gateway services and entities. This makes the server completely generic and adaptable to any SAP OData service without code changes.

## Configuration Architecture

```
┌─────────────────────────────────────┐
│ config/services.yaml                │
│  ├─ Gateway URL Patterns            │
│  └─ Service Definitions             │
│      ├─ Service Metadata            │
│      └─ Entity Definitions          │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ SAPClient (Runtime)                 │
│  ├─ Builds URLs from patterns       │
│  ├─ Validates service requests      │
│  └─ Executes OData operations       │
└─────────────────────────────────────┘
```

## Configuration Files

### 1. services.yaml

**Location**: `config/services.yaml`

**Purpose**: Defines all SAP OData services and entities available through the MCP server

**Structure**:

```yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
  metadata_suffix: "/$metadata"
  service_catalog_path: "/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection"

services:
  - id: SERVICE_ID
    name: "Human Readable Name"
    path: "/SAP/SERVICE_PATH"
    version: v2
    description: "Service description"
    entities:
      - name: EntitySetName
        key_field: KeyFieldName
        description: "Entity description"
        navigations:
          - NavigationProperty1
          - NavigationProperty2
        default_select:
          - Field1
          - Field2
    custom_headers:
      header-name: "header-value"
```

### 2. Environment Variables

**File**: `.env`

**Service Configuration**:
```bash
# Optional: Path to custom services.yaml
MCP_SERVICES_CONFIG_PATH=/path/to/custom/services.yaml
```

**SAP Connection** (required):
```bash
SAP_HOST=your-sap-host.com
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=your-username
SAP_PASSWORD=your-password
SAP_VERIFY_SSL=false
SAP_TIMEOUT=30
SAP_RETRY_ATTEMPTS=3
```

## Configuration Schema

### Gateway Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base_url_pattern` | string | Yes | URL pattern with `{host}` and `{port}` placeholders |
| `metadata_suffix` | string | No | Metadata endpoint suffix (default: `/$metadata`) |
| `service_catalog_path` | string | No | Service catalog path for listing services |

**Example**:
```yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
  metadata_suffix: "/$metadata"
  service_catalog_path: "/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection"
```

### Service Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique service identifier (used in MCP tool calls) |
| `name` | string | Yes | Human-readable service name |
| `path` | string | Yes | Service path (e.g., `/SAP/Z_ORDER_SRV`) |
| `version` | string | No | OData version: `v2` or `v4` (default: `v2`) |
| `description` | string | No | Service description for documentation |
| `entities` | list | No | List of entity set definitions |
| `custom_headers` | dict | No | Custom HTTP headers for this service |

### Entity Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Entity set name (e.g., `CustomerSet`) |
| `key_field` | string | Yes | Primary key field name |
| `description` | string | No | Entity description |
| `navigations` | list | No | Navigation property names |
| `default_select` | list | No | Default fields to select in queries |

## Configuration Examples

### Example 1: Basic Service

```yaml
services:
  - id: Z_CUSTOMER_SRV
    name: "Customer Service"
    path: "/SAP/Z_CUSTOMER_SRV"
    version: v2
    entities:
      - name: CustomerSet
        key_field: Kunnr
        description: "Customer master data"
        default_select:
          - Kunnr
          - Name1
          - Land1
```

### Example 2: Service with Multiple Entities

```yaml
services:
  - id: Z_SALES_SRV
    name: "Sales Service"
    path: "/SAP/Z_SALES_SRV"
    version: v2
    entities:
      - name: OrderSet
        key_field: Vbeln
        description: "Sales orders"
        navigations:
          - ToItems
          - ToPartner
        default_select:
          - Vbeln
          - Erdat
          - Netwr
      - name: OrderItemSet
        key_field: Posnr
        description: "Order items"
        default_select:
          - Vbeln
          - Posnr
          - Matnr
```

### Example 3: OData v4 Service

```yaml
services:
  - id: Z_FINANCE_SRV
    name: "Finance Service"
    path: "/SAP/Z_FINANCE_SRV"
    version: v4
    description: "Financial accounting (OData v4)"
    entities:
      - name: GLAccountSet
        key_field: Hkont
        default_select:
          - Hkont
          - Txt20
          - Waers
    custom_headers:
      Prefer: "odata.maxpagesize=500"
```

### Example 4: Custom Gateway URL Pattern

For SAP systems with non-standard URL patterns:

```yaml
gateway:
  # Custom pattern for SAP BTP Cloud Foundry
  base_url_pattern: "https://{host}/sap/opu/odata"
  # No port in the URL

services:
  - id: MY_SERVICE
    name: "My Service"
    path: "/custom/path/MY_SERVICE"
    version: v2
```

## How to Add a New Service

### Step 1: Discover Service Metadata

1. Find service name in SAP:
   - Transaction: `/IWFND/MAINT_SERVICE`
   - Or browse: `https://your-sap-host/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection`

2. View service metadata:
   ```
   https://your-sap-host/sap/opu/odata/SAP/YOUR_SERVICE/$metadata
   ```

### Step 2: Extract Service Information

From the metadata XML:

- **Service path**: Look at the URL before `/$metadata`
- **Entity sets**: Find `<EntitySet>` elements
- **Key fields**: Find `<Key>` elements in `<EntityType>`
- **Navigations**: Find `<NavigationProperty>` elements

### Step 3: Add to services.yaml

```yaml
services:
  - id: YOUR_SERVICE_ID
    name: "Your Service Name"
    path: "/SAP/YOUR_SERVICE"
    version: v2
    description: "Service description"
    entities:
      - name: YourEntitySet
        key_field: YourKeyField
        description: "Entity description"
        default_select:
          - Field1
          - Field2
```

### Step 4: Test Configuration

1. Reload server or restart
2. Use `sap_list_services` tool to verify configuration
3. Test entity retrieval with `sap_get_entity`

## Configuration Validation

The server validates configuration at startup:

### Automatic Validation

- ✅ YAML syntax
- ✅ Required fields present
- ✅ OData version (`v2` or `v4`)
- ✅ Service path format (must start with `/`)
- ✅ Gateway URL pattern (must contain `{host}` and `{port}`)

### Runtime Validation

- ✅ Service exists when calling tools
- ✅ Entity exists in service
- ✅ Helpful error messages with available options

**Example error**:
```json
{
  "success": false,
  "error": "Service 'Z_UNKNOWN_SRV' not found in configuration. Available services: Z_SALES_SRV, Z_CUSTOMER_SRV, Z_MATERIAL_SRV"
}
```

## Configuration Best Practices

### 1. Use Descriptive IDs and Names

```yaml
# Good
id: Z_SALES_ORDER_SRV
name: "Sales Order Management Service"

# Avoid
id: SERVICE1
name: "Service"
```

### 2. Document with Descriptions

```yaml
services:
  - id: Z_CUSTOMER_SRV
    name: "Customer Master Data Service"
    description: "Provides access to customer master records and related data"
    entities:
      - name: CustomerSet
        key_field: Kunnr
        description: "Customer master records with basic information"
```

### 3. Specify Default Select Fields

Improves performance by reducing payload size:

```yaml
entities:
  - name: OrderSet
    key_field: Vbeln
    default_select:
      - Vbeln      # Order number
      - Erdat      # Creation date
      - Netwr      # Net value
      - Waerk      # Currency
```

### 4. Group Related Services

Organize services.yaml by business domain:

```yaml
services:
  # Sales Domain
  - id: Z_SALES_ORDER_SRV
    # ...
  - id: Z_SALES_ANALYTICS_SRV
    # ...

  # Finance Domain
  - id: Z_FINANCE_SRV
    # ...
  - id: Z_ACCOUNTING_SRV
    # ...
```

### 5. Version Control Configuration

- Store `services.yaml` in version control
- Use `services.yaml.example` for documentation
- Document any environment-specific configurations

## Troubleshooting

### Issue: Services not loading

**Symptom**: `sap_list_services` returns empty or default services

**Solutions**:
1. Check `MCP_SERVICES_CONFIG_PATH` environment variable
2. Verify `services.yaml` exists in `config/` directory
3. Check server logs for YAML parsing errors
4. Validate YAML syntax with online validator

### Issue: Service not found error

**Symptom**: `Service 'X' not found in configuration`

**Solutions**:
1. Run `sap_list_services` to see available services
2. Check service ID matches exactly (case-sensitive)
3. Verify service is defined in `services.yaml`
4. Restart server after configuration changes

### Issue: Entity not found error

**Symptom**: `Entity set 'X' not found in service 'Y'`

**Solutions**:
1. Check entity name matches SAP metadata exactly
2. Verify entity is listed in service's `entities` section
3. Check SAP metadata: `{service_url}/$metadata`

### Issue: Invalid URL pattern

**Symptom**: `base_url_pattern must contain {host} and {port} placeholders`

**Solutions**:
1. Ensure gateway configuration has `{host}` and `{port}`
2. Use exact placeholder names
3. Check for typos in configuration

## Advanced Configuration

### Multi-Tenant Setup

For serving multiple SAP systems:

```yaml
# system1.yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
services:
  # System 1 services

# system2.yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
services:
  # System 2 services
```

Set different config paths:
```bash
# System 1
MCP_SERVICES_CONFIG_PATH=config/system1.yaml

# System 2
MCP_SERVICES_CONFIG_PATH=config/system2.yaml
```

### Development vs Production

**development.yaml**:
```yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
services:
  - id: Z_TEST_SRV
    path: "/SAP/Z_TEST_SRV"
    # Test services only
```

**production.yaml**:
```yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"
services:
  - id: Z_PROD_ORDER_SRV
    path: "/SAP/Z_PROD_ORDER_SRV"
    # Production services only
```

## Migration Guide

### From Hardcoded Services

**Before** (code):
```python
# Hardcoded in code
service_path = f"/SAP/Z_SALES_ORDER_GENAI_SRV"
```

**After** (YAML):
```yaml
# config/services.yaml
services:
  - id: Z_SALES_ORDER_GENAI_SRV
    name: "Sales Order Service"
    path: "/SAP/Z_SALES_ORDER_GENAI_SRV"
```

**Tool usage** (unchanged):
```python
await session.call_tool(
    "sap_get_entity",
    {
        "service": "Z_SALES_ORDER_GENAI_SRV",
        "entity_set": "zsd004Set",
        "entity_key": "91000092"
    }
)
```

### Existing Deployments

1. Create `config/services.yaml` from current hardcoded services
2. Set `MCP_SERVICES_CONFIG_PATH` if using custom location
3. Test with `sap_list_services` tool
4. Deploy with new configuration
5. No client code changes required

## References

- SAP OData Documentation: https://help.sap.com/odata
- SAP Gateway Documentation: https://help.sap.com/gateway
- YAML Specification: https://yaml.org/spec/
- Pydantic Validation: https://docs.pydantic.dev/
