As part of a course at Zionet, we were given an assignment to create a microservices-based system.
The system brings the latest news, selects the most interesting news using AI based on the user's preferences, and sends them updates by email.

The system includes the following services:
1. Manager
2. Engine
3. User Accessor
4. Mail Accessor
5. HF Accessor
6. News Accessor

Below is a diagram:




To run the system, you use Docker.
Run the command docker-compose up.

To test the system we will use swagger:
http://localhost:8000/docs