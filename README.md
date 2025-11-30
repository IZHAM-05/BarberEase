BARBERS WORLD
The traditional method of booking barbershop appointments often involves waiting in long queues or manually contacting shop owners, which can lead to inefficiencies and poor customer experience. The proposed system, BarberEase, is a web-based application that enables customers to discover barbershops, view their services, and conveniently book appointments online. The platform also empowers barbershop owners to manage their services and appointments, while a system administrator oversees the platform’s overall operations.By digitalizing appointment scheduling, BarberEase improves efficiency for barbers and enhances convenience for customers, ensuring reduced waiting times and streamlined business operations. The system has been developed entirely in Django, integrating both backend and frontend, with a focus on responsive design, usability, and secure data handling.
The BarberEase project is a web-based appointment booking system designed to simplify the interaction between customers and barbershops. Built using Django, the system integrates backend and frontend within a single framework, making it efficient and scalable. The platform introduces three types of users:
1.
Super Admin – Manages the platform, barbershops, users, and appointments.
2.
Barbershop Owners – Manage their shop profiles, services, and approve/reject customer bookings.
3.
Customers – Browse barbershops, view services, book appointments, and provide reviews.
The system includes key modules such as user authentication, barbershop management, appointment booking, service management, reviews & ratings, and role-based dashboards. Django templates, Bootstrap, and CSS are used for a responsive and interactive frontend, while the Django ORM handles database operations securely.
This project demonstrates practical skills in full-stack development with Django, covering user authentication, role-based access control, CRUD operations, and dashboard design. Future enhancements may include location-based shop search, online payments, and automated notifications to further enhance the system’s usability.
Requirements
•
Frontend: Django Templates, HTML5, CSS3, Bootstrap
•
Backend: Django Framework (Python)
•
Database: MySQL / PostgreSQL
•
Tools & IDEs: VS Code / PyCharm, Git (for version control)
•
Browser: Google Chrome / Mozilla Firefox
Modules
1. Authentication & User Management
•
Secure login and registration system with role-based access.
•
Supports three roles: Super Admin, Barber, and Customer.
•
Super Admin can add/remove barber accounts and monitor activities.
2. Super Admin Dashboard
•
Full control of the platform.
•
Manage barbershops, customers, appointments, and reviews.
•
Platform-wide statistics (total users, bookings, shops).
3. Barbershop Management Module (for Owners)
•
Shop profile management (name, address, contact, image).
•
Add, update, and delete services (with pricing).
•
Manage appointments by approving or rejecting bookings.
•
View customer reviews and ratings.
4. Appointment Booking Module (for Customers)
•
Customers choose a shop, service, and time slot.
•
System prevents double booking of time slots.
•
Customers can track appointment status (Pending / Approved / Rejected).
5. Reviews & Ratings Module
•
Customers leave star ratings and feedback after appointments.
•
Reviews are visible on shop profiles.
•
Helps improve shop credibility and customer decision-making.
6. Customer Dashboard
•
View upcoming and past appointments.
•
Track booking status.
•
Option to leave reviews and ratings.
7. Owner Dashboard
•
Overview of services, recent appointments, and reviews.
•
Appointment actions: Approve / Reject.
•
Service management and shop profile updates.
