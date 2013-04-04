import unittest
from collections import namedtuple

from applications.threaded_discussion import group


Message = namedtuple("Message", "pk parent_id body")


class ThreadedDiscussionTests(unittest.TestCase):
    def test_grouping(self):
        m1 = Message(1, None, 'hi')
        m2 = Message(2, None, 'hi')
        m3 = Message(3, 1, 'yo mate')
        m4 = Message(4, 1, 'yo too')

        raw_messages = [m1, m2, m3, m4]
        self.assertEqual(
            group(raw_messages),
            [(0, m1),
             (1, m3),
             (1, m4),
             (0, m2)]
        )
