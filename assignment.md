# AMD201 (2024/25) Advanced Microservice Development and Deployment

**Contribution:** 100% of course  
**Author:** Ngo Tra (TraNLT2@fe.edu.vn)  
**Technology:** FastAPI Microservice  
**Deadline:** 13/03/2025

--aaaaaaaaaaaa

## Build a Ride Sharing System with FastAPI

### Overview

A ride-sharing system allows users to request rides and be matched with the nearest available riders. Similar to popular ride-sharing platforms, this system will handle:

- User registration
- Rider management
- Ride booking
- Fare calculation
- Ride status updates

In this assignment, you will design and implement a backend-only microservices system using FastAPI. The goal is to apply system design and API development principles to build a scalable, performant, and efficient ride-hailing application.

### Scenario

You are a team of software engineers (3-4 members) working for a startup launching a new ride-sharing service. Your task is to develop the backend system and API for the service.

The system should:

- Use the C4 Model to document the software architecture.
- Allow users to register and book rides.
- Allow riders to register and accept ride requests.
- Assign the nearest available rider to a user based on a fake distance matrix.
- Calculate ride fares based on a tiered distance pricing model.
- Track ride status updates (Pending, In Progress, Completed, Canceled).
- Store all data in a PostgreSQL database.
- Earn additional points if Kafka is integrated.

### Requirements

#### 1. Software Architecture Design (C4 Model)

- **Documentation:** Use the C4 Model to describe and document the architecture.
- **Diagrams:** Include at least the following C4 diagrams:
  - **Context Diagram:** Overview of the system and its interactions with users and external components.
  - **Container Diagram:** High-level components such as FastAPI services, database, and external systems.
  - **Component Diagram:** Breakdown of microservices and their roles.
  - **Code Diagram (Optional):** A detailed view of class/module relationships within the system.

#### 2. User & Rider Management

- **Users:** Store name, phone number, and password.
- **Riders:** Store all user details plus rating and vehicle information (type, license plate).
- **Rider Status:** Track availability (Available / Busy).

#### 3. Finding the Closest Free Rider

- **Distance Matrix:** No real GPS integration; use a predefined table of 5 users mapped to 5 riders with random distances.

|         | **Rider_1** | **Rider_2** | **Rider_3** | **Rider_4** | **Rider_5** |
|---------|-------------|-------------|-------------|-------------|-------------|
| **User_1**  | 8 km        | 5 km        | 6 km        | 2 km        | 7 km        |
| **User_2**  | 3 km        | 9 km        | 4 km        | 6 km        | 1 km        |
| **User_3**  | 5 km        | 2 km        | 8 km        | 7 km        | 4 km        |
| **User_4**  | 6 km        | 10 km       | 3 km        | 1 km        | 9 km        |
| **User_5**  | 7 km        | 4 km        | 2 km        | 9 km        | 5 km        |

- **Assignment:** Assign the nearest available rider. If multiple riders are available, choose one randomly.

#### 4. Fare Calculation

- **Distance:** Random distance between 1 to 10 km.
- **Pricing Model:**
  - **1 km:** 10k/km
  - **2 - 4 km:** 15k/km
  - **More than 4 km:** 12k/km
- **Note:** No integration with Google Maps API or real-world distance calculation.

#### 5. Booking & Ride Status Management

- **Booking:** Instant ride requests only (no future bookings).
- **Ride Statuses:** Pending, In Progress, Completed, Canceled.

#### 6. Technology Stack & Features

- **Application Type:** Backend-only (no frontend required).
- **API Development:** FastAPI.
- **Database:** PostgreSQL.
- **Payments:** No payment integration (use fake payments).

### Core Microservices Architecture

For this Ride Sharing App coursework, a microservices-based architecture would typically include the following core services:

1. **User Service**
   - Manages user authentication and profile (CRUD operations).
   - Handles login, registration, and password management.
   - Implements JWT-based authentication and role-based access control.

2. **Rider Service**
   - Manages rider profiles, including availability status (Available/Busy).
   - Provides CRUD operations for riders.
   - Stores vehicle details (type, license plate) and ratings.

3. **Booking Service**
   - Manages ride requests and assigns the closest available rider.
   - Stores ride history and ride statuses (Pending, In Progress, Completed, Canceled).
   - Handles fare calculation based on distance.

4. **Ride Matching Service**
   - Implements the logic for finding the nearest available rider.
   - Uses the predefined table of users mapped to riders with random distances.
   - Ensures fair distribution if multiple riders are the closest.

5. **API Gateway Service**
   - Acts as the central entry point for clients (users & riders).
   - Manages request routing, load balancing, and authentication.

### Deliverables

- **Group Presentation (70%):**
  - Present your system design and implementation to the class.
  - Explain the architecture, technologies, and trade-offs of your solution.
  - Demonstrate the functionality of your web application.
  - Include slides and source code (with a git link).

- **Individual Report (30%):**
  - Write a self-evaluation report of the project.
  - Reflect on your contribution, challenges, and learning outcomes.
  - Provide feedback on team members and the assignment.
  - Include source code (with a git link showing your branch).

### Assessment

To pass the course, you must achieve an average score of at least 5.

#### Group Presentation Mark Criteria

- **9 - 10:** Exceptional presentation with thorough understanding, highly organized structure, seamless transitions, exceptional technical depth, flawless demonstration of functionality, and excellent, clean, well-documented source code.
- **7 – 8.5:** Solid understanding with clear organization, logical flow, clear technical explanations, successful demonstration with minor issues, and source code adhering to standards with few minor bugs.
- **5 – 6.5:** Basic understanding with significant gaps, somewhat organized structure with clarity issues, basic technical details, limited demonstration of functionality, and source code with some issues.
- **< 5:** Lacks understanding, coherence, and technical depth; disorganized structure; flawed technical explanations; ineffective demonstration; and poor source code quality.

#### Individual Report Mark Criteria

- **9 - 10:** Exceptional report with thorough and insightful reflection on personal contribution, challenges, and learning outcomes; detailed and constructive feedback on team members and the assignment; high level of self-awareness and critical evaluation.
- **7 – 8.5:** Solid understanding with reasonable reflection on personal contribution, challenges, and learning outcomes; constructive feedback with some specificity.
- **5 – 6.5:** Basic understanding with significant gaps; limited and shallow reflection on personal contribution, challenges, and learning outcomes; basic feedback.
- **< 5:** Lacks depth and understanding; superficial reflection; and limited or no feedback.

---

*File created based on the content from SP25-AMD201-ASSIGNMENT BRIEF.pdf*  
:contentReference[oaicite:0]{index=0}
