# Stripe Payments API - Example Documentation

## Overview

The Stripe API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

**Base URL:** https://api.stripe.com/v1

**Authentication:** Bearer token (API key)

## Authentication

Authenticate your account by including your secret key in API requests. You can manage your API keys in the Stripe Dashboard. Your API keys carry many privileges, so be sure to keep them secure!

Authentication to the API is performed via HTTP Bearer Auth. Provide your API key as the bearer token value.

```
Authorization: Bearer YOUR_STRIPE_API_KEY
```

## Endpoints

### Create a Charge

POST /charges

Creates a new charge object to charge a credit or debit card.

**Parameters:**
- amount (required, integer): Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00).
- currency (required, string): Three-letter ISO currency code, in lowercase. Must be a supported currency.
- source (optional, string): A payment source to be charged. This can be the ID of a card, bank account, or source.
- description (optional, string): An arbitrary string which you can attach to a charge object.

**Response:**
```json
{
  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",
  "object": "charge",
  "amount": 2000,
  "currency": "usd",
  "status": "succeeded",
  "created": 1680800504
}
```

### Retrieve a Charge

GET /charges/{id}

Retrieves the details of a charge that has previously been created.

**Parameters:**
- id (required, path, string): The identifier of the charge to be retrieved.

**Response:**
```json
{
  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",
  "object": "charge",
  "amount": 2000,
  "currency": "usd",
  "status": "succeeded"
}
```

### List all Charges

GET /charges

Returns a list of charges you've previously created. The charges are returned in sorted order, with the most recent charges appearing first.

**Parameters:**
- limit (optional, query, integer): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
- starting_after (optional, query, string): A cursor for use in pagination.

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",
      "object": "charge",
      "amount": 2000,
      "currency": "usd"
    }
  ],
  "has_more": false
}
```

### Create a Customer

POST /customers

Creates a new customer object.

**Parameters:**
- email (optional, string): Customer's email address.
- name (optional, string): The customer's full name or business name.
- description (optional, string): An arbitrary string that you can attach to a customer object.

**Response:**
```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "email": "customer@example.com",
  "name": "John Doe",
  "created": 1680800504
}
```

## Rate Limits

The Stripe API has rate limits to prevent abuse. The default rate limit is 100 requests per second in test mode and 100 requests per second in live mode.

## Error Handling

Stripe uses conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Stripe's servers.
