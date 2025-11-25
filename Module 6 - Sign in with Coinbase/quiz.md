# Module 6: Knowledge Check

### Q1: In the OAuth2 flow, what is the purpose of the `state` parameter?
A) To tell the server which country the user is in.
B) To prevent Cross-Site Request Forgery (CSRF) attacks.
C) To store the user's password.
D) It is optional and useless.

### Q2: Which grant type is used to exchange an Authorization Code for an Access Token?
A) `client_credentials`
B) `implicit`
C) `authorization_code`
D) `password`

### Q3: If an Access Token expires, what should the application do?
A) Ask the user to log in again.
B) Use the `refresh_token` to get a new pair of tokens.
C) Panic and crash.
D) Generate a new random string.

### Q4: Why is PKCE (Proof Key for Code Exchange) recommended?
A) It makes the URL shorter.
B) It prevents authorization code interception attacks (especially on mobile/public clients).
C) It speeds up the request.

---
**Answers:**
1: B
2: C
3: B
4: B

