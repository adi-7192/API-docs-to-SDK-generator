# Twilio Messaging API - Example Documentation

## Overview

The Twilio Messaging API allows you to send and receive SMS and MMS messages.

**Base URL:** https://api.twilio.com/2010-04-01

**Authentication:** Basic Auth (Account SID and Auth Token)

## Authentication

Twilio uses HTTP Basic authentication. Provide your Account SID as the username and your Auth Token as the password.

## Endpoints

### Send a Message

POST /Accounts/{AccountSid}/Messages.json

Send an SMS or MMS message.

**Parameters:**
- AccountSid (required, path, string): The SID of the Account creating the Message resource.
- To (required, body, string): The recipient's phone number in E.164 format.
- From (required, body, string): The sender's Twilio phone number in E.164 format.
- Body (required, body, string): The text content of the message (up to 1,600 characters).
- MediaUrl (optional, body, array): The URL of media to include in the message (for MMS).

**Response:**
```json
{
  "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "from": "+15558675310",
  "to": "+15551234567",
  "body": "Hello from Twilio!",
  "status": "queued",
  "date_created": "Mon, 16 Aug 2021 03:45:01 +0000"
}
```

### Retrieve a Message

GET /Accounts/{AccountSid}/Messages/{MessageSid}.json

Fetch a specific message by its SID.

**Parameters:**
- AccountSid (required, path, string): The SID of the Account that created the Message resource.
- MessageSid (required, path, string): The SID of the Message resource to fetch.

**Response:**
```json
{
  "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "from": "+15558675310",
  "to": "+15551234567",
  "body": "Hello from Twilio!",
  "status": "delivered"
}
```

### List Messages

GET /Accounts/{AccountSid}/Messages.json

Retrieve a list of messages belonging to the account.

**Parameters:**
- AccountSid (required, path, string): The SID of the Account that created the Message resources.
- To (optional, query, string): Filter by recipient phone number.
- From (optional, query, string): Filter by sender phone number.
- PageSize (optional, query, integer): How many resources to return in each list page. Default: 50

**Response:**
```json
{
  "messages": [
    {
      "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "from": "+15558675310",
      "to": "+15551234567",
      "body": "Hello from Twilio!",
      "status": "delivered"
    }
  ],
  "page": 0,
  "page_size": 50
}
```

## Rate Limits

Twilio enforces rate limits to ensure system stability. The default limit is 60 requests per second per account.

## Error Codes

- 20003: Authentication Error
- 21211: Invalid 'To' Phone Number
- 21614: 'To' number is not a valid mobile number
