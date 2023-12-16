# Vessel API Python SDK

The Vessel API Python SDK is a PyPi library for accessing the Vessel API, a Unified CRM API that provides standardized endpoints for performing operations on common CRM Objects.

<!-- Start SDK Installation [installation] -->
## SDK Installation

```bash
pip install vesselapi
```
<!-- End SDK Installation [installation] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI()

req = operations.DeleteConnectionRequestBody(
    connection_id='string',
)

res = s.connections.delete(req, operations.DeleteConnectionSecurity(
    vessel_api_token="<YOUR_API_KEY_HERE>",
))

if res.status_code == 200:
    # handle response
    pass
```
<!-- End SDK Example Usage [usage] -->

## Authentication

To authenticate the Vessel Node SDK you will need to provide a Vessel API Token, along with an Access Token for each request. For more details please see the [Vessel API Documentation](https://docs.vessel.land/authentication-and-security).

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [connections](docs/sdks/connections/README.md)

* [delete](docs/sdks/connections/README.md#delete) - Delete Connection
* [find](docs/sdks/connections/README.md#find) - Get Connection
* [list](docs/sdks/connections/README.md#list) - Get All Connections

### [integrations](docs/sdks/integrations/README.md)

* [list](docs/sdks/integrations/README.md#list) - Get CRM Integrations

### [webhooks](docs/sdks/webhooks/README.md)

* [create](docs/sdks/webhooks/README.md#create) - Create Webhook
* [delete](docs/sdks/webhooks/README.md#delete) - Remove Webhook
* [find](docs/sdks/webhooks/README.md#find) - Get Webhook

### [accounts](docs/sdks/accounts/README.md)

* [batch](docs/sdks/accounts/README.md#batch) - Get Batch Accounts
* [create](docs/sdks/accounts/README.md#create) - Create Account
* [details](docs/sdks/accounts/README.md#details) - Get Account Details
* [find](docs/sdks/accounts/README.md#find) - Get Account
* [list](docs/sdks/accounts/README.md#list) - Get All Accounts
* [search](docs/sdks/accounts/README.md#search) - Search Accounts
* [update](docs/sdks/accounts/README.md#update) - Update Account

### [calls](docs/sdks/calls/README.md)

* [batch](docs/sdks/calls/README.md#batch) - Batch Calls
* [create](docs/sdks/calls/README.md#create) - Create Call
* [details](docs/sdks/calls/README.md#details) - Get Call Details
* [find](docs/sdks/calls/README.md#find) - Get Call
* [list](docs/sdks/calls/README.md#list) - Get All Calls
* [search](docs/sdks/calls/README.md#search) - Search Calls
* [update](docs/sdks/calls/README.md#update) - Update Call

### [contacts](docs/sdks/contacts/README.md)

* [batch](docs/sdks/contacts/README.md#batch) - Get Batch Contacts
* [create](docs/sdks/contacts/README.md#create) - Create Contact
* [details](docs/sdks/contacts/README.md#details) - Get Contact Details
* [find](docs/sdks/contacts/README.md#find) - Get Contact
* [list](docs/sdks/contacts/README.md#list) - Get All Contacts
* [search](docs/sdks/contacts/README.md#search) - Search Contacts
* [update](docs/sdks/contacts/README.md#update) - Update Contact

### [deals](docs/sdks/deals/README.md)

* [batch](docs/sdks/deals/README.md#batch) - Get Batch Deals
* [create](docs/sdks/deals/README.md#create) - Create Deal
* [details](docs/sdks/deals/README.md#details) - Get Deal Details
* [find](docs/sdks/deals/README.md#find) - Get Deal
* [list](docs/sdks/deals/README.md#list) - Get All Deals
* [search](docs/sdks/deals/README.md#search) - Search Deals
* [update](docs/sdks/deals/README.md#update) - Update Deal

### [emails](docs/sdks/emails/README.md)

* [batch](docs/sdks/emails/README.md#batch) - Get Batch Emails
* [create](docs/sdks/emails/README.md#create) - Create Email
* [details](docs/sdks/emails/README.md#details) - Get Email Details
* [find](docs/sdks/emails/README.md#find) - Get Email
* [list](docs/sdks/emails/README.md#list) - Get All Emails
* [search](docs/sdks/emails/README.md#search) - Search Emails
* [update](docs/sdks/emails/README.md#update) - Update Email

### [events](docs/sdks/events/README.md)

* [batch](docs/sdks/events/README.md#batch) - Get Batch Events
* [create](docs/sdks/events/README.md#create) - Create Event
* [details](docs/sdks/events/README.md#details) - Get Event Details
* [find](docs/sdks/events/README.md#find) - Get Event
* [list](docs/sdks/events/README.md#list) - Get All Events
* [search](docs/sdks/events/README.md#search) - Search Events
* [update](docs/sdks/events/README.md#update) - Update Event

### [attendees](docs/sdks/attendees/README.md)

* [batch](docs/sdks/attendees/README.md#batch) - Get Batch Event Attendees
* [create](docs/sdks/attendees/README.md#create) - Create Event Attendee
* [details](docs/sdks/attendees/README.md#details) - Get Event Attendee Details
* [find](docs/sdks/attendees/README.md#find) - Get Event Attendee
* [list](docs/sdks/attendees/README.md#list) - Get All Event Attendees
* [search](docs/sdks/attendees/README.md#search) - Search Event Attendees
* [update](docs/sdks/attendees/README.md#update) - Update Event Attendee

### [leads](docs/sdks/leads/README.md)

* [batch](docs/sdks/leads/README.md#batch) - Get Batch Leads
* [create](docs/sdks/leads/README.md#create) - Create Lead
* [details](docs/sdks/leads/README.md#details) - Get Lead Details
* [find](docs/sdks/leads/README.md#find) - Get Lead
* [list](docs/sdks/leads/README.md#list) - Get All Leads
* [search](docs/sdks/leads/README.md#search) - Search Leads
* [update](docs/sdks/leads/README.md#update) - Update Lead

### [notes](docs/sdks/notes/README.md)

* [batch](docs/sdks/notes/README.md#batch) - Get Batch Notes
* [create](docs/sdks/notes/README.md#create) - Create Note
* [details](docs/sdks/notes/README.md#details) - Get Note Details
* [find](docs/sdks/notes/README.md#find) - Get Note
* [list](docs/sdks/notes/README.md#list) - Get All Notes
* [search](docs/sdks/notes/README.md#search) - Search Notes
* [update](docs/sdks/notes/README.md#update) - Update Note

### [passthrough](docs/sdks/passthrough/README.md)

* [create](docs/sdks/passthrough/README.md#create) - Passthrough Request

### [tasks](docs/sdks/tasks/README.md)

* [batch](docs/sdks/tasks/README.md#batch) - Get Batch Tasks
* [create](docs/sdks/tasks/README.md#create) - Create Task
* [details](docs/sdks/tasks/README.md#details) - Get Task Details
* [find](docs/sdks/tasks/README.md#find) - Get Task
* [list](docs/sdks/tasks/README.md#list) - Get All Tasks
* [search](docs/sdks/tasks/README.md#search) - Search Tasks
* [update](docs/sdks/tasks/README.md#update) - Update Task

### [users](docs/sdks/users/README.md)

* [batch](docs/sdks/users/README.md#batch) - Get Batch Users
* [details](docs/sdks/users/README.md#details) - Get User Details
* [find](docs/sdks/users/README.md#find) - Get User
* [list](docs/sdks/users/README.md#list) - Get All Users
* [search](docs/sdks/users/README.md#search) - Search Users

### [links](docs/sdks/links/README.md)

* [create](docs/sdks/links/README.md#create) - Exchange Public Token for Access Token

### [tokens](docs/sdks/tokens/README.md)

* [create](docs/sdks/tokens/README.md#create) - Create Link Token
<!-- End Available Resources and Operations [operations] -->







<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 400-600         | */*             |

### Example

```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI()

req = operations.DeleteConnectionRequestBody(
    connection_id='string',
)

res = None
try:
    res = s.connections.delete(req, operations.DeleteConnectionSecurity(
    vessel_api_token="<YOUR_API_KEY_HERE>",
))
except errors.SDKError as e:
    print(e)  # handle exception
    raise(e)

if res.status_code == 200:
    # handle response
    pass
```
<!-- End Error Handling [errors] -->



<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://api.vessel.land` | None |

#### Example

```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI(
    server_idx=0,
)

req = operations.DeleteConnectionRequestBody(
    connection_id='string',
)

res = s.connections.delete(req, operations.DeleteConnectionSecurity(
    vessel_api_token="<YOUR_API_KEY_HERE>",
))

if res.status_code == 200:
    # handle response
    pass
```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI(
    server_url="https://api.vessel.land",
)

req = operations.DeleteConnectionRequestBody(
    connection_id='string',
)

res = s.connections.delete(req, operations.DeleteConnectionSecurity(
    vessel_api_token="<YOUR_API_KEY_HERE>",
))

if res.status_code == 200:
    # handle response
    pass
```
<!-- End Server Selection [server] -->



<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the (requests)[https://pypi.org/project/requests/] HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with a custom `requests.Session` object.

For example, you could specify a header for every request that this sdk makes as follows:
```python
import vesselapi
import requests

http_client = requests.Session()
http_client.headers.update({'x-custom-header': 'someValue'})
s = vesselapi.VesselAPI(client: http_client)
```
<!-- End Custom HTTP Client [http-client] -->



<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name               | Type               | Scheme             |
| ------------------ | ------------------ | ------------------ |
| `vessel_api_token` | apiKey             | API key            |

You can set the security parameters through the `security` optional parameter when initializing the SDK client instance. For example:
```python
import vesselapi
from vesselapi.models import operations, shared

s = vesselapi.VesselAPI(
    security=shared.Security(
        vessel_api_token="<YOUR_API_KEY_HERE>",
    ),
)

req = operations.GetOneConnectionRequest(
    connection_id='string',
)

res = s.connections.find(req)

if res.response_body is not None:
    # handle response
    pass
```

### Per-Operation Security Schemes

Some operations in this SDK require the security scheme to be specified at the request level. For example:
```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI()

req = operations.DeleteConnectionRequestBody(
    connection_id='string',
)

res = s.connections.delete(req, operations.DeleteConnectionSecurity(
    vessel_api_token="<YOUR_API_KEY_HERE>",
))

if res.status_code == 200:
    # handle response
    pass
```
<!-- End Authentication [security] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->



### SDK Generated by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
