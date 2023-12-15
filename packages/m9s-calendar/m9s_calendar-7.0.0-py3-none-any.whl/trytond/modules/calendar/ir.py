# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class Rule(metaclass=PoolMeta):
    __name__ = 'ir.rule'

    @classmethod
    def _context_modelnames(cls):
        """
        List of models to add 'user_id' to context
        """
        try:
            result = super()._context_modelnames()
        except Exception:
            result = set()
        result |= {
            'calendar.calendar',
            'calendar.event',
            }
        return result

    @classmethod
    def _get_context(cls, model_name):
        context = super()._get_context(model_name)
        if model_name in cls._context_modelnames():
            context['user_id'] = Transaction().user
        return context

    @classmethod
    def _get_cache_key(cls, model_name):
        key = super()._get_cache_key(model_name)
        if model_name in cls._context_modelnames():
            key = (*key, Transaction().user)
        return key
