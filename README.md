# Django Blog API

A backend-only Blog API built with Django REST Framework and JWT Authentication.

## Features

- User registration
- JWT authentication
- Category CRUD
- Post CRUD
- Comment CRUD
- Public read access for published posts
- Draft / published post status
- Only author can update or delete their own posts
- Staff/admin can manage all posts
- Search posts by title
- Filter posts by status and category
- Filter comments by post
- Publish and unpublish post API
- Tested with Postman

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Postman

## Installation

```bash
git clone <your-repo-url>
cd django_blog_api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

---------------------------------------

API Endpoints:

Auth:
POST /api/register/
POST /api/token/
POST /api/token/refresh/

Categories:
GET    /api/categories/
POST   /api/categories/
GET    /api/categories/{id}/
PATCH  /api/categories/{id}/
DELETE /api/categories/{id}/

Posts:
GET    /api/posts/
POST   /api/posts/
GET    /api/posts/{id}/
PATCH  /api/posts/{id}/
DELETE /api/posts/{id}/
PATCH  /api/posts/{id}/publish/
PATCH  /api/posts/{id}/unpublish/

Comments:
GET    /api/comments/
POST   /api/comments/
GET    /api/comments/{id}/
PATCH  /api/comments/{id}/
DELETE /api/comments/{id}/

Filters:
GET /api/posts/?search=django
GET /api/posts/?status=published
GET /api/posts/?category=1
GET /api/comments/?post=1


-----------------------------------------
Example Create Post
{
  "category": 1,
  "title": "Learning Django REST Framework",
  "content": "This is my first blog post API.",
  "status": "draft"
}

Example Create Comment
{
  "post": 1,
  "content": "Great article!"
}