
Product Catalog API

Author: Ivy Githinji
Admission Number: C027-01-0883/2024
Course: CIT 3107 - Back-End Development
Date: July 2026


Project Overview

A complete CRUD API for a product catalog with categories. This simulates a real-world e-commerce backend.


Features

Category management (Create, List)
Product management (Create, Read, Update, Delete)
Product search by name or description
Product filtering by category and price range
Product statistics (total products, average price, etc.)
Unique product name validation
Pagination support


Tech Stack

FastAPI - Web framework
SQLModel - ORM + Pydantic
SQLite - Database
Uvicorn - ASGI server


API Endpoints

Categories

POST /categories - Create a new category
GET /categories - List all categories

Products

POST /products - Create a new product
GET /products - List all products (with filters)
GET /products/{id} - Get a specific product
PATCH /products/{id} - Update a product
DELETE /products/{id} - Delete a product
GET /products/search - Search products by name/description
GET /products/stats - Get product statistics


Sample Data

Categories

ID: 1, Name: Marketing, Description: Marketing and advertising tools
ID: 2, Name: Data, Description: Data analytics and database solutions
ID: 3, Name: Consulting, Description: Business and HR consulting tools

Products

ID: 1, Name: Social Media Scheduler, Category: Marketing, Price: 25,000 KES, Stock: 15
ID: 2, Name: Email Marketing Tool, Category: Marketing, Price: 18,000 KES, Stock: 8
ID: 3, Name: Data Analytics Dashboard, Category: Data, Price: 45,000 KES, Stock: 5
ID: 4, Name: Database Cleaner, Category: Data, Price: 12,000 KES, Stock: 20
ID: 5, Name: Strategy Planning Tool, Category: Consulting, Price: 55,000 KES, Stock: 3
ID: 6, Name: HR Management System, Category: Consulting, Price: 38,000 KES, Stock: 7



Screenshots

Swagger UI screenshot
Products list screenshot
Stats endpoint screenshot
Search endpoint screenshot
Categories list screenshot


Lessons Learned

Database relationships - Connecting products to categories
CRUD operations - Full create, read, update, delete functionality
Data validation - Ensuring data integrity
API design - Clean, intuitive endpoints
Error handling - Proper HTTP status codes




GitHub: ivygithinji-student
Email: ivy.githinji24@students.dkut.ac.ke

