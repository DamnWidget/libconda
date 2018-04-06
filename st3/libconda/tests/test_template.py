import os
import unittest
from unittest.mock import Mock, patch


class TestTemplate(unittest.TestCase):
    """Tests Template class
    """

    def setUp(self):
        self.sublime = Mock()
        self.sublime.load_resource = self._mock_sublime_load_resource

    def test_template(self):
        # patch sys.modules
        with patch.dict('sys.modules', sublime=self.sublime):
            from libconda.template import Template

            sut = Template('subject_under_test')
            self.assertEqual(sut.name, 'subject_under_test')
            self.assertFalse(sut.components)
            self.assertEqual(sut.filename, 'subject_under_test.jinja')
            self.assertEqual(
                sut.canonical_path,
                'Packages/libconda/st3/libconda/ui/templates/{}.jinja'.format(
                    'subject_under_test'
                )
            )
            self.assertIsNone(sut.content)
            self.assertFalse(sut.ready)

            sut.load()
            self.assertTrue(sut.ready)
            expected = ''.join(
                s.strip()
                for s in self._mock_sublime_load_resource('').splitlines()
            )
            self.assertEqual(sut.content, expected)
            self.assertFalse(sut.modified)

            self.sublime.load_resource = (
                lambda p: self._mock_sublime_load_resource(None, True)
            )
            self.assertTrue(sut.modified)

            sut.load()
            expected += 'EOF'
            self.assertEqual(sut.content, expected)

    def _mock_sublime_load_resource(self, path, modified=False):
        """Mocks the sublime.load_resource function
        """

        path = os.path.join(
            os.path.dirname(__file__),
            '..', 'ui', 'templates', 'golconda_panel.jinja'
        )

        with open(path) as f:
            if not modified:
                return f.read()

            return f.read() + 'EOF'
