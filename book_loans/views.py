import jwt
from django.conf import settings
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from book_loans.models import Book, BookLoans
from members.models import Members
from book_loans.forms import BookLoanForm


def index(request):
    latest_book_loan_list = BookLoans.objects.order_by("-created_at")[:10]
    books = Book.objects.all()
    member = Members.objects.all()
    context = {
        "book_loans": latest_book_loan_list,
        "form": BookLoanForm(),
        "books": books,
        "members": member,
    }

    if request.method == "POST":
        form = BookLoanForm(request.POST)
        if form.is_valid:
            book_id = request.POST["book"]
            member_id = request.POST["member"]
            loan_date = form.data["loan_date"]
            due_date = form.data["due_date"]
            return_date = form.data["return_date"] or None
            notes = form.data["notes"]

            book = books.get(id=book_id)
            new_stock = book.stock - 1
            books.filter(id=book_id).update(stock=new_stock)

            auth_session = request.session.get("auth_session", None)
            decoded = jwt.decode(
                auth_session, settings.JWT_SECRET, algorithms=["HS256"]
            )
            librarians_id = decoded["librarian_id"]

            BookLoans.objects.create(
                book_id=book_id,
                member_id=member_id,
                loan_date=loan_date,
                due_date=due_date,
                notes=notes,
                librarians_id=librarians_id,
                return_date=return_date,
            )

    return render(request, "loans.html", context)


def update(request, id):
    latest_book_loan_list = BookLoans.objects.order_by("created_at")[:10]
    loan = get_object_or_404(BookLoans, id=id)
    books = Book.objects.all()
    member = Members.objects.all()
    context = {
        "book_loans": latest_book_loan_list,
        "loan": loan,
        "books": books,
        "members": member,
    }
    initial_dict = {
        "loan_date": loan.loan_date,
        "due_date": loan.due_date,
        "return_date": loan.return_date,
        "notes": loan.notes,
    }
    form = BookLoanForm(request.POST or None, initial=initial_dict)

    if request.method == "POST":
        book_id = request.POST["book"]
        member_id = request.POST["member"]
        loan = BookLoans.objects.filter(id=id)

        auth_session = request.session.get("auth_session", None)
        decoded = jwt.decode(auth_session, settings.JWT_SECRET, algorithms=["HS256"])
        librarians_id = decoded["librarian_id"]
        context["initial_book_id"] = book_id

        if form.is_valid:
            loan_date = form.data["loan_date"]
            due_date = form.data["due_date"]
            return_date = form.data["return_date"] or None
            notes = form.data["notes"]

            loan.update(
                book_id=book_id,
                member_id=member_id,
                librarians_id=librarians_id,
                loan_date=loan_date,
                due_date=due_date,
                return_date=return_date,
                notes=notes,
                updated_at=datetime.now(),
            )
            return HttpResponseRedirect("/dashboard/book-loans")

    context["form"] = form
    return render(request, "book_loan_update_form.html", context)


def delete(request, id):
    context = {}
    book_loan = get_object_or_404(BookLoans, id=id)

    if request.method == "POST":
        book_loan.delete()
        return HttpResponseRedirect("/dashboard/book-loans")

    return render(request, "loans.html", context)
