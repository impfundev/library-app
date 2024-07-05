## Librarian App

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

### Start Development

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

4. Configure secure variable ```.env```

```
cp .env.example .env
```

in ```.env```

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


### Features

* **Masters:**
    * Book Master - Manage book details (title, etc.)
    * Member Master - Manage member information (name, contact details, etc.)
    * Librarian Master - Manage librarian accounts (username, password, etc.)
* **Transactions:**
    * Book Loan - Record book lending and return activity
    * Login History - Track librarian login attempts
* **Functionalities:**
    * Login - Secure access for librarians
    * CRUD (Create, Read, Update, Delete) operations for:
        * Book records
        * Member records
        * Librarian records
        * Book loan records
* **Reports:**
    * Near Outstanding Book Loans - Identify loans nearing due date
    * Overdue Book Loans - View books currently overdue
    * Librarian Login History - Track librarian activity

### Usage

1. **Login:**
    * Access the application login page.
    * Enter valid librarian credentials.
    * Click Login.
2. **Book Management:**
    * Access the Book Master section.
    * View existing book records.
    * Add new book entries.
    * Edit or update existing book information.
    * Delete unwanted book records.
3. **Member Management:**
    * Access the Member Master section.
    * View existing member records.
    * Add new member entries.
    * Edit or update existing member information.
    * Delete unwanted member records.
4. **Librarian Management:**
    * Access the Librarian Master section (**Note:** Restricted access)
    * View existing librarian accounts.
    * Add new librarian accounts (**Note:**  Grant appropriate access levels)
    * Edit or update existing librarian information.
    * Delete unwanted librarian accounts (**Note:**  Maintain at least one active account)
5. **Book Loan Management:**
    * Access the Book Loan section.
    * View existing loan records.
    * Create new loan entries (linking books and members).
    * Edit or update loan details (e.g., return date).
    * Mark loans as returned.
6. **Reports:**
    * Access the Reports section.
    * View a list of Near Outstanding Book Loans.
    * View a list of Overdue Book Loans.
    * View historical Librarian Login data.
