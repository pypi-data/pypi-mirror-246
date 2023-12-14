"""Text color changer for Sphinx."""
from docutils import nodes
from docutils.writers import Writer
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.util.docutils import SphinxRole

__version__ = "0.1.1"

COLORS = {
    "black": "#000000",
    "silver": "#c0c0c0",
    "gray": "#808080",
    "white": "#ffffff",
    "maroon": "#800000",
    "red": "#ff0000",
    "purple": "#800080",
    "fuchsia": "#ff00ff",
    "green": "#008000",
    "lime": "#00ff00",
    "olive": "#808000",
    "yellow": "#ffff00",
    "navy": "#000080",
    "blue": "#0000ff",
    "teal": "#008080",
    "aqua": "#00ffff",
}
"""Major named-colors.

Use "Standard colors" from
 `MDN <https://developer.mozilla.org/en-US/docs/Web/CSS/named-color>`_.
"""


class ColorRole(SphinxRole):  # noqa: D101
    def __init__(self, color_code: str):  # noqa: D107
        self._color_code = color_code

    def run(self):  # noqa: D102
        messages = []
        node = ColorText(self.rawtext, self.text)
        node["style"] = f"color: {self._color_code}"
        return [node], messages


class ColorDomain(Domain):  # noqa: D101
    name = "color"
    label = "Color text"
    roles = {k: ColorRole(v) for k, v in COLORS.items()}


class ColorText(nodes.Inline, nodes.TextElement):  # noqa: D101
    pass


def visit_color_text(self: Writer, node: ColorText):  # noqa: D103
    self.body.append(self.starttag(node, "span", "", style=node["style"]))


def depart_color_text(self: Writer, node: ColorText):  # noqa: D103
    self.body.append("</span>")


def setup(app: Sphinx):  # noqa: D103
    app.add_domain(ColorDomain)
    app.add_node(ColorText, html=(visit_color_text, depart_color_text))
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
