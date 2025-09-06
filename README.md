# job-portal

# Job Portal Backend

A platform for managing job postings, applications, and user profiles (job seekers & employers).  
Built with **Django + DRF** and powered by **Docker, Redis, Celery, ElasticSearch, Swagger, and JWT Authentication**.

---

## 🚀 Features
- Full authentication system:
  - Registration & login with JWT
  - Email verification
  - Password reset
  - Google Social Login
- Job Seeker & Employer profile management
- Job & JobApplication models with workflow and publication control
- Notification & email system for job events
- **Repository Pattern** for data access layer
- **Redis-backed pagination** for jobs and applications
- Job search & filtering with **ElasticSearch**
- API documentation with **Swagger**
- **Celery + Redis** for background tasks (e.g., email sending)

---

## 🛠️ Tech Stack
- **Backend:** Django, Django Rest Framework
- **Auth:** SimpleJWT, django-allauth
- **DB:** PostgreSQL
- **Cache/Queue:** Redis + Celery
- **Search:** ElasticSearch
- **Containerization:** Docker, Docker Compose
- **Reverse Proxy (future):** Nginx

---

## 📂 Project Structure (simplified)
core/
┣ models/ # Core models (User, Job, JobApplication, Profile, Notification)
┣ serializers/ # DRF serializers
┣ views/ # API views
┣ repositories/ # Repository Pattern for models
┣ tasks.py # Celery tasks (emails, etc.)
┗ urls.py