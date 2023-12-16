try:
    import friendly_traceback.core as friendly_core
    import friendly_traceback
except ImportError:
    friendly_core = None
    friendly_traceback = None

import rich.panel
import rich.traceback
import rich.markdown
import sys

# lang = "hi" TODO
lang = "hi"
jupyter = False
use_rich = False

excepthook_no_friendly = sys.excepthook

def excepthook_friendly(exc_type, exc_value, tb, show_traceback=True):
    friendly_traceback.set_lang(lang)
    if jupyter:
        import IPython.display
        import IPython.core.ultratb
    else:
        IPython = None
    # load friendly
    fr = friendly_core.FriendlyTraceback(exc_type, exc_value, tb)
    fr.compile_info()
    # print traceback
    if IPython:
        ip = IPython.get_ipython()
        ###########
        if show_traceback:
            stb = ip.InteractiveTB.structured_traceback(exc_type,
                                                        exc_value, tb)

            ip._showtraceback(exc_type, exc_value, stb)
        ###############
    else:
        if show_traceback:
            print(fr.info["shortened_traceback"], file=sys.stderr)
    # get info from friendly
    generic = fr.info.get("generic", '')
    cause = fr.info.get("cause", '')
    suggest = fr.info.get("suggest", '')
    if suggest:
        suggest = "\n" + suggest

    # build Panel (or display Markdown for ipython)
    string = f'{generic}\n{suggest}\n{cause}'
    if IPython and use_rich:
        IPython.display.display(IPython.display.Markdown(string))

    else:
        trace = rich.panel.Panel(rich.markdown.Markdown(string),
                                 title="[traceback.title] Friendly Explanation [dim](Usually boring Python traceback ke baad):\n",
                                 expand=False,
                                 padding=(0, 1))

        rich.get_console().print(trace)

if friendly_traceback:
    excepthook = excepthook_friendly
else:
    excepthook = excepthook_no_friendly
