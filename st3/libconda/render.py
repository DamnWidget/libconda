from jinja2 import Template


class Renderable:
    """Provides it's subclasses with capacity to render themselves
    """

    def __init__(self) -> None:
        self._tpl.load()  # type: ignore

    def render(self):
        """Render the renderable using it's template contents
        """

        return Template(self._tpl.content).render(data=self)
