A comprehensive, production-ready blog platform built with Django and Django REST Framework that includes premium content, payment integration, collaboration features, and advanced user management.


🌟 Complete Feature Overview
🔐 Authentication & User Management
User Registration & Login with token authentication

Password Reset functionality

User Profiles with avatar uploads and bio

Role-based Access Control (Regular vs Premium users)

Profile Management with edit capabilities

💰 Premium Content & Payment System
Paystack Payment Integration for premium subscriptions

Two-tier User System: Regular (free) and Premium (paid)

Premium Content Gating - exclusive posts for paying users

Payment Verification with transaction tracking

Automatic User Status Upgrade after successful payment

👥 Collaboration Features
Post Invitation System - invite contributors via email

Multi-author Posts with contributor management

Invitation Token System with acceptance tracking

Role-based Post Editing (authors and contributors only)

📝 Advanced Content Management
Rich Text Editor (CKEditor) for enhanced content creation

Category-based Organization with filtering

Post Scheduling with publication dates

Premium Post Flagging for exclusive content

View Tracking with user-specific view counting

💬 Social & Engagement Features
Comment System with user authentication

Nested Comments for discussions

Post View Analytics with unique viewer tracking

Trending Posts Algorithm based on views and comments

Newsletter Subscription with email notifications

🎯 Content Discovery
Advanced Search & Filtering by categories

Trending Posts with customizable thresholds

Category-based Browsing

Recent Posts ordering

Author Profile Pages with post collections

🛠️ Technology Stack
Backend
Django 4.2+ - Web framework

Django REST Framework - API development

CKEditor with Upload - Rich text editing

Paystack API - Payment processing

SQLite/PostgreSQL - Database

Pillow - Image processing

Additional Features
Email Integration (invitations, notifications)

File Upload (images, avatars)

UUID-based Invitation System

Custom Permissions System

📋 Prerequisites
Python 3.8 or higher

pip (Python package manager)

Git

Paystack account (for payment processing)

🔧 API Endpoints
Authentication
POST /api/register/ - User registration

POST /api/login/ - User login (token-based)

GET /api/profile/ - User profile management

Posts & Content
GET /api/posts/ - List posts (filtered by user status)

GET /api/posts/category/<name>/ - Posts by category

GET /api/posts/<title>/ - Single post with comments

POST /api/posts/create/ - Create new post

PATCH /api/posts/<title>/edit/ - Edit post (author/contributors only)

Payments & Premium
POST /api/payment/initiate/ - Initialize Paystack payment

POST /api/payment/verify/ - Verify payment and upgrade user

Premium posts automatically restricted for regular users

Collaboration
POST /api/posts/<title>/invite/ - Send contributor invitations

GET /api/accept_invitation/<token>/ - Accept invitation

GET /api/posts/<title>/contributors/ - List post contributors

Engagement
POST /api/posts/<title>/comments/ - Add comments

GET /api/trending-posts/ - Get trending posts

POST /api/subscribe/ - Newsletter subscription


git clone https://github.com/Abdullateef2006/advanced_blog.git
cd advanced_blog/blog_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "SECRET_KEY=your-key" > .env
echo "DEBUG=True" >> .env
echo "PAYSTACK_SECRET_KEY=your-paystack-key" >> .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
