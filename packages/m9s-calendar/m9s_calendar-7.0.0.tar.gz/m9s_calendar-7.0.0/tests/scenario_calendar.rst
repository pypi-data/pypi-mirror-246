=================
Calendar Scenario
=================

Imports::
    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules, set_user
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date.today()

Activate modules::

    >>> config = activate_modules('calendar')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create calendar users::

    >>> Group = Model.get('res.group')
    >>> group_calendar_admin, = Group.find(['name', '=', 'Calendar Administration'])
    >>> group_calendar, = Group.find(['name', '=', 'Calendar'])


    >>> User = Model.get('res.user')
    
    >>> cal_default = User()
    >>> cal_default.login = 'cal_default'
    >>> cal_default.name = 'cal_default'
    >>> cal_default.company = company
    >>> cal_default.save()
    
    >>> cal_admin = User()
    >>> cal_admin.login = 'cal_admin'
    >>> cal_admin.name = 'cal_admin'
    >>> cal_admin.company = company
    >>> cal_admin.groups.append(group_calendar_admin)
    >>> cal_admin.save()
    
    >>> cal1_user = User()
    >>> cal1_user.login = 'cal1_user'
    >>> cal1_user.name = 'cal1_user'
    >>> cal1_user.company = company
    >>> cal1_user.groups.append(group_calendar)
    >>> cal1_user.save()
    
    >>> cal2_user, = cal1_user.duplicate()
    >>> cal2_user.login = 'cal2_user'
    >>> cal2_user.name = 'cal2_user'
    >>> cal2_user.save()

    >>> #with config.set_context(periods=period_ids):

    >>> #print(config.context)
    >>> set_user(cal_admin.id)
    >>> #print(config.user)
    >>> #print(cal1_user.groups)

Set allowed models for calendars::

    >>> IrModel = Model.get('ir.model')
    >>> CalModel = Model.get('calendar.model')
    >>> models = IrModel.find([('model', 'in', ['party.party', 'res.user'])])
    >>> for model in models:
    ...     cal_model = CalModel()
    ...     cal_model.model = model
    ...     cal_model.company=company
    ...     cal_model.save()
    >>> len(CalModel.find([]))
    2

Create resources::

    >>> Resource = Model.get('calendar.resource')
    >>> for model in models:
    ...     # class of model
    ...     # currently setting of strings not supported by proteus
    ...     # caused by assert value.startswith(',')
    ...     # -> works in ModuleTestCase
    ...     #resource = Resource()
    ...     #res_name = model.model + ',-1'
    ...     #resource.email = '%s@example.com' % res_name
    ...     #resource.resource = res_name
    ...     #resource.save()
    ...     # instance of model
    ...     Instance = Model.get(model.model)
    ...     instance, = Instance.find([], limit=1)
    ...     res_name = instance.rec_name
    ...     resource = Resource()
    ...     resource.email = '%s@example.com' % res_name
    ...     resource.resource = instance
    ...     resource.save()
    >>> resources = Resource.find([])
    >>> len(resources)
    2

Create calendars for all patterns::

    >>> Calendar = Model.get('calendar.calendar')
    >>> for resource in resources:
    ...     for type in ['availability', 'freebusy']:
    ...         calendar = Calendar()
    ...         calendar.owner = resource
    ...         calendar.type = type
    ...         calendar.name = resource.rec_name
    ...         calendar.save()
    >>> len(Calendar.find([]))
    4

Test access permissions::

    >>> set_user(cal_default.id)
    >>> Calendar.find([])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    AccessError: ...

    >>> set_user(cal1_user.id)
    >>> len(Calendar.find([]))
    0

    >>> set_user(cal2_user.id)
    >>> len(Calendar.find([]))
    0

Test constraint owner/type unique::

    >>> set_user(cal1_user.id)
    >>> cal1_1 = Calendar()
    >>> cal1_1.name = 'cal1_1'
    >>> cal1_1.owner = resources[0]
    >>> cal1_1.type = 'freebusy'
    >>> cal1_1.save()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SQLConstraintError: ...

    >>> set_user(cal_admin.id)
    >>> calendars = Calendar.find([])
    >>> len(calendars)
    4
    >>> cal = calendars[0]
    >>> cal2 = cal.duplicate()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SQLConstraintError: ...

Cleanup all existent calendars to be able to create new calendars::

    >>> Calendar.delete(calendars)
    >>> len(Calendar.find([]))
    0

Test default read/write permissions::

    >>> set_user(cal1_user.id)
    >>> cal1_1 = Calendar()
    >>> cal1_1.name = 'cal1_1'
    >>> cal1_1.owner = resources[0]
    >>> cal1_1.type = 'freebusy'
    >>> cal1_1.save()
    >>> set_user(cal2_user.id)
    >>> len(Calendar.find([]))
    0

Test granted read permissions::

    >>> set_user(cal1_user.id)
    >>> cal1_2 = Calendar()
    >>> cal1_2.name = 'cal1_2'
    >>> cal1_2.owner = resources[0]
    >>> cal1_2.type = 'availability'
    >>> cal1_2.save()
    >>> len(Calendar.find([]))
    2
    >>> set_user(cal2_user.id)
    >>> len(Calendar.find([]))
    0
    >>> set_user(cal1_user.id)
    >>> cal1_2.read_users.append(cal2_user)
    >>> cal1_2.save()
    >>> set_user(cal2_user.id)
    >>> calendars = Calendar.find([])
    >>> len(calendars)
    1
    >>> calendars[0].name
    'cal1_2'

cal2 tries to change read-only calendar::

    >>> cal1_2.name = 'cal2'
    >>> cal1_2.save()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    AccessError: ...

Test granted write permissions::

    >>> set_user(cal1_user.id)
    >>> cal1_3 = Calendar()
    >>> cal1_3.name = 'cal1_3'
    >>> cal1_3.owner = resources[0]
    >>> cal1_3.type = 'holiday'
    >>> cal1_3.save()
    >>> len(Calendar.find([]))
    3
    >>> cal1_3.read_users.append(cal2_user)
    >>> cal1_3.save()
    >>> len(cal1_3.read_users)
    1
    >>> len(cal1_3.write_users)
    0
    >>> set_user(cal2_user.id)
    >>> len(Calendar.find([]))
    2
    >>> # proteus Bug: assert record._group is None
    >>> set_user(cal1_user.id)
    >>> cal1_3.write_users.append(cal2_user)
    >>> cal1_3.save()
    >>> len(cal1_3.write_users)
    1

    >>> set_user(cal2_user.id)
    >>> calendars = Calendar.find([])
    >>> len(calendars)
    2

cal2 succeeds in writing to write calendar::

    >>> cal1_3.name = 'cal2'
    >>> cal1_3.save()

    >>> set_user(cal1_user.id)
    >>> cal1_3.name
    'cal2'

Create resource and calendar for own party as member of calendar group::

    >>> Party = Model.get('party.party')
    >>> party = Party()
    >>> party.name = 'cal2'
    >>> party.save()

    >>> resource = Resource()
    >>> resource.email = '%s@example.com' % party.name
    >>> resource.resource = party
    >>> resource.save()
    >>> resource.rec_name
    'cal2 | cal2@example.com'

    >>> cal2_1 = Calendar()
    >>> cal2_1.name = 'cal2_1'
    >>> cal2_1.owner = resource
    >>> cal2_1.type = 'freebusy'
    >>> cal2_1.save()
    >>> cal2_1.rec_name
    'cal2_1'
