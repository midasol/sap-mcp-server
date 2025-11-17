# SAP MCP Demo Guide: Interacting with the SFLIGHT OData Service

This guide provides a step-by-step walkthrough on how to use the SAP MCP (Model Context Protocol) server to interact with an OData service based on the standard SAP SFLIGHT demo dataset. It will show you how to configure the server and use its tools to query flight data.

## 🎯 Scenario Overview

The SFLIGHT dataset is a sample database provided by SAP that includes data for flight schedules, airlines, airports, and bookings. It's an excellent resource for testing and demonstrating data modeling and service creation.

This guide assumes you have an OData service exposing this dataset. The goal is to connect our SAP MCP server to this service and interact with it using AI agents or other clients.

**Official SAP Documentation:**
*   [SAP Documentation - Flight Model](https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/3c/a4923c05b32954e10000000a114084/frameset.htm)
*   [SAP Help Portal - Flight Model](https://help.sap.com/viewer/BI_AN_ALL/AN_ALL/en-US/3ca4923c05b32954e10000000a114084.html)

---

## ✅ Prerequisites

1.  **SAP MCP Server Installed**: You must have the SAP MCP server installed and a working Python environment. For full instructions, please see the [**Quick Start section in the main README.md**](../../../README.md#🚀-quick-start).

2.  **SFLIGHT OData Service**: An active OData service exposing the SFLIGHT dataset must be available on your SAP Gateway system.
    *   If you need to create this service, you can follow our detailed guide: [**OData Service Creation Guide: FLIGHT Demo Scenario**](./odata-service-creation-flight-demo.md).
    *   For this guide, we will assume the service is named `Z_FLIGHT_DEMO_SRV`.

---

## ⚙️ Step 1: Configure the SFLIGHT Service

First, we need to make the SAP MCP server aware of our new SFLIGHT OData service. We do this by adding its definition to the `services.yaml` file.

**1. Open the configuration file**:
Navigate to and open `packages/server/config/services.yaml`.

**2. Add the service definition**:
Append the following YAML block to the `services` list. This configuration defines the service ID, its entities, and key fields based on the SFLIGHT model.

```yaml
# packages/server/config/services.yaml

# ... (other services may be listed here)

  # SFLIGHT Demo Service
  - id: Z_FLIGHT_DEMO_SRV
    name: "SFLIGHT Demo Service"
    path: "/SAP/Z_FLIGHT_DEMO_SRV"  # IMPORTANT: Replace with your actual service path
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
      - name: ConnectionSet
        # Composite Key
        key_field: "CARRID='{CARRID}',CONNID='{CONNID}'"
        description: "Flight connections between two airports"
      - name: FlightSet
        # Composite Key
        key_field: "CARRID='{CARRID}',CONNID='{CONNID}',FLDATE=datetime'{FLDATE}'"
        description: "Specific flights on a given date"
      - name: BookingSet
        # Composite Key
        key_field: "CARRID='{CARRID}',CONNID='{CONNID}',FLDATE=datetime'{FLDATE}',BOOKID='{BOOKID}'"
        description: "Individual flight bookings"
      - name: PassengerSet
        key_field: ID
        description: "Passengers (Customers)"
```

**3. Save the file.** The server will now recognize `Z_FLIGHT_DEMO_SRV` and its associated entities.

---

## 🛠️ Step 2: Interact with the SFLIGHT Service Using MCP Tools

With the configuration in place, you can now use the SAP MCP tools to query the SFLIGHT data. Below are examples of `ToolCallRequest` JSON payloads you could send to the server.

### 1. List All Available Services

First, let's verify that our new service is registered correctly.

**Request**:
```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

**Expected Response**:
The output should now include the `Z_FLIGHT_DEMO_SRV`.
```json
{
  "services": [
    {
      "name": "Z_FLIGHT_DEMO_SRV",
      "description": "OData service for the SFLIGHT demo dataset.",
      "entity_sets": ["AirlineSet", "AirportSet", "ConnectionSet", "FlightSet", "BookingSet", "PassengerSet"]
    }
    // ... other services
  ],
  "count": 1
}
```

### 2. Query Airlines (`sap_query`)

Let's retrieve a list of all airlines.

**Request**:
```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_FLIGHT_DEMO_SRV",
    "entity_set": "AirlineSet"
  }
}
```

### 3. Get a Specific Airport (`sap_get_entity`)

Now, let's fetch the details for a single airport, for example, Frankfurt Airport (`FRA`).

**Request**:
```json
{
  "name": "sap_get_entity",
  "arguments": {
    "service": "Z_FLIGHT_DEMO_SRV",
    "entity_set": "AirportSet",
    "entity_key": "'FRA'"
  }
}
```
> **Note**: For string keys in OData, the value must be enclosed in single quotes.

### 4. Query Flights with a Filter (`sap_query`)

Let's find all Lufthansa (`LH`) flights.

**Request**:
```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_FLIGHT_DEMO_SRV",
    "entity_set": "FlightSet",
    "filter": "CARRID eq 'LH'",
    "select": "CARRID,CONNID,FLDATE,PRICE",
    "top": 5
  }
}
```

---

## 🤖 Step 3: Example Prompts for Gemini CLI

If you have integrated the SAP MCP server with the Gemini CLI, you can now use natural language to query the SFLIGHT data.

1.  **Start Gemini CLI**:
    ```bash
    gemini
    ```

2.  **Use natural language prompts**:

    *   **"Authenticate with SAP."**
        *   *Gemini will call `sap_authenticate`.*

    *   **"Using the SFLIGHT service, show me all airlines."**
        *   *Gemini will call `sap_query` on the `AirlineSet`.*

    *   **"Find details for Frankfurt airport in the SFLIGHT demo service."**
        *   *Gemini will likely use `sap_query` with a filter: `sap_query(service="Z_FLIGHT_DEMO_SRV", entity_set="AirportSet", filter="ID eq 'FRA'")`.*

    *   **"List the first 5 Lufthansa flights available in the system."**
        *   *Gemini will call `sap_query` on `FlightSet` with a filter for `CARRID eq 'LH'` and `$top=5`.*

    *   **"What SAP services are available?"**
        *   *Gemini will call `sap_list_services` and show you the newly added SFLIGHT service.*

---

## Conclusion

You have successfully configured the SAP MCP server to connect to an SFLIGHT OData service and have tested data retrieval using the available tools. This setup provides a powerful foundation for building AI-driven applications that can interact with real-world SAP data scenarios.