"""ytho - Change your REPL prompt."""
from __future__ import annotations
from typing import Protocol

import ast
import code
import importlib.util
import os
import site
import sys
from contextlib import suppress
from functools import lru_cache


YTHO_PROMPT_FILE = os.path.expanduser("~/.ytho.py")


class Prompter(Protocol):
    def prompt(self) -> tuple[str, str]:
        ...


@lru_cache(maxsize=1)
def find_custom_prompt() -> Prompter | None:
    if os.path.exists(YTHO_PROMPT_FILE):
        spec = importlib.util.spec_from_file_location(".ytho.py", YTHO_PROMPT_FILE)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        assert module is not None
        spec.loader.exec_module(module)

        if hasattr(module, "Prompt") and isinstance(module.Prompt, type):
            prompter: Prompter = module.Prompt()
            return prompter

    return None


class YthoPrompt(code.InteractiveConsole):
    def __init__(self, prompter: Prompter) -> None:
        super().__init__()
        self.prompter = prompter
        sys.ps1, sys.ps2 = self.prompter.prompt()

    def runsource(
        self,
        source: str,
        filename: str = "<console>",
        symbol: str = "single",
    ) -> bool:
        # First, check if it could be incomplete input, return True if it is.
        # This will allow it to keep taking input
        with suppress(SyntaxError, OverflowError):
            if code.compile_command(source) == None:
                return True

        try:
            # Change the prompt
            sys.ps1, sys.ps2 = self.prompter.prompt()
        
            # Now compile statement as normal.
            tree = ast.parse(source, filename, mode=symbol)
            assert isinstance(tree, ast.Interactive)
            code_obj = compile(tree, filename, mode=symbol)
        except (ValueError, SyntaxError):
            # Let the original implementation take care of incomplete input / errors
            return super().runsource(source, filename, symbol)

        self.runcode(code_obj)
        return False


def register() -> None:
    is_in_repl = sys.argv[0] == ''
    if not is_in_repl:
        # We only want to start our prompt if we are in interactive_mode.
        return

    prompter = find_custom_prompt()
    if prompter is not None:
        prompt = YthoPrompt(prompter)

        # Copied from code.py
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'

        default_banner = f"{sys.version} on {sys.platform}\n{cprt}"

        # TODO: do the other things that site.main() does
        site.setquit()
        site.setcopyright()
        site.sethelper()
        # For tab completion and arrow key support
        if sys.platform != "win32":
            import readline
        
            readline.parse_and_bind("tab: complete")

        prompt.interact(banner=default_banner, exitmsg="")
        os._exit(0)
    else:
        # Simply change the PS1 for now. Maybe remove this code later.
        sys.ps1 = r"¯\_(ツ)_/¯> "
        sys.ps2 = "........... "
