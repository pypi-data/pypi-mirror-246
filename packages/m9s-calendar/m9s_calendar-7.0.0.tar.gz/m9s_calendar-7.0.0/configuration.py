# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import (
    ModelSingleton, ModelSQL, ModelView, MultiValueMixin, ValueMixin, fields)
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction

#allowed_models = fields.One2Many('ir.model', 'company',
#            'Allowed models')


class Configuration(
        ModelSingleton, ModelSQL, ModelView):
    'Calendar Configuration'
    __name__ = 'calendar.configuration'

    allowed_models = fields.Many2Many('calendar.configuration.company_model',
        'company', 'calendar_model', 'Allowed models',
        #domain=[
        #    ('company', '=', Eval('context', {}).get('company', -1)),
        #    ],
        help="The models that can be used as a calendar resource")


#class Configuration(
#        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
#    'Calendar Configuration'
#    __name__ = 'calendar.configuration'

#    allowed_models = fields.MultiValue(allowed_models)

#    @classmethod
#    def multivalue_model(cls, field):
#        pool = Pool()
#        #if field in {'calendar_invoice_method', 'calendar_shipment_method'}:
#        #    return pool.get('calendar.configuration.calendar_method')
#        if field == 'allowed_models':
#            return pool.get('calendar.configuration.allowed_models')
#        return super(Configuration, cls).multivalue_model(field)




#class ConfigurationCalendarModel(ModelSQL, CompanyValueMixin):
#    "Calendar Configuration Calendar Model"
#    __name__ = 'calendar.configuration.allowed_models'
#    allowed_models = allowed_models


class CalendarCompanyModel(ModelSQL):
    'Calendar Model per Company'
    __name__ = 'calendar.configuration.company_model'
    company = fields.Many2One('company.company', 'Company', ondelete='CASCADE',
        required=True,
        #domain=[
        #    ('company', '=', Eval('context', {}).get('company', -1)),
        #    ],
        ),
    calendar_model = fields.Many2One('ir.model', 'Model', ondelete='CASCADE',
        required=True)

    @staticmethod
    def default_company(cls):
        return Transaction().context.get('company')
