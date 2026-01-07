# GitHub REST API - Example Documentation

## Overview

The GitHub REST API allows you to manage repositories, issues, pull requests, and more.

**Base URL:** https://api.github.com

**Authentication:** Bearer token (Personal Access Token)

## Authentication

GitHub API requires authentication for most endpoints. Use a personal access token in the Authorization header:

```
Authorization: Bearer ghp_xxxxxxxxxxxxxxxxxxxx
```

## Endpoints

### Get a Repository

GET /repos/{owner}/{repo}

Get a repository by owner and name.

**Parameters:**
- owner (required, path, string): The account owner of the repository.
- repo (required, path, string): The name of the repository.

**Response:**
```json
{
  "id": 1296269,
  "name": "Hello-World",
  "full_name": "octocat/Hello-World",
  "owner": {
    "login": "octocat",
    "id": 1
  },
  "private": false,
  "description": "My first repository"
}
```

### List Repository Issues

GET /repos/{owner}/{repo}/issues

List issues in a repository.

**Parameters:**
- owner (required, path, string): The account owner of the repository.
- repo (required, path, string): The name of the repository.
- state (optional, query, string): Indicates the state of the issues to return. Can be either open, closed, or all. Default: open
- per_page (optional, query, integer): The number of results per page (max 100). Default: 30

**Response:**
```json
[
  {
    "id": 1,
    "number": 1347,
    "title": "Found a bug",
    "state": "open",
    "created_at": "2011-04-22T13:33:48Z"
  }
]
```

### Create an Issue

POST /repos/{owner}/{repo}/issues

Create a new issue.

**Parameters:**
- owner (required, path, string): The account owner of the repository.
- repo (required, path, string): The name of the repository.
- title (required, body, string): The title of the issue.
- body (optional, body, string): The contents of the issue.
- labels (optional, body, array): Labels to associate with this issue.

**Response:**
```json
{
  "id": 1,
  "number": 1347,
  "title": "Found a bug",
  "state": "open",
  "created_at": "2011-04-22T13:33:48Z"
}
```

### Get Authenticated User

GET /user

Get the authenticated user's profile.

**Response:**
```json
{
  "login": "octocat",
  "id": 1,
  "name": "The Octocat",
  "email": "octocat@github.com",
  "public_repos": 2
}
```

## Rate Limits

For authenticated requests, you can make up to 5,000 requests per hour. For unauthenticated requests, the rate limit allows for up to 60 requests per hour.
