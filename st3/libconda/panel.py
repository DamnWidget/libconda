import webbrowser

import sublime
import mdpopups

from .template import Tpl, Template
from .packages.typing import Dict, Any, Union, List, Callable

NavigationHandler = Dict[str, Callable]


class GolcondaPanelTpl(Tpl):
    """Base template class for panel templates
    """

    _tpl = Template('golconda_panel')


class GolcondaPanel:
    """Features an HTML rich bottom panel using phantoms
    """

    _style = None
    _id = 'golconda_bottom_panel'

    def __init__(self, content: Dict[str, Any]) -> None:
        self.navigation_handlers = {}  # type: Dict[str, Callable]
        self._enable_syntax_highlighter()
        self._load_style()
        self._add_handlers()
        self._initialize_output_panel()
        self.header = content.get('header', '')
        self.body = content.get('body', '')
        self.footer = content.get('footer', '')

    @classmethod
    def _load_style(cls):
        """Load CSS style
        """

        if cls.__name__ != 'GolcondaPanel':
            raise NotImplementedError(
                'you must provide your own _load_style method when '
                'subclassing GolcondaPanel'
            )

        stylename = '{}.css'.format(cls.__name__.lower())
        cls._style = sublime.load_resource(
            '/'.join(['Packages/libconda/st3/libconda/ui/styles', stylename])
        )

    @property
    def frontmatter(self) -> Dict[str, Union[bool, List[Union[str, Dict[str, Any]]]]]:  # noqa
        """Returns configured mdpopups frontmatter
        """

        return {
            "allow_code_wrap": True,
            "markdown_extensions": [
                "markdown.extensions.admonition",
                "markdown.extensions.attr_list",
                "markdown.extensions.def_list",
                "markdown.extensions.nl2br",
                # Smart quotes always have corner cases that annoy me,
                # so don't bother with them.
                {"markdown.extensions.smarty": {"smart_quotes": False}},
                "pymdownx.extrarawhtml",
                "pymdownx.keys",
                {"pymdownx.escapeall": {"hardbreak": True, "nbsp": False}},
                # Sublime doesn't support superscript, so no ordinal numbers
                {"pymdownx.smartsymbols": {"ordinal_numbers": False}}
            ]
        }

    def add_handler(self, url: str, handler: Callable) -> None:
        """Add the given handler for the given url for navigation
        """

        if not callable(handler):
            raise RuntimeError(
                'handler {} is not callable'.format(handler.__name__)
            )

        self.navigation_handlers[url] = handler

    def render(self) -> str:
        """Renders the panel as HTML output into a phantom
        """

        tpl_content = {
            'header': self.header,
            'body': self.body,
            'footer': self.footer
        }
        tpl = GolcondaPanelTpl(tpl_content)
        return tpl.render()

    def show(self) -> None:
        """Shows the rendered panel
        """

        self.panel.show(0)
        sublime.active_window().run_command(
            'show_panel', {'panel': 'output.{}'.format(self._id)}
        )

    def update(self) -> None:
        """Update an existing panel re-rendering it with new contents
        """

        self.remove_phantom(self._id)
        self.inject_phantom(self.render())

    def remove_phantom(self, key: str) -> None:
        """Removes the phantom identified by the giveb key from the panel
        """

        mdpopups.erase_phantoms(self.panel, key)

    def inject_phantom(self, content: str=None) -> str:
        """Injects a phantom with the given content and returns it's ID/Key
        """

        if not content:
            content = self.render()

        content = mdpopups.format_frontmatter(self.frontmatter) + content
        self.remove_phantom(self._id)
        mdpopups.clear_cache()
        return mdpopups.add_phantom(
            self.panel,
            self._id,
            sublime.Region(0),
            content,
            sublime.LAYOUT_INLINE,
            on_navigate=self.on_navigate,
            wrapper_class='libconda_panel',
            css=self._style,
            md=False
        )

    def on_navigate(self, url: str) -> None:
        """Sublime Text calls this method when the user clicks a link
        """

        url, handler_key = url.split(':', 1)
        handler = self.navigation_handlers.get(handler_key)
        if handler is None:
            raise RuntimeError('unknown handler {}'.format(url))

        if not callable(handler):
            raise RuntimeError(
                'handler {} is not callable'.format(handler.__name__)
            )

        handler(url)

    def _initialize_output_panel(self) -> None:
        """Initializes the Sublime Text output panel that is going to be used
        """

        window = sublime.active_window()
        panel = window.create_output_panel(self._id)
        panel.settings().set('line_numbers', False)
        panel.settings().set('gutter', False)
        panel.settings().set('scroll_past_end', False)
        panel.set_read_only(True)

        self.panel = panel
        window.create_output_panel(self._id)

    def _add_handlers(self):
        """Add common handlers for golconda panels
        """

        self.add_handler('link', lambda url: webbrowser.open_new_tab(url[5:]))

    def _enable_syntax_highlighter(self):
        """Enable the syntax highlighter for mdpopups
        """

        s = sublime.load_settings('Preferences.sublime-settings')
        if not s.get('mdpopups.use_sublime_highlighter'):
            s.set('mdpopups.use_sublime_highlighter', True)
