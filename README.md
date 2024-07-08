# Librarian App

The Librarian App is a library management tool designed to streamline book lending and member management processes. It offers functionalities for librarians to:

* Manage book entries (add, edit, delete)
* Manage member information (add, edit, delete)
* Manage librarian accounts (add, edit, delete with access control)
* Record book loans and returns
* Track librarian login history
* Generate reports on:
  * Near outstanding book loans
  * Overdue book loans
  * Librarian login activity

This app provides a centralized platform for librarians to effectively manage library resources and user interactions.

## API

prefix: `/api/v1`

postman:

### Auth

| Endpoint | Description | HTTP |
|----|----|----|
| `/auth/login` | Login for librarian or member | POST |
| `/auth/logout` | Logout for librarian or member | GET |
| `/auth/registration` | Register new librarian or member | POST |
| `/auth/password/reset` | Reset password | POST |
| `/auth/password/reset/confirm` | Confirm reset password | POST |

### Books

| Endpoint | Description | HTTP |
|----|----|----|
| `/books` | book lists | GET |
| `/books/{{ book.id }}` | book details | GET, POST, PUT |
| `/books?search={{ book.title }}` | search book lists, filtered by name | GET |
| `/books?year={{ year }}` | filter book lists by year | GET |
| `/books?category={{ category }}` | filter book lists by category | GET |

### Categories

| Endpoint | Description | HTTP |
|----|----|----|
| `/categories` | category lists | GET |
| `/categories/{{ book.id }}` | category details | GET, POST, PUT |
| `/categories?search={{ book.title }}` | search category  lists, filtered by name | GET |
| `/categories?year={{ year }}` | filter category  lists by year | GET |
| `/categories?category={{ category }}` | filter category  lists by category | GET |

### Members

| Endpoint | Description | HTTP |
|----|----|----|
| `/members` | member lists | GET |
| `/members/{{ book.id }}` | member details | GET, POST, PUT |
| `/members?search={{ book.title }}` | search member lists, filtered by name | GET |
| `/members?year={{ year }}` | filter member lists by year | GET |
| `/members?category={{ category }}` | filter member lists by category | GET |

### Librarians

| Endpoint | Description | HTTP |
|----|----|----|
| `/librarians` | librarian lists | GET |
| `/librarians/{{ book.id }}` | librarian details | GET, POST, PUT |
| `/librarians?search={{ book.title }}` | search librarian lists, filtered by name | GET |
| `/librarians?year={{ year }}` | filter librarian lists by year | GET |
| `/librarians?category={{ category }}` | filter librarian  lists by category | GET |

### Book Loans

| Endpoint | Description | HTTP |
|----|----|----|
| `/book-loans` | book loan lists | GET |
| `/book-loans/{{ book.id }}` | book loan details | GET, POST, PUT |
| `/book-loans?search={{ book.title }}` | search book loan  lists, filtered by name | GET |
| `/book-loans?year={{ year }}` | filter book loan lists by year | GET |
| `/book-loans?category={{ category }}` | filter book loan lists by category | GET |

## Start Development


1. Clone this project

```
git clone https://github.com/impfundev/library-app.git
cd library-app
```


2. Create virtual environments

```
python -m venv library_app_env

# linux
source library_app_env/bin/activate

# windows
library_app_env\Scripts\Activate.ps1
```


3. Install Depedencies

```
pip -r install requirements.txt
```


4. Configure secure variable `.env`

```
cp .env.example .env
```

in `.env`

```
JWT_SECRET= #SECURE RANDOM SECREET

### Database
PGHOST=""
PGDATABASE=""
PGUSER=""
PGPASSWORD=""
```


5. Make migration:

```
python manage.py makemigrations
python manage.py migrate
```


6. Run Development Server

```
python manage.py runserver
```


