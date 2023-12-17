# python_hindi

python_hindi is a Python library (with command-line utilities) for programming Python in Hindi.
(Haan, Bhai possible hai!)

python_hindi runs in Python 3.6+

After downloading this library, you can write a script like:

```
# if-else

sankhya = poornank(niwesh("Ek sankhya daalein: "))
yadi (sankhya % 2) == 0:
    bol("{0} sam hai".format(sankhya))
anyatha:
    bol("{0} visam hai".format(sankhya))
```

```
# while loop

num = 0
jabtak num < 10:
    num += 1
    yadi (num % 2) == 0:
        jaari
    bol(num)
```

```
#for loop

languages = ['Swift', 'Python', 'Go', 'JavaScript']
pratyek language mein languages:
    bol(language)
```

Name the file `kuchbhi.pyhi` and run it with `pyhi kuchbhi.pyhi`.

You can also import other `.pyhi` and `.py` files from the main file:

```
aayat kuchbhi
```

## Installing

To install with pip, type in the terminal:

and for non-errors support :

```
pip install python-hindi
```

This will create the command-line script: `pyhi`

## Usage

You can run pyhi files with `pyhi <file>`

You can start the Hindi Python console with just `pyhi`

Example:

```
pyhi file.pyhi

```

## `.pyhi` file syntax

`.pyhi` file supports Hindi Python syntax (syntax with keywords like `aayat` (import)  
and functions like `bol` (print))
in addition to normal Python syntax.

## Use from normal Python file/repl

You can use it as a library:

To import `.pyhi` files into your `.py` file:

```
from python_hindi import create_hook
create_hook(run_module=False, console=False) # without running the main module or starting the repl
import pyhi_module # now you can import .pyhi files
```

Or to start the REPL from the normal REPL:

```
from python_hindi import create_hook
create_hook(run_module=True, console=True) # *with* starting the repl
```

## jupyter/ipython

`python-hindi` supports [jupyter](https://jupyter.org) and [ipython](https://ipython.org/) interactive console by IPython extension. To use:

Install Jupyter Notebook by: `pip install notebook`  
Start Jupyter Notebook by: `jupyter notebook`.
Then create a new Python 3 by the new button.

In the first cell, enter the text `%load_ext python_hindi` and press `Ctrl + Enter`.

Now you can write Hindi Python in the entire notebook.

## Dependencies

python-hindi depends on the Python libraries:

- [friendly](https://github.com/aroberge/friendly) - for more friendly Hinglish(hindi in roman script) traceback

- [ideas](https://github.com/aroberge/ideas) - most of this library is built on this project. It supports easy creation of import hooks and it has a [simple example](https://github.com/aroberge/ideas/blob/master/ideas/examples/french.py) for replacing keywords with French keywords

- [rich] - rich is a Python library for rich text and beautiful formatting in the terminal.

## Contribute

For all errors, problems, or suggestions, please open a [GitHub issue](https://github.com/itsrealkaran/python_hindi/issues)

## Author

Karan Singh

## License

This project is licensed under the [BSD-4 License](https://github.com/itsrealkaran/python_hindi/blob/main/LICENSE).
