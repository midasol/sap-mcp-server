# OData Service Creation Guide: FLIGHT Demo Scenario

This guide provides a step-by-step walkthrough for creating an OData service in an SAP system using the SAP Gateway Service Builder (SEGW) to expose the Flight scenario data available in SAP S/4HANA Fully Activated Appliance (FAA) version.

## Scenario Overview

**Goal**: Expose flight schedules, bookings, and related master data via an OData service.

**Scenario Data Needs**: Flight schedules, dates, times, airport details, airline details, passenger details, pricing, etc.

**SAP Tables Involved**: `SFLIGHT`, `SPFLI`, `SCARR`, `SAIRPORT`, `SBOOK`, `SCUSTOM`.

## Steps to Create the OData Service in SEGW

### 1. Access SAP Gateway Service Builder

Navigate to the SAP transaction code `SEGW`.

### 2. Create a New Project

1.  Click the "Create Project" button.
2.  **Project Name**: Assign a name (e.g., `Z_TRAVEL_RECOMMENDATIONS_SRV`).
3.  **Description**: Provide a meaningful description.
4.  **Package**: Assign to a package (e.g., `$TMP` for local development or a transportable package).

### 3. Import Data Model from DDIC Structures

This step defines your OData entities based on the underlying SAP tables.

1.  Right-click on the "Data Model" folder within your project.
2.  Select "Import" -> "DDIC Structure".
3.  Repeat the import process for each required table, specifying the Entity Type Name and selecting the necessary fields.

**Action Required**: Ensure the Key fields are correctly marked during the import process.

| DDIC Structure | Entity Type Name | Recommended Key Fields | Relevant Payload Fields (Examples) |
| :--- | :--- | :--- | :--- |
| `SFLIGHT` | Flight | `CARRID`, `CONNID`, `FLDATE` | `PRICE`, `CURRENCY`, `PLANETYPE`, `SEATSMAX`, `SEATSOCC` |
| `SPFLI` | Connection | `CARRID`, `CONNID` | `COUNTRYFR`, `CITYFROM`, `AIRPFROM`, `COUNTRYTO`, `CITYTO`, `AIRPTO`, `DEPTIME`, `ARRTIME`, `DISTANCE` |
| `SCARR` | Airline | `CARRID` | `CARRNAME`, `CURRCODE`, `URL` |
| `SAIRPORT` | Airport | `ID` | `NAME`, `CITY`, `COUNTRY` |
| `SBOOK` | Booking | `CARRID`, `CONNID`, `FLDATE`, `BOOKID` | `CUSTOMID`, `CUSTTYPE`, `SMOKER`, `LUGGWEIGHT`, `WUNIT`, `INVOICE`, `CLASS`, `FORCURAM`, `ORDER_DATE` |
| `SCUSTOM` | Passenger | `ID` | `NAME`, `FORM`, `STREET`, `POSTCODE`, `CITY`, `COUNTRY`, `PHONE` |

### 4. Define Associations and Navigation Properties

Associations link entities based on key fields. Navigation Properties allow client applications to easily traverse these relationships (e.g., using `$expand`).

#### Logical Relationships

*   **1:N**: Airline <-> Flights, Airline <-> Connections, Connection <-> Flights, Flight <-> Bookings, Passenger <-> Bookings.
*   **N:1**: Connection <-> Origin Airport, Connection <-> Destination Airport.

#### Steps to Create an Association

1.  Right-click on "Data Model" -> "Create" -> "Association".
2.  Define the Association Name, Principal Entity (the 'one' side), Dependent Entity (the 'many' side), and Cardinality (e.g., 1:N).
3.  On the next screen, Specify Key Mapping by matching the key fields between the Principal and Dependent entities.

#### Specific Associations to Create

| No. | Association Name | Principal:Dependent | Cardinality | Key Mapping |
| :-- | :--- | :--- | :--- | :--- |
| 1 | `Assoc_Airline_Flights` | Airline : Flight | 1:N | `Airline.CARRID` <-> `Flight.CARRID` |
| 2 | `Assoc_Airline_Connections` | Airline : Connection | 1:N | `Airline.CARRID` <-> `Connection.CARRID` |
| 3 | `Assoc_Connection_Flights` | Connection : Flight | 1:N | `CARRID` & `CONNID` (both ways) |
| 4 | `Assoc_Flight_Bookings` | Flight : Booking | 1:N | `CARRID`, `CONNID`, `FLDATE` (all three ways) |
| 5 | `Assoc_Passenger_Bookings` | Passenger : Booking | 1:N | `Passenger.ID` <-> `Booking.CUSTOMID` |
| 6 | `Assoc_Connection_OriginAirport` | Connection : Airport | N:1 | `Connection.AIRPFROM` <-> `Airport.ID` |
| 7 | `Assoc_Connection_DestAirport` | Connection : Airport | N:1 | `Connection.AIRPTO` <-> `Airport.ID` |

#### Navigation Properties to Create

| Entity | Navigation Property Name | Target Entity | Used Association |
| :--- | :--- | :--- | :--- |
| Airline | `ToFlights`, `ToConnections` | Flight, Connection | `Assoc_Airline_Flights`, `Assoc_Airline_Connections` |
| Flight | `ToAirline`, `ToConnection`, `ToBookings` | Airline, Connection, Booking | `Assoc_Airline_Flights`, `Assoc_Connection_Flights`, `Assoc_Flight_Bookings` |
| Connection | `ToAirline`, `ToFlights`, `ToOriginAirport`, `ToDestinationAirport` | Airline, Flight, Airport, Airport | `Assoc_Airline_Connections`, `Assoc_Connection_Flights`, `Assoc_Connection_OriginAirport`, `Assoc_Connection_DestAirport` |
| Booking | `ToFlight`, `ToPassenger` | Flight, Passenger | `Assoc_Flight_Bookings`, `Assoc_Passenger_Bookings` |
| Passenger | `ToBookings` | Booking | `Assoc_Passenger_Bookings` |

### 5. Generate Runtime Objects

1.  Click the "Generate Runtime Objects" button (magic wand icon).
2.  This generates the ABAP classes: Model Provider Class (MPC) and Data Provider Class (DPC).
3.  Accept or adjust the default class names.

### 6. Implement Data Provider Class (DPC) Methods

The generated DPC extension class (e.g., `ZCL_Z_TRAVEL_RECOM_DPC_EXT`) is used for custom logic.

*   If direct table mapping is sufficient, the base implementation may suffice.
*   For custom filtering, joins, calculations, or complex Read/Create/Update/Delete (CRUD) operations, you must redefine methods like `*_GET_ENTITY` (single record) and `*_GET_ENTITYSET` (collection) in the DPC extension class.

Here is an example of method `AIRLINESET_GET_ENTITYSET`:

```abap
METHOD airlineset_get_entityset.
  DATA: lt_airlines TYPE TABLE OF scarr,
        ls_airline TYPE scarr,
        lv_filter_string TYPE string.

  TRY.