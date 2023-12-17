import builtins
import json
import logging
import os
import sys
import importlib.util
import importlib

try:
    from friendly_traceback.console_helpers import set_formatter
except ImportError:
    set_formatter = None

from ideas import import_hook
from ideas.examples import french

from . import hindi_data  # Update to use Hindi data

try:
    from ddebug import dd
except ImportError as e:
    exc = e

    class DD:
        def call(self, *args, **kwargs):
            raise exc

        __add__ = __enter__ = __exit__ = __call__ = __and__ = __getattr__ = __getitem__ = __setitem__ = __setattr__ = call

    dd = DD()

from . import error_hook

useful_globals = {"dd": dd, 'set_formatter': set_formatter}

def set_lang(l: str):
    """
    Set hook error-friendly language.
    
    Args:
        l (str): The language (like en, fr) - it needs to be in the friendly language list in URL: https://friendly-traceback.github.io/docs/usage_adv.html#language-used
    """
    error_hook.lang = l

def transform_source(source: str, module=None, callback_params=None, **kwargs):
    """
    This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.

    Transform source from Hindi keywords to English keywords using ideas.examples.french.french_to_english.

    Args:
        source (str): Source string of the file.
        module (ModuleType): Module of source (use for __name__).
        callback_params (dict|None): Can be a dict with {show_original: bool, show_transformed: bool}.
        **kwargs: More parameters not needed for the transform.

    Returns:
        str: Source after transforming to English keywords.
    """
    if callback_params is not None:
        if callback_params["show_original"]:
            french.print_info("Original", source)
    source = french.french_to_english(source)

    if callback_params is not None:
        if callback_params["show_transformed"]:
            french.print_info("Transformed", source)

    return source

french.transform_source = transform_source
is_setup = False
hindi_builtins = {}

def setup(with_excepthook=True):
    """
    Set excepthook, load hindi_keywords.json and hindi_builtins.json to fr_to_py dict (keywords) and hindi_builtins (builtins) dict.
    """
    sys.excepthook = error_hook.excepthook
    cdir = os.path.dirname(__file__)

    str_hindi_builtins = hindi_data.hindi_builtins  # Update to use Hindi data
    french.fr_to_py = hindi_data.hindi_keywords  # Update to use Hindi data
    for k, v in str_hindi_builtins.items():
        k: str
        v: str
        if hasattr(builtins, v):
            hindi_builtins.update({k: getattr(builtins, v)})
        else:
            logging.warning(f"Cannot find key in builtins: '{v}'")

def exec_code(code, filename, globals_: dict, module, callback_params):  # noqa
    """
    Execute code with hindi_builtins + normal_builtins.

    Args:
        code (codeType): Code object for exec.
        filename: Filename to execute.
        globals_: Globals values of the code.
        module: Module of the code.
        callback_params: Callback_params with show_original and show_transformed. Not needed for this function.
    """
    globals_.update(useful_globals)
    all_builtins = module.__dict__
    all_builtins.update(hindi_builtins)

    exec(code, globals_, all_builtins)

def create_hook(run_module: bool = False, show_original: bool = False, show_transformed: bool = False,
                verbose_finder: bool = False, console: bool = (len(sys.argv) == 1)) -> import_hook.IdeasMetaFinder:
    """
    Create an import hook. Start the console with this hook if `console` is True, and run the module `run_module` if `run_module` is True and console is False.

    Args:
        run_module (bool): If sys.argv[1] exists - run the module sys.argv[1] with the hook.
        show_original (bool): Show the original source.
        show_transformed (bool): Show the transformed source.
        verbose_finder (bool): Verbose the .pyhi finder - print every search and find.
        console (bool): The default value is (True if command-line argument < 0). If this True and `run_module` is True - start repl with the hook.

    Returns :
        ideas.import_hook.IdeasMetaFinder: The hook.
    """
    if not hindi_builtins:
        setup()

    hook = import_hook.create_hook(
        transform_source=french.transform_source,
        callback_params={"show_original": show_original, "show_transformed": show_transformed},
        hook_name=__name__,
        extensions=[".pyhi"] if not console else None,
        verbose_finder=verbose_finder,
        exec_=exec_code
    )
    if run_module:
        if not console:
            if os.path.splitext(sys.argv[1])[1] == ".py":
                print("Note: You are running .py as the main script...")
                print("Extension ko .pyhi mein badaliye")
                exit(1)

            module = None
            if os.path.exists(sys.argv[1]):
                module = os.path.splitext(sys.argv[1])[0]
            elif os.path.exists(sys.argv[1] + ".pyhi"):
                module = sys.argv[1]
            if not module:
                print("File not found:", sys.argv[1])
                print(sys.argv[1], "File nahi mila")
                exit()
        else:
            from ideas import console

            def runcode(self, code):
                try:
                    exec_code(code, "<stdin>", {}, builtins, {})
                except SystemExit:
                    os._exit(1)  # noqa
                except Exception:
                    self.showtraceback()

            console.IdeasConsole.runcode = runcode
            console.start()
            return hook

        sys.path.append(os.path.dirname(module))
        importlib.import_module(module)

    return hook
