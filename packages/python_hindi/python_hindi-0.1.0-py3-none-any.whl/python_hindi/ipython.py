import copy
import sys
from typing import Optional

from . import hook

from functools import partial


class HindiIPython:
    def __init__(self, shell):
        """
        IPython extension for writing IPython (or Jupyter) scripts in Hindi

        Args:
            shell (InteractiveShell): current IPython shell
        """
        from IPython import InteractiveShell
        # set_formatter('jupyter')
        hook.error_hook.jupyter = True

        self.ip: InteractiveShell = shell
        # old values
        self.old_showtraceback = self.ip.showtraceback
        self.old_auto_builtins = copy.copy(self.ip.builtin_trap.auto_builtins)

        hook.setup(with_excepthook=False)
        hook.error_hook.use_rich = self.isnotebook()
        hook.create_hook(False, console=False)

    def isnotebook(self):  # credit https://stackoverflow.com/a/39662359/12269724
        try:
            shell = self.ip.__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True  # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False  # Probably standard Python interpreter

    @staticmethod
    def hindi2py(lines: str) -> list:
        """
        Convert HindiPython keywords to normal Python keywords.

        Show the original and transformed if the first line starts with "# PYHI:SHOW".

        Args:
            lines: list of lines with HindiPython keywords

        Returns:
            list: list of lines with normal Python keywords

        """
        callback_params = None
        pyhi_show = False
        if lines:
            if lines[0].upper().startswith("# PYHI:SHOW"):
                pyhi_show = True
        lines = list(map(partial(hook.transform_source), lines))
        if pyhi_show:
            hook.french.print_info("Transformed", ''.join(lines))
        # return hook.transform_source('\n'.join(lines), callback_params=callback_params).split("\n")
        return lines

    def showtraceback(self, exc_tuple: Optional[tuple] = None, show_traceback=True, *args, **kwargs):  # noqa
        """
        Show the traceback on normal error

        Args:
            exc_tuple (tuple or None): (exc_type, exc_value, tb) like sys.excepthook or None for auto-detect
        """
        try:
            etype, value, tb = self.ip._get_exc_info(exc_tuple)  # noqa
        except ValueError:
            print('No traceback available to show.', file=sys.stderr)
            return
        hook.error_hook.excepthook(etype, value, tb, show_traceback=show_traceback)

    def load(self):
        """
        Load the HindiIPython extension by updating IPython shell functions and objects
        """
        # Functions to replace:
        self.ip.showtraceback = self.showtraceback
        # self.ip.showsyntaxerror = lambda *a, **k: self.showtraceback(self.ip._get_exc_info(), show_traceback=False)

        # Objects to modify:
        # self._old(self.ip.input_transformers_cleanup)
        self.ip.input_transformers_cleanup.append(self.hindi2py)
        # self._old(self.ip.user_global_ns)
        self.ip.user_global_ns.update(hook.useful_globals)
        #
        self.ip.builtin_trap.auto_builtins.update(hook.hebrew_builtins)

    def unload(self):
        self.ip.showtraceback = self.old_showtraceback
        if self.hindi2py in self.ip.input_transformers_cleanup:
            self.ip.input_transformers_cleanup.remove(self.hindi2py)
        for k in hook.useful_globals.keys():
            self.ip.user_global_ns.pop(k, None)
        self.ip.builtin_trap.auto_builtins = self.old_auto_builtins


pyhi_s = []


def load_ipython_extension(shell):
    """
    The function IPython calls on `%load_ext hindi_python`.

    Initialize HindiIPython class and load the HindiIPython extension with HindiIPython.load

    Args:
        shell (InteractiveShell): IPython shell
    """
    pyhi = HindiIPython(shell)
    pyhi.load()
    pyhi_s.append(pyhi)


def unload_ipython_extension(shell):
    """
    The function IPython calls on `%unload_ext hindi_python`.

    Unload the HindiIPython extension by HindiIPython.unload

    Args:
         shell (InteractiveShell): IPython shell

    """
    for pyhi in pyhi_s:
        pyhi.unload()
