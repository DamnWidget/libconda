from hashlib import md5

import sublime

from .render import Renderable
from .packages.typing import Tuple


class Tpl(Renderable):
    """Base template class for any renderable template
    """

    def __init__(self, tpl_data) -> None:
        for key, value in tpl_data.items():
            setattr(self, key, value)

        super(Tpl, self).__init__()


class Template:
    """Load Jinja2 template files from ST3 packages
    """

    def __init__(self, name: str, *components: Tuple[str]) -> None:
        self.name = name
        self.content = None  # type: str
        self.ready = False
        self.md5sum = None  # type: int
        self.components = components

    @property
    def filename(self) -> str:
        """Retuns back the complete filename
        """

        return '{}.jinja'.format(self.name)

    @property
    def canonical_path(self) -> str:
        """Returns back the canonical file path
        """

        if not self.components:
            self.components = (
                'libconda', 'st3', 'libconda', 'ui', 'templates'
            )

        path = 'Packages/{}'.format('/'.join(self.components))
        return '{}/{}'.format(path, self.filename)

    @property
    def modified(self) -> bool:
        """Checks if the template content has been modified since it's load
        """

        md5sum = md5(sublime.load_resource(self.canonical_path).encode('utf8'))
        return int(md5sum.hexdigest(), 16) != self.md5sum

    def load(self) -> None:
        """Load the template file if necessary
        """

        if not self.ready or self.modified:
            tpl_contents = sublime.load_resource(self.canonical_path)
            self.md5sum = int(md5(tpl_contents.encode('utf8')).hexdigest(), 16)
            self.content = ''.join(
                s.strip() for s in tpl_contents.splitlines()
            )
            if not self.ready:
                self.ready = True
