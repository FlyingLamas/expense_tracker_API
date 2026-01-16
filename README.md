Expense Tracker API (Django REST Framework)

A secure and fully featured RESTful API for tracking personal expenses, built using Django REST Framework (DRF).
This API allows users to record expenses, categorize them, generate reports, and manage their financial data securely.

Features
1. Authentication & Security
  - Token-based authentication
  - Permissions ensuring users can only access their own expenses
  - User-specific queryset filtering in all endpoints

2. Expense Management (CRUD)
  - Create, Read, Update, and Delete expenses
  - Each expense contains: title, description, amount, category, and date
  - Automatic ownership assignment during creation

3. Filtering, Searching & Ordering
  - Filter expenses by:
    1. category
    2. expense_date
  - Search by:
    1. title
    2. description
  - Order by:
    1. amount
    2. expense_date

4. Analytics & Reports
  - Overall summary using aggregate functions:
    1. Total amount
    2. Average
    3. Minimum
    4. Maximum
    5. Count

  - Monthly report: filter by month & year

5. Pagination
  - Custom page size pagination for efficient data handling

Tech Stack
  - Backend: Django, Django REST Framework
  - Database: Sqlite
  - Authentication: Token Authentication


