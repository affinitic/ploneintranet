import unittest2 as unittest

from ploneintranet.pagerank.graph import Graphs
from ploneintranet.pagerank.testing import\
    PLONEINTRANET_PAGERANK_INTEGRATION

from ploneintranet.pagerank import testing_config as config


class TestGraph(unittest.TestCase):

    layer = PLONEINTRANET_PAGERANK_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.graphs = Graphs()

    def test_social_following(self):
        """Get the social graph from plonesocial.network
        """
        self.assertEqual(set(self.graphs.social_following().edges()),
                         config.SOCIAL_GRAPH)

    def test_content_tree(self):
        """Get the object containment tree
        """
        self.assertEqual(
            set(self.graphs.content_tree().edges()),
            set([('path:/plone/public', 'path:/plone/public/d1'),
                 ('path:/plone/public/d1', 'path:/plone/public')]))

    def test_content_authors(self):
        """Get the object authorships
        """
        self.assertEqual(
            set(self.graphs.content_authors().edges()),
            set([('path:/plone/public', 'user:admin'),
                 ('path:/plone/public/d1', 'user:admin'),
                 ('user:admin', 'path:/plone/public'),
                 ('user:admin', 'path:/plone/public/d1')]))

    def test_content_tags(self):
        """Get the object authorships
        """
        self.assertEqual(set(self.graphs.content_tags().edges()),
                         config.CONTENT_TAGS)
