import unittest

from libconda.render import Renderable


class TestRenderable(unittest.TestCase):
    """Tests Renderable functionality
    """

    def test_render(self):
        sut = Tpl()
        self.assertEqual(sut.render(), 'Hello Subject Under Test!')

        sut.name = 'World'
        self.assertEqual(sut.render(), 'Hello World!')


class Stub:
    content = 'Hello {{ data.name }}!'

    def load(self):
        pass


class Tpl(Renderable):
    _tpl = Stub()
    name = 'Subject Under Test'
