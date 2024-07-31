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
