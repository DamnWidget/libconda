import os
import unittest
from unittest.mock import patch, Mock


class TestGolcondaPanel(unittest.TestCase):
    """Tests GolcondaPanel class
    """

    def setUp(self):
        self.content = (
            '<div class="container">'
            'This is the header'
            'This is the body'
            'This is the footer'
            '</div>'
        )

        self.webbrowser = Mock()
        self.window = Mock()
        self.sublime = Mock()
        self.mdpopups = Mock()
        self.test_handler = Mock()

        self.window.create_output_panel.return_value = Mock()
        self.sublime.LAYOUT_INLINE = 10
        self.sublime.load_resource = self._mock_sublime_load_resource
        self.sublime.active_window.return_value = self.window
        self.mdpopups.format_frontmatter.return_value = ''

    def test_golconda_panel(self):
        with patch.dict(
            'sys.modules',
            sublime=self.sublime,
            mdpopups=self.mdpopups,
            webbrowser=self.webbrowser
        ):
            from libconda.panel import GolcondaPanel
            from libconda.panel import NoTcallableHandler, UnknownHandler

            content = {
                'header': 'This is the header',
                'body': 'This is the body',
                'footer': 'This is the footer'
            }
            sut = GolcondaPanel(content)
            self.assertEqual(sut._style, 'body {}')
            self.assertEqual(sut.header, 'This is the header')
            self.assertEqual(sut.body, 'This is the body')
            self.assertEqual(sut.footer, 'This is the footer')

            self.sublime.active_window.assert_called_once()
            self.window.create_output_panel.assert_called_with(sut._id)
            self.assertEqual(sut.panel.settings.call_count, 3)

            self.assertEqual(len(sut.navigation_handlers), 1)
            self.assertTrue('link' in sut.navigation_handlers)

            self.assertEqual(sut.render(), self.content)

            sut.inject_phantom(self.content)
            self.mdpopups.format_frontmatter.assert_called_once_with(
                sut.frontmatter
            )
            self.mdpopups.erase_phantoms.assert_called_once_with(
                sut.panel, sut._id
            )
            self.mdpopups.clear_cache.assert_called_once()
            _, args, kwargs = self.mdpopups.add_phantom.mock_calls[0]
            self.assertEqual(args[0], sut.panel)
            self.assertEqual(args[1], sut._id)
            self.assertEqual(args[3], self.content)
            self.assertEqual(args[4], 10)
            self.assertEqual(kwargs['on_navigate'], sut.on_navigate)
            self.assertEqual(kwargs['wrapper_class'], 'libconda_panel')
            self.assertEqual(kwargs['css'], 'body {}')
            self.assertEqual(kwargs['md'], False)

            sut.on_navigate('link:http://www.google.com')
            self.webbrowser.open_new_tab.assert_called_once_with(
                'http://www.google.com'
            )

            sut.add_handler('test', self.test_handler)
            sut.on_navigate('test:this_is_the_url_part')
            self.test_handler.assert_called_once_with('this_is_the_url_part')
            sut.add_handler('test_colons', self.test_handler)
            self.assertTrue('test_colons' in sut.navigation_handlers)
            sut.on_navigate('test_colons:test:with:colons')
            self.test_handler.assert_called_with('test:with:colons')

            self.assertRaises(UnknownHandler, sut.on_navigate, 'no_hanlder:0')
            self.assertRaises(
                NoTcallableHandler, sut.add_handler, '0', 'NotCallable'
            )
            sut.navigation_handlers['not_callable'] = 'NotCallable'
            self.assertRaises(
                NoTcallableHandler, sut.on_navigate, 'not_callable:0'
            )

            sut.show()
            sut.panel.show.assert_called_once_with(0)

    def _mock_sublime_load_resource(self, path):
        """Mocks the sublime.load_resource function
        """

        if 'css' in path:
            return 'body {}'

        path = os.path.join(
            os.path.dirname(__file__),
            '..', 'ui', 'templates', 'golconda_panel.jinja'
        )

        with open(path) as f:
            return f.read()
