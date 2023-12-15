# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=global-statement
'''
    A module of utility methods used for generating console log messages.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: random_utils
'''

import random as _random
import hashlib as _hashlib
import time as _time
import string as _string
from typing import Union as _Union


from colorama import Fore as _Fore
from colorama import Style as _Style
from colorama import Back as _Back


import colemen_config as config
import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu



FILTER = []
TIMERS = {}

def start_timer(name:str):
    if name not in TIMERS:
        data = {
            "start_time":_time.time(),
            "end_time":None,
            "duration":None,
        }
        TIMERS[name] = data

def end_timer(name:str,print_log:bool=True):
    if name not in TIMERS:
        return None
    t = TIMERS[name]
    t['end_time'] = _time.time()
    t['duration'] = t['end_time'] - t['start_time']
    TIMERS[name] = t
    if print_log is True:
        log(f"{name} duration: {t['duration']} seconds","info")

def add_filter(value):
    if value not in FILTER:
        FILTER.append(value)

def _contains_filter_term(value):
    for x in FILTER:
        if x in value:
            return True
    return False


def _prepend(message,fore):
    if fore is not None:
        return fore + message
    return message



def log(
    message,
    style:str=None,
    return_string:bool=False,
    same_line:bool=False,
    ):
    '''
        Print shit to the console with a little style.

        ----------

        Arguments
        -------------------------
        `message` {string}
            The message to print.

        `style` {string}
            The style to use on the message:
            - error, red
            - success, green
            - warn, yellow
            - cyan, info
            - magenta, pink
            - blue

            You can also provide "invert" which will make the background the primary color and the text black.

        [`return_string`=False] {bool}
            if True, the message is not printed, but returned.

        [`same_line`=False] {bool}
            if True, the message is printed to the same line and the cursor is set back to the beginning.
        Keyword Arguments
        -------------------------

        Return {string|None}
        ----------------------
        if return_string is False or not provided, it will return nothing, otherwise is returns the string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-28-2022 08:59:11
        `memberOf`: log
        `version`: 1.0
        `method_name`: log
        * @xxx [06-28-2022 09:21:49]: documentation for log
    '''



    # return_string = _obj.get_kwarg(['return','return string','no print'],False,(bool),**kwargs)
    # style = _obj.get_kwarg(['style'],style,(str),**kwargs)
    # same_line = _obj.get_kwarg(['same_line'],False,(bool),**kwargs)
    # bg = _obj.get_kwarg(['bg','back','back ground'],None,(str),**kwargs)
    # fg = _obj.get_kwarg(['fg','fore','fore ground'],None,(str),**kwargs)

    if config.verbose is False:
        return None
    if len(FILTER) > 0:
        skip = not _contains_filter_term(message)
        if skip is True:
            skip = not _contains_filter_term(style)
        if skip is True:
            return None

    
    
    colors = [
        {
            "styles":["default","standard","white"],
            "colors":{
                "fore":_Fore.WHITE,
                "back":None
            },
            "invert":{
                "back":_Back.WHITE,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["error","red"],
            "colors":{
                "fore":_Fore.RED,
                "back":None
            },
            "invert":{
                "back":_Back.RED,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["success","green"],
            "colors":{
                "fore":_Fore.GREEN,
                "back":None
            },
            "invert":{
                "back":_Back.GREEN,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["warn","warning","yellow"],
            "colors":{
                "fore":_Fore.YELLOW,
                "back":None
            },
            "invert":{
                "back":_Back.YELLOW,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["cyan","info"],
            "colors":{
                "fore":_Fore.CYAN,
                "back":None
            },
            "invert":{
                "back":_Back.CYAN,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["magenta","pink"],
            "colors":{
                "fore":_Fore.MAGENTA,
                "back":None
            },
            "invert":{
                "back":_Back.MAGENTA,
                "fore":_Fore.BLACK
            },
        },
        {
            "styles":["blue"],
            "colors":{
                "fore":_Fore.BLUE,
                "back":None
            },
            "invert":{
                "back":_Back.BLUE,
                "fore":_Fore.BLACK
            },
        }
    ]

    output = message


    if style is None and return_string is False:
        if same_line:
            print(output,end="\r",flush=True)
        else:
            print(output)
        return



    if style is not None:
        ais = _csu.array_in_string
        style = style.lower()

        for sty in colors:
            # print(f"style: {sty['styles']}")
            if ais(sty['styles'],style):
                if ais(["invert","inv"],style):
                    output = _prepend(output,sty['invert']['fore'])
                    output = _prepend(output,sty['invert']['back'])
                else:
                    output = _prepend(output,sty['colors']['fore'])
                    output = _prepend(output,sty['colors']['back'])

        output = output + _Style.RESET_ALL



    if return_string is False:
        # print(f"return_string is False")
        if same_line:
            print(output,end="\r",flush=True)
        else:
            print(output)
    return output