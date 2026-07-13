const content = `
# HTTP — Level 1 (Beginner)
## What is HTTP?
**HTTP (HyperText Transfer Protocol)** is a set of rules that allows two computers to communicate over a network, usually the internet.
When you open a website, use a mobile app, or call an API, HTTP is often the language being used behind the scenes.
Think of it as:
> "The protocol that defines how a client asks for information and how a server responds."
---
## Why does HTTP exist?
Computers need a standard way to talk to each other.
Without HTTP:
* Every website would communicate differently.
* Browsers would need custom code for every website.
* Mobile apps wouldn't know how to talk to APIs.
HTTP gives everyone a common language.
---
## What problem does it solve?
Imagine walking into a restaurant.
Without rules:
* Customers shout random things.
* Waiters don't know what customers want.
* Food arrives at random tables.
Chaos.
HTTP solves the same problem for computers by defining:
1. How to ask for something.
2. How to respond.
3. How to indicate success or failure.
4. How to send data.
---
## Core Concepts You Must Understand First

Before learning advanced HTTP, understand these concepts:

### 1. Client
The thing making the request.
Examples:
* Browser
* Mobile app
* Backend service
* Curl command
Example:
\`\`\`text
Chrome Browser
\`\`\`
---

### 2. Server

The thing receiving requests and sending responses.

Examples:

* Google servers
* Your Golang API
* Firebase
* Supabase

Example:
\`\`\`text
api.myapp.com
\`\`\`

---

### 3. Request

A message sent from a client to a server.

Example:

\`\`\`text
Please give me the user profile.
\`\`\`

---

### 4. Response

The server's answer.

Example:

\`\`\`text
Here is the user profile.
\`\`\`

---

### 5. URL

The address of the thing you want.

Example:

\`\`\`text
https://api.myapp.com/users/1
\`\`\`

---

### 6. Data

Information being transferred.

Example:

\`\`\`json
{
  "name": "Sibongiseni"
}
\`\`\`

---

## Assumptions You Should Already Know

Before learning HTTP, it helps to understand:

### Required

* What a computer is
* What a network is
* What the internet is
* Basic client/server idea

### Nice to Have

* JSON
* Web browsers
* Mobile apps
* APIs

If you know React Native and Golang already, you're ready.

---

# A Simple Example

Imagine your backend has:

\`\`\`text
https://api.afika.app/profile
\`\`\`

Your mobile app sends:

\`\`\`http
GET /profile
\`\`\`

The server receives it and responds:

\`\`\`json
{
  "name": "Sibongiseni",
  "country": "South Africa"
}
\`\`\`

Flow:

\`\`\`text
Mobile App
    |
    | Request
    v
Server
    |
    | Response
    v
Mobile App
\`\`\`

---

## What Actually Happens?

### Step 1

You open your app.

\`\`\`text
Open Profile Screen
\`\`\`

### Step 2

The app asks the server:

\`\`\`http
GET /profile
\`\`\`

### Step 3

The server looks for the profile.

### Step 4

The server sends back:

\`\`\`json
{
  "name": "Sibongiseni"
}
\`\`\`

### Step 5

The app displays:

\`\`\`text
Hello Sibongiseni
\`\`\`

---

## Real World Analogy

Think of HTTP like ordering food.

### Request

\`\`\`text
Can I have a burger?
\`\`\`

### Server Processing

Kitchen makes burger.

### Response

\`\`\`text
Here's your burger.
\`\`\`

---

## How a Backend Engineer Sees HTTP

Most backend work is:

1. Receive HTTP requests.
2. Validate them.
3. Query a database.
4. Return HTTP responses.

Example in Go:

\`\`\`go
func GetUser(w http.ResponseWriter, r *http.Request) {
    user := User{
        Name: "Sibongiseni",
    }

    json.NewEncoder(w).Encode(user)
}
\`\`\`

The entire internet is basically millions of these request/response interactions every second.

---

# Explain Like I'm 10

Imagine you're at school.

You walk up to the librarian and say:

> "Can I borrow the Harry Potter book?"

That's the **request**.

The librarian checks the shelf.

Then says:

> "Here it is."

That's the **response**.

You are the **client**.

The librarian is the **server**.

The question is the **HTTP request**.

The answer is the **HTTP response**.

The rule that says how you should ask and how the librarian should answer is **HTTP**.

---

# Mental Model

If you remember only one thing:

\`\`\`text
Client  ---> Request ---> Server

Client <--- Response <--- Server
\`\`\`

HTTP is simply the set of rules that makes this conversation possible.

---

## Level 1 Checklist

You understand HTTP when you can answer:

* What is a client?
* What is a server?
* What is a request?
* What is a response?
* What is a URL?
* Why do computers need HTTP?

Once these are clear, the next level is:

**Level 2: HTTP Messages**

* Methods (GET, POST, PUT, DELETE)
* Headers
* Body
* Status Codes
* JSON APIs

That's where HTTP starts becoming useful for backend engineering.
`;

export { content };
