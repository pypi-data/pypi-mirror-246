# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.model.exceptions import ValidationError


class CalendarNameValidationError(ValidationError):
    pass


class EventInvalidRecurrenceError(ValidationError):
    pass


class InvalidRRuleError(ValidationError):
    pass
