# -*- coding: utf-8 -*-

from plone import api
from plone.app.testing import TEST_USER_ID
from ploneintranet.workspace.tests.base import BaseTestCase
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import zope.event


class TestTodos(BaseTestCase):
    """Test Todo items in Case Workspaces"""

    def setUp(self):
        self.portal = self.layer['portal']
        self.workspaces = api.content.create(
            type='ploneintranet.workspace.workspacecontainer',
            title='workspaces',
            container=self.portal,
        )
        self.case = api.content.create(
            type='ploneintranet.workspace.case',
            title='case',
            container=self.workspaces,
        )
        api.content.transition(self.case, 'transfer_to_department')

    def test_todo_reopen_earlier_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_reopen_current_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='in_progress',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_reopen_future_milestone(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='archived',
        )
        api.content.transition(case_todo, 'finish')
        case_todo.reopen()
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_todo_initial_state_open(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_initial_state_planned(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='complete',
        )
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_todo_update_state_to_open(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='archived',
        )
        case_todo.milestone = 'new'
        notify(ObjectModifiedEvent(case_todo))
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'open',
        )

    def test_todo_update_state_to_planned(self):
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=self.case,
            milestone='new',
        )
        case_todo.milestone = 'archived'
        notify(ObjectModifiedEvent(case_todo))
        self.assertEquals(
            self.portal.portal_workflow.getInfoFor(case_todo, 'review_state'),
            'planned',
        )

    def test_update_todo_state_when_case_state_is_changed(self):
        case2 = api.content.create(
            type='ploneintranet.workspace.case',
            title='case',
            container=self.workspaces,
        )
        case_todo = api.content.create(
            type='todo',
            title='case_todo',
            container=case2,
            milestone='in_progress',
        )
        wft = self.portal.portal_workflow
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'planned')
        api.content.transition(case2, 'transfer_to_department')
        self.assertEquals(wft.getInfoFor(case_todo, 'review_state'), 'open')