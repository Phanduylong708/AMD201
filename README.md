# Ride Sharing System

A FastAPI-based microservices system for ride sharing, developed as part of the AMD201 Advanced Microservice Development and Deployment coursework.

## Project Structure

```
ride-sharing/
├── api-gateway/          # API Gateway service
├── services/            
│   ├── user/            # User management service
│   ├── rider/           # Rider management service
│   ├── booking/         # Booking management service
│   └── ride-matching/   # Ride matching service
├── docs/                # Documentation and C4 diagrams
└── requirements.txt     # Project dependencies
```

## Services Overview

1. **User Service**: Handles user authentication and profile management
2. **Rider Service**: Manages rider profiles and availability
3. **Booking Service**: Handles ride requests and fare calculation
4. **Ride Matching Service**: Implements rider matching logic
5. **API Gateway**: Central entry point for all client requests

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Team

- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

## Documentation

Detailed documentation including API specifications and architecture diagrams can be found in the `/docs` directory. 