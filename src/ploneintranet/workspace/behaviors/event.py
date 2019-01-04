# coding=utf-8
from plone.app.contenttypes.interfaces import IEvent
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.multi import multiFieldWidgetFactory
from zope import schema
from zope.interface import alsoProvides


class IPloneIntranetEvent(IEvent):
    """Additional fields for PloneIntranet events
    """
    directives.widget(agenda_items=multiFieldWidgetFactory)
    agenda_items = schema.List(
        title=u"Agenda Items",
        description=u"Items associated with this event",
        required=False,
        default=[],
        value_type=schema.TextLine(title=u'Agenda item'),
    )

    organizer = schema.TextLine(
        title=u'Organizer',
        description=u'The user id of the event organizer',
        required=False,
    )

    invitees = schema.TextLine(
        title=u'Invitees',
        description=u'Members who are invited to the event',
        required=False,
    )

alsoProvides(IPloneIntranetEvent, IFormFieldProvider)
