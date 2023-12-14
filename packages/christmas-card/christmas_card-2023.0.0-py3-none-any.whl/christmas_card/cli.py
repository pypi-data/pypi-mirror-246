from pathlib import Path

import cryptography.fernet
import rich
import typer
from rich.console import Console, RenderableType
from rich_pixels import Pixels
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widget import Widget
from textual.widgets import Markdown
from rich import emoji
from .encrypt import decrypt
from rich.markdown import Markdown as RichMarkdown
console = Console()

CSS = """
Screen {
    layout: grid;
    grid-size: 3;
    grid-columns: 30% 40% 30%;
}

.box {
    height: 100%;
    content-align: center middle;
}

.center-box {
    height: 100%;
    content-align: center middle;
    
    text-align: center;
    align: center middle;
}

.inner-box {
    height: 40%;
}

MarkdownH1 {
    background: rgb(255,204,203);
    border: wide $background;
    content-align: center middle;

    padding: 1;
    text-style: bold;
    color: $text;
}

MarkdownBlock {
    text-align: center;
}
"""

IMAGE_DIRECTORY = Path(__file__).parent / "images"


class ImageView(Widget):
    def __init__(self, image_name: str, **kwargs):
        self.image_name = image_name
        super().__init__(**kwargs)

    def render(self) -> RenderableType:
        height = self.window_region.height // 2
        width = self.window_region.width // 2
        return Pixels.from_image_path(IMAGE_DIRECTORY / self.image_name, resize=(width, height))


class MyApp(App):
    CSS = CSS

    def __init__(self, markdown_card: str, *args, **kwargs):
        self.markdown_card = markdown_card
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield ImageView('fireplace.png', classes="box")
        markdown = Markdown(self.markdown_card, classes="inner-box")
        yield Center(markdown, classes="center-box")
        yield ImageView('santa.png', classes="box")


def main():
    rich.print(
        RichMarkdown("# ⚠️  This card is encrypted ⚠️\n\nEnter the password given to you to continue")
    )
    card = Path(__file__).parent / "encrypted_card.md"

    passphrase = typer.prompt("Enter passphrase", hide_input=False)
    try:
        markdown_card_contents = decrypt(card, passphrase.encode())
    except cryptography.fernet.InvalidToken as e:
        rich.print("\nIncorrect passphrase!")
        return

    markdown_card = emoji.Emoji.replace(markdown_card_contents)
    app = MyApp(markdown_card)
    app.run()


if __name__ == "__main__":
    typer.run(main)
