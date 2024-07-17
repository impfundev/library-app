from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def validate_loan_date(value):
    now = timezone.now()
    loan_date = value
    if loan_date > now:
        raise ValidationError(
            _("Loan date cannot be later than today"),
            params={"value": value},
        )


def validate_due_date(value):
    due_date = value
    loan_date = timezone.now()
    if due_date < loan_date:
        raise ValidationError(
            _("Due date cannot be less than loan date"),
            params={"value": value},
        )
