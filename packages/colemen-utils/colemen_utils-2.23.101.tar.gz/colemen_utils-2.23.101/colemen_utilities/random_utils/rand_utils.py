# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    A module of utility methods used for performing various
    actions randomly.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: random_utils
'''

import random as _random
import colemen_utilities.dict_utils as _obj
# import colemen_utilities.string_utils as _csu
# import hashlib
# import time
# import string
# from typing import Union

# import facades.rand_utils_facade as rand



# from colemen_utilities._object_utils import rand_option as option
# from colemen_utilities.string_generation import text,phone,email,url,abstract_name,rand
# from colemen_utilities.dict_utils.dict_utils import get_kwarg as _obj.get_kwarg


COMMON_FILE_EXTENSIONS = ["aif","au","avi","bat","bmp","class","java","csv","cvs","dbf","dif","doc","docx","eps","exe","fm3","gif","hqx","htm","html","jpg","jpeg","mac","map","mdb","mid","midi","mov","qt","mtb","mtw","pdf","p65","t65","png","ppt","pptx","psd","psp","qxd","ra","rtf","sit","tar","tif","txt","wav","wk3","wks","wpd","wp5","xls","xlsx","zip"]

COMMON_ANIMALS = [
    "Aardvark",
    "Alligator",
    "Alpaca",
    "Anaconda",
    "Ant",
    "Anteater",
    "Antelope",
    "Aphid",
    "Armadillo",
    "Asp",
    "Ass",
    "Baboon",
    "Badger",
    "Bald Eagle",
    "Barracuda",
    "Bass",
    "Basset Hound",
    "Bat",
    "Bearded Dragon",
    "Beaver",
    "Bedbug",
    "Bee",
    "Bee-eater",
    "Bird",
    "Bison",
    "Black panther",
    "Black Widow Spider",
    "Blue Jay",
    "Blue Whale",
    "Bobcat",
    "Buffalo",
    "Butterfly",
    "Buzzard",
    "Camel",
    "Canada Lynx",
    "Carp",
    "Cat",
    "Caterpillar",
    "Catfish",
    "Cheetah",
    "Chicken",
    "Chimpanzee",
    "Chipmunk",
    "Cobra",
    "Cod",
    "Condor",
    "Cougar",
    "Cow",
    "Coyote",
    "Crab",
    "Crane Fly",
    "Cricket",
    "Crocodile",
    "Crow",
    "Cuckoo",
    "Deer",
    "Dinosaur",
    "Dog",
    "Dolphin",
    "Donkey",
    "Dove",
    "Dragonfly",
    "Duck",
    "Eagle",
    "Eel",
    "Elephant",
    "Emu",
    "Falcon",
    "Ferret",
    "Finch",
    "Fish",
    "Flamingo",
    "Flea",
    "Fly",
    "Fox",
    "Frog",
    "Goat",
    "Goose",
    "Gopher",
    "Gorilla",
    "Guinea Pig",
    "Hamster",
    "Hare",
    "Hawk",
    "Hippopotamus",
    "Horse",
    "Hummingbird",
    "Humpback Whale",
    "Husky",
    "Iguana",
    "Impala",
    "Kangaroo",
    "Lemur",
    "Leopard",
    "Lion",
    "Lizard",
    "Llama",
    "Lobster",
    "Margay",
    "Monitor lizard",
    "Monkey",
    "Moose",
    "Mosquito",
    "Moth",
    "Mountain Zebra",
    "Mouse",
    "Mule",
    "Octopus",
    "Orca",
    "Ostrich",
    "Otter",
    "Owl",
    "Ox",
    "Oyster",
    "Panda",
    "Parrot",
    "Peacock",
    "Pelican",
    "Penguin",
    "Perch",
    "Pheasant",
    "Pig",
    "Pigeon",
    "Polar bear",
    "Porcupine",
    "Quagga",
    "Rabbit",
    "Raccoon",
    "Rat",
    "Rattlesnake",
    "Red Wolf",
    "Rooster",
    "Seal",
    "Sheep",
    "Skunk",
    "Sloth",
    "Snail",
    "Snake",
    "Spider",
    "Tiger",
    "Whale",
    "Wolf",
    "Wombat",
    "Zebra"
]





def option(options:list,count:int=1,allow_repeats:bool=False,default=None)->any:
    '''
        Select a random option from a list.

        ----------

        Arguments
        -------------------------
        `options` {list}
            The list or dictionary to select from.

        [`count`=1] {int}
            How many random options to select.

        [`allow_repeats`=False] {bool}
            If True, the result can contain the same option multiple times.

        [`default`=None] {any}
            This is the value returned if options is an empty list.

        Return {any}
        ----------------------
        The random option or a list of random options if `count` is greater than one.\n
        returns `default` if there are no options.


        Examples
        ----------------------

        options = ["kitties","and","titties"]\n

        _obj.rand_option(options)\n
        // 'titties'\n

        _obj.rand_option(options,count=2)\n
        // ['kitties', 'and']\n

        _obj.rand_option(options,count=8)\n
        // ['kitties', 'and', 'titties']\n

        _obj.rand_option(options,count=6,repeats=True)\n
        // ['titties', 'kitties', 'titties', 'and', 'kitties', 'and']\n

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 08:01:13
        `memberOf`: _objectUtils
        `version`: 1.0
        `method_name`: rand_option
        * @xxx [06-03-2022 08:33:02]: documentation for rand_option
    '''

    # count = _obj.get_kwarg(['count'], 1, (int), **kwargs)
    # allow_repeats = _obj.get_kwarg(['allow repeats','repeats'], False, (bool), **kwargs)
    # default = _obj.get_kwarg(['default'], None, None, **kwargs)
    # keys = _obj.get_kwarg(['keys','return keys'], False, (bool), **kwargs)

    # TODO []: add support for dictionaries
    # if isinstance(options,(dict)):
    #     is_dict = True
    #     return options[random_key(options)]


    olen = len(options)

    # @Mstep [IF] if there are no options.
    if olen == 0:
        # @Mstep [RETURN] return None.
        return default

    # @Mstep [IF] if the option length is less than or equal to the selection count.
    if olen <= count:
        # @Mstep [if] if repeats are not allowed.
        if allow_repeats is False:
            # @Mstep [] set the selection count to the number of options.
            count = olen

    # @Mstep [IF] if the count is equal to the options length
    if count == olen:
        # @Mstep [IF] if the selection count is one
        if count == 1:
            # @Mstep [return] return the only available option.
            return options[0]
        return options

    selection = []

    while len(selection) != count:
        select = options[_random.randint(0, olen-1)]
        if allow_repeats is False and select not in selection:
            selection.append(select)
        elif allow_repeats is True:
            selection.append(select)


    if len(selection) == 1:
        return selection[0]
    return selection






