from django.utils import timezone

from users.models import LibrarianLoginHistory, Member
from book.models import Category, Book
from loans.models import BookLoan


def dashboard_context(request):
    login_history = LibrarianLoginHistory.objects.order_by("-date")[:10]
    book_loans = BookLoan.objects.all()
    total_book = Book.objects.count()
    total_category = Category.objects.count()
    total_member = Member.objects.count()
    total_book_loans = book_loans.count()

    now = timezone.now()
    overdue_loans = book_loans.filter(due_date__lte=now, return_date=None).order_by(
        "-due_date"
    )[:10]

    due_date_treshold = now + timezone.timedelta(days=3)
    upcoming_loans = (
        book_loans.filter(due_date__lte=due_date_treshold, return_date=None)
        .filter(due_date__gte=now)
        .order_by("-due_date")[:10]
    )

    data = {
        "login_histories": login_history,
        "total_book": total_book,
        "total_category": total_category,
        "total_member": total_member,
        "total_book_loans": total_book_loans,
        "total_overdue": overdue_loans.count(),
        "total_upcoming": upcoming_loans.count(),
        "overdue_loans": overdue_loans,
        "upcoming_loans": upcoming_loans,
    }

    return data
