# functions:
hindi_builtins = {
    # numbers
    "mul": "abs",
    "sab": "all",
    "koi": "any",  

    # list
    "lambai": "len",
    "kam": "min", #nyuntam
    "zyada": "max", #adhiktam
    "ulta": 'reversed',
    "ganana":"enumerate",
    "manchitra":"map",

    # std
    "bol": "print",
    "niwesh": "input",

    # errors
    "AayatTruti": "ImportError",
    "NaamTruti": "NameError",
    "AnumatiTruti": "PermissionError",
    "Apavad":"Exception",
    "FileNahiMili":"FileNotFoundError",
    

    # strings
    'prat': 'repr',
    "chalao": "exec",
    "kholo":"open"
}

# keywords:
hindi_keywords = {
    "banao":
    "hindi_python",  # TODO : I want to create another module for this.

    # if and booleans:
    "yadi": "if",
    "satya": "True",
    "mithya": "False",
    "aur": "and",
    "nahi": "not",
    "barabar": "is",
    "anyatha": "else",
    "anyathayadi": "elif",  # anyathayadi ?
    "ya": "or",

    # loops
    "pratyek": "for",
    "mein": "in",
    "sima": "range",
    "break": "break",
    "jabtak": "while",
    "jaari": "continue",

    # types:
    "suchi": "list",
    "poornank": "int",
    "dashansh": "float",
    "Shunya": "None",
    "bool": "bool",
    "wakya":"str",
    "set()": "set()",
    'object': 'object',

    # imports
    "se": "from",
    "aayat": "import",
    "jaise": "as",

    # classes and functions
    "lautao": "return",
    "kaksha": "class",
    "vaishwik": "global",
    "karm": "def",
    "pass": "pass",
    "utpann": "yield",

    # errors
    "koshish_karo": "try",
    "yakin": "assert",
    "badhao": "raise",
    "siwaye": "except",
    "antatah": "finally",
    
    # list
    "purnankan()": "round()",
    "tod()": "slice()",
    "wargit()": "sorted()",
    "jod()": "sum()",
    "prakar()": "type()",

    #
    "sath": "with",
    "hataayein": "del",
    "lambda": "lambda",
}
