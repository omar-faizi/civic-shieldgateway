Civic-Shield: Geofenced Security Gateway

Civic-Shield is a FastAPI-based API gateway designed to protect sensitive infrastructure data for the City of Toronto by enforcing multiple layers of security before any request is allowed through.

Security Approach

Geofencing (Layer 1)
Incoming requests are checked using the ipinfo geolocation service. Any traffic coming from outside of Canada is automatically blocked.

JWT Authentication (Layer 2)
Access to protected endpoints requires a valid JSON Web Token (JWT), ensuring that only authenticated users can interact with the API.

Fail-Closed Design
If any security dependency (such as geolocation or token verification) becomes unavailable, the system denies access by default. This prevents data exposure during outages or misconfigurations.

Technology Stack

Language: Python

Framework: FastAPI

Security Tools: JWT (python-jose), ipinfo Geolocation API
