"""Petit lanceur Textual pour exécuter les scripts Python de `helpers`.

Usage:
    python helpers/tools_menu.py
"""

from __future__ import annotations

import asyncio
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, ListItem, ListView, RichLog, Static
from text_clean import clean_multiline, clean_text


class HelpersToolboxApp(App):
    TITLE = "Helpers Toolbox"
    SUB_TITLE = "Lanceur de scripts Python"

    CSS = """
    Screen {
        layout: vertical;
    }

    #body {
        height: 1fr;
    }

    #left-pane {
        width: 35%;
        border: solid $primary;
        padding: 0 1;
    }

    #right-pane {
        width: 65%;
        border: solid $accent;
        padding: 0 1;
    }

    #scripts {
        height: 1fr;
    }

    #details {
        margin-top: 1;
        color: $text-muted;
        height: auto;
    }

    #controls {
        height: auto;
        margin-bottom: 1;
    }

    #args {
        margin-top: 1;
        margin-bottom: 1;
    }

    #run {
        margin-right: 1;
    }

    #status {
        margin-top: 1;
        color: $text-muted;
    }

    #output {
        height: 1fr;
        border: solid $panel;
    }
    #copy {
        margin-left: 30;
    }
    """

    BINDINGS = [
        ("r", "run_script", "Run"),
        ("s", "stop_script", "Stop"),
        ("c", "copy_output", "Copy"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.helpers_dir = Path(__file__).resolve().parent
        self.current_file = Path(__file__).resolve()
        self.scripts = self._discover_scripts()
        self.selected_script: Path | None = None
        self.selected_index: int | None = None
        self.process: asyncio.subprocess.Process | None = None
        self.last_stdout: str = ""

    def _discover_scripts(self) -> list[Path]:
        scripts = sorted(
            path
            for path in self.helpers_dir.rglob("*.py")
            if path.resolve() != self.current_file and "__pycache__" not in path.parts
        )
        return scripts

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="body"):
            with Vertical(id="left-pane"):
                yield Label("Scripts disponibles")
                yield ListView(
                    *(ListItem(Label(str(script.relative_to(self.helpers_dir)))) for script in self.scripts),
                    id="scripts",
                )
                yield Static(self._selected_details_text(), id="details")
            with Vertical(id="right-pane"):
                with Horizontal(id="controls"):
                    yield Button("Executer (r)", id="run", variant="success")
                    yield Button("Stop (s)", id="stop", variant="error")
                    yield Button("Copier stdout (c)", id="copy", variant="primary", classes="copy-button")
                yield Input(
                    placeholder='Arguments (ex: question 123 ou chercher "bonjour le monde")',
                    id="args",
                )
                yield Static("Pret.", id="status")
                yield RichLog(id="output", wrap=True, markup=False, auto_scroll=True)
        yield Footer()

    def on_mount(self) -> None:
        scripts_widget = self.query_one("#scripts", ListView)
        if self.scripts:
            scripts_widget.index = 0
            self._update_selection_from_index(0)
        else:
            self.query_one("#status", Static).update("Aucun script Python trouve dans helpers.")
            self.query_one("#run", Button).disabled = True
        self._set_running_state(False)

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.id == "scripts":
            self._update_selection_from_index(event.list_view.index)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "scripts":
            self._update_selection_from_index(event.list_view.index)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self.action_run_script()
        elif event.button.id == "stop":
            self.action_stop_script()
        elif event.button.id == "copy":
            self.action_copy_output()

    def _selected_details_text(self) -> str:
        if not self.selected_script:
            return "Selection: (aucune)"
        rel = self.selected_script.relative_to(self.helpers_dir)
        return f"Selection: {rel}\nChemin: {self.selected_script}"

    def _update_selection_from_index(self, index: int | None) -> None:
        if index is None:
            return
        if index < 0 or index >= len(self.scripts):
            return
        if self.selected_index == index:
            return
        self.selected_index = index
        self.selected_script = self.scripts[index]

        # nettoyage du terminal
        self.query_one("#details", Static).update(self._selected_details_text())
        self.query_one("#output", RichLog).clear()
        self.query_one("#status", Static).update("Apercu: execution sans arguments...")

        # nettoyage du champ de saisie des arguments
        self.query_one("#args", Input).value = ""
        
        self._run_selected_script_with_args([])

    def _parse_args(self, args_text: str) -> list[str]:
        if not args_text.strip():
            return []
        # Utilise toujours le mode POSIX pour que les guillemets servent bien
        # a regrouper les arguments multi-mots sur toutes les plateformes.
        return shlex.split(args_text, posix=True)

    def _format_command(self, command: list[str]) -> str:
        if os.name == "nt":
            return subprocess.list2cmdline(command)
        return shlex.join(command)

    def _set_running_state(self, running: bool) -> None:
        self.query_one("#run", Button).disabled = running
        self.query_one("#stop", Button).disabled = not running
        self.query_one("#copy", Button).disabled = running or not self.last_stdout

    def _run_selected_script_with_args(self, script_args: list[str]) -> None:
        if not self.selected_script:
            self.query_one("#status", Static).update("Aucun script selectionne.")
            return
        if self.process and self.process.returncode is None:
            self.query_one("#status", Static).update("Un script est deja en cours. Stoppe-le avant d'en lancer un autre.")
            return
        self.run_worker(
            self._run_selected_script(script_args),
            group="script-runner",
            exclusive=True,
            exit_on_error=False,
        )

    def action_run_script(self) -> None:
        args_input = self.query_one("#args", Input)
        try:
            script_args = self._parse_args(args_input.value)
        except ValueError as exc:
            self.query_one("#status", Static).update(f"Arguments invalides: {exc}")
            return
        self._run_selected_script_with_args(script_args)

    def action_stop_script(self) -> None:
        if self.process and self.process.returncode is None:
            self.process.terminate()
            self.query_one("#status", Static).update("Arret du script en cours...")
        else:
            self.query_one("#status", Static).update("Aucun script en cours.")

    def action_copy_output(self) -> None:
        if not self.last_stdout:
            self.query_one("#status", Static).update("Rien a copier: aucune sortie standard disponible.")
            return
        try:
            cleaned = clean_multiline(self.last_stdout).rstrip("\n")
            self._copy_to_clipboard(cleaned)
            self.query_one("#status", Static).update("Sortie standard copiee dans le presse-papiers.")
        except Exception as exc:  # pragma: no cover - depend des outils systeme
            self.query_one("#status", Static).update(f"Impossible de copier: {exc}")

    def _copy_to_clipboard(self, content: str) -> None:
        if os.name == "nt":
            subprocess.run(["clip"], input=content, text=True, encoding="utf-8", check=True)
            return
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=content, text=True, check=True)
            return

        if shutil.which("wl-copy"):
            subprocess.run(["wl-copy"], input=content, text=True, check=True)
            return
        if shutil.which("xclip"):
            subprocess.run(["xclip", "-selection", "clipboard"], input=content, text=True, check=True)
            return
        raise RuntimeError("Aucun utilitaire de presse-papiers detecte (clip/pbcopy/wl-copy/xclip).")

    async def _run_selected_script(self, script_args: list[str]) -> None:
        output = self.query_one("#output", RichLog)
        status = self.query_one("#status", Static)

        command = [sys.executable, str(self.selected_script), *script_args]
        output.clear()
        output.write(f"$ {self._format_command(command)}")
        self.last_stdout = ""
        status.update("Execution en cours...")
        self._set_running_state(True)

        try:
            self.process = await asyncio.create_subprocess_exec(
                *command,
                cwd=str(self.selected_script.parent),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            assert self.process.stdout is not None
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                text = clean_text(line.decode("utf-8", errors="replace").rstrip("\n"))
                self.last_stdout += text + "\n"
                output.write(text)

            return_code = await self.process.wait()
            if return_code == 0:
                status.update("Execution terminee (code 0).")
            else:
                status.update(f"Execution terminee avec erreur (code {return_code}).")
        except asyncio.CancelledError:
            if self.process and self.process.returncode is None:
                self.process.terminate()
            status.update("Execution annulee.")
            raise
        except ProcessLookupError:
            status.update("Processus introuvable au moment de l'arret.")
        except Exception as exc:  # pragma: no cover - securite runtime
            status.update(f"Erreur inattendue: {exc}")
        finally:
            self.process = None
            self._set_running_state(False)


if __name__ == "__main__":
    HelpersToolboxApp().run()
