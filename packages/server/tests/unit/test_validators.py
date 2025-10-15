"""Unit tests for validation utilities"""

import pytest

from sap_mcp_server.utils.validators import (
    sanitize_input,
    validate_entity_key,
    validate_field_name,
    validate_odata_filter,
    validate_pagination_params,
    validate_port,
    validate_select_fields,
    validate_service_path,
    validate_url,
)


@pytest.mark.unit
class TestODataValidators:
    """Tests for OData-specific validators"""

    def test_validate_odata_filter_valid(self):
        """Test valid OData filter expressions"""
        assert validate_odata_filter("OrderID eq '12345'")
        assert validate_odata_filter("Price gt 100")
        assert validate_odata_filter("Status ne 'COMPLETED' and Date lt '2024-01-01'")

    def test_validate_odata_filter_invalid(self):
        """Test invalid OData filter expressions"""
        assert not validate_odata_filter("OrderID = 12345")  # Wrong operator
        assert not validate_odata_filter("just some text")

    def test_validate_field_name_valid(self):
        """Test valid field names"""
        assert validate_field_name("OrderID")
        assert validate_field_name("Customer_Name")
        assert validate_field_name("_privateField")

    def test_validate_field_name_invalid(self):
        """Test invalid field names"""
        assert not validate_field_name("Order-ID")  # Hyphen not allowed
        assert not validate_field_name("123Field")  # Can't start with number
        assert not validate_field_name("")  # Empty
        assert not validate_field_name("Field Name")  # Space not allowed

    def test_validate_select_fields_valid(self):
        """Test valid $select parameter"""
        fields = validate_select_fields("OrderID,CustomerName,OrderDate")
        assert fields == ["OrderID", "CustomerName", "OrderDate"]

    def test_validate_select_fields_with_spaces(self):
        """Test $select with spaces"""
        fields = validate_select_fields("OrderID, CustomerName, OrderDate")
        assert fields == ["OrderID", "CustomerName", "OrderDate"]

    def test_validate_select_fields_invalid(self):
        """Test invalid $select parameter"""
        with pytest.raises(ValueError, match="Invalid field name"):
            validate_select_fields("OrderID,Invalid-Field")

    def test_validate_pagination_params_valid(self):
        """Test valid pagination parameters"""
        params = validate_pagination_params(top=10, skip=5)
        assert params == {"top": 10, "skip": 5}

    def test_validate_pagination_params_top_only(self):
        """Test pagination with only $top"""
        params = validate_pagination_params(top=20)
        assert params == {"top": 20}

    def test_validate_pagination_params_invalid_top(self):
        """Test invalid $top parameter"""
        with pytest.raises(ValueError, match="must be a positive integer"):
            validate_pagination_params(top=-1)

        with pytest.raises(ValueError, match="cannot exceed"):
            validate_pagination_params(top=20000)

    def test_validate_pagination_params_invalid_skip(self):
        """Test invalid $skip parameter"""
        with pytest.raises(ValueError, match="must be a non-negative integer"):
            validate_pagination_params(skip=-1)


@pytest.mark.unit
class TestSAPValidators:
    """Tests for SAP-specific validators"""

    def test_validate_entity_key_valid(self):
        """Test valid entity keys"""
        assert validate_entity_key("12345")
        assert validate_entity_key("ORD-2024-001")
        assert validate_entity_key("customer.001")

    def test_validate_entity_key_invalid(self):
        """Test invalid entity keys"""
        assert not validate_entity_key("")
        assert not validate_entity_key("key with spaces")
        assert not validate_entity_key("key@special")

    def test_validate_service_path_valid(self):
        """Test valid service paths"""
        assert validate_service_path("/sap/opu/odata/sap/Z_ORDER_SRV")
        assert validate_service_path("/custom/api/v1/orders")

    def test_validate_service_path_invalid(self):
        """Test invalid service paths"""
        assert not validate_service_path("no-leading-slash")
        assert not validate_service_path("")
        assert not validate_service_path("/path with spaces")


@pytest.mark.unit
class TestNetworkValidators:
    """Tests for network-related validators"""

    def test_validate_url_valid(self):
        """Test valid URLs"""
        assert validate_url("https://sap.example.com")
        assert validate_url("http://localhost:8000")
        assert validate_url("https://sap.example.com:44300/path")

    def test_validate_url_https_required(self):
        """Test HTTPS requirement"""
        assert validate_url("https://sap.example.com", require_https=True)
        assert not validate_url("http://sap.example.com", require_https=True)

    def test_validate_url_invalid(self):
        """Test invalid URLs"""
        assert not validate_url("not a url")
        assert not validate_url("")
        assert not validate_url("ftp://sap.example.com")  # Wrong protocol

    def test_validate_port_valid(self):
        """Test valid ports"""
        assert validate_port(80)
        assert validate_port(443)
        assert validate_port(44300)

    def test_validate_port_invalid(self):
        """Test invalid ports"""
        assert not validate_port(0)
        assert not validate_port(70000)
        assert not validate_port(-1)


@pytest.mark.unit
class TestInputSanitization:
    """Tests for input sanitization"""

    def test_sanitize_input_valid(self):
        """Test sanitizing valid input"""
        assert sanitize_input("OrderID") == "OrderID"
        assert sanitize_input("Customer Name") == "Customer Name"

    def test_sanitize_input_too_long(self):
        """Test input exceeding max length"""
        with pytest.raises(ValueError, match="exceeds maximum length"):
            sanitize_input("A" * 2000)

    def test_sanitize_input_dangerous_content(self):
        """Test input with potentially dangerous content"""
        with pytest.raises(ValueError, match="dangerous content"):
            sanitize_input("<script>alert('xss')</script>")

        with pytest.raises(ValueError, match="dangerous content"):
            sanitize_input("javascript:alert('xss')")

        with pytest.raises(ValueError, match="dangerous content"):
            sanitize_input("'; DROP TABLE users; --")

    def test_sanitize_input_not_string(self):
        """Test non-string input"""
        with pytest.raises(ValueError, match="must be a string"):
            sanitize_input(12345)  # type: ignore
