# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import calendar_, ir

__all__ = ['register']


def register():
    Pool.register(
        calendar_.CalendarModel,
        calendar_.Calendar,
        calendar_.ReadUser,
        calendar_.WriteUser,
        calendar_.Category,
        calendar_.Location,
        calendar_.Event,
        calendar_.EventCategory,
        calendar_.EventAlarm,
        calendar_.EventAttendee,
        calendar_.EventRDate,
        calendar_.EventExDate,
        calendar_.EventRRule,
        calendar_.EventExRule,
        calendar_.CalendarResource,
        ir.Rule,
        module='calendar', type_='model')
