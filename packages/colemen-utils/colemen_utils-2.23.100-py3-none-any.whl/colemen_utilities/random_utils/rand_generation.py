# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=global-statement
'''
    A module of utility methods used for generating random data.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: random_utils
'''
import os
import re as _re
import random as _random
import exrex as _exrex
import hashlib as _hashlib
import time as _time
import string as _string
import uuid
from typing import Iterable, Union as _Union
from faker import Faker as _Faker
from colemen_config import _os_platform,_os_divider
import colemen_utilities.random_utils.rand_utils as _ru
import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu
import colemen_utilities.file_utils as _f
# import facades.rand_utils_facade as rand



# from colemen_utilities.object_utils import rand_option as option
# from colemen_utilities.string_generation import text,phone,email,url,abstract_name,rand

# from colemen_utilities.dict_utils.dict_utils import get_kwarg as _obj.get_kwarg

FAKER_INSTANCE = None

ADJECTIVES = None
NOUNS = None


def faker()->_Faker:
    global FAKER_INSTANCE
    if FAKER_INSTANCE is None:
        FAKER_INSTANCE = _Faker()
    return FAKER_INSTANCE


def gen_variations(value):
    value = str(value)
    varis = []
    lower = value.lower()
    upper = value.upper()
    snake_case = lower.replace(" ", "_")
    screaming_snake_case = upper.replace(" ", "_")
    varis.append(lower)
    varis.append(upper)
    varis.append(snake_case)
    varis.append(screaming_snake_case)
    varis.append(_csu.to_camel_case(value))
    varis.append(_csu.to_pascal_case(value))
    varis.append(_csu.to_kebab_case(value))
    return varis

def number(minimum=1,maximum=100):
    if minimum > maximum:
        maximum = minimum + maximum
    return _random.randint(minimum,maximum)
integer = number


def boolean(bias=50):
    '''
        Generate a random boolean
        ----------

        Arguments
        -------------------------
        [`bias`=50] {int}
            The likelihood of this returning True

            100 would always return True.


        Return {bool}
        ----------------------
        The randomly selected boolean

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 12:21:10
        `version`: 1.0
        `method_name`: boolean
        * @xxx [03-15-2023 12:22:02]: documentation for boolean
    '''
    return _random.randint(1,100) <= bias

def null_boolean():
    return{
        0: None,
        1: True,
        -1: False,
    }[_random.randint(-1, 1)]

def md5(raw_output: bool = False) -> _Union[bytes, str]:
    """Generate a random MD5 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the MD5 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = _hashlib.md5(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha1(raw_output: bool = False) -> _Union[bytes, str]:
    """Generate a random SHA1 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the SHA1 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = _hashlib.sha1(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha256(raw_output:bool=False) -> _Union[bytes, str]:
    res = _hashlib.sha256(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def past_date(days:_Union[int,None]=None)->int:
    if days is None:
        days = _random.randint(1,800)
    seconds = _random.randint(1,86400)
    return int(_time.time()) - ((days * 86400) + seconds)

def future_date(days:_Union[int,None]=None)->int:
    if days is None:
        days = _random.randint(1,800)
    seconds = _random.randint(1,86400)
    return int(_time.time()) + ((days * 86400) + seconds)

def rand(length=12, **kwargs):
    '''
        Generates a cryptographically secure random _string.


        ----------
        Arguments
        -----------------
        `length`=12 {int}
            The number of characters that the string should contain.

        Keyword Arguments
        -----------------
        `upper_case`=True {bool}
            If True, uppercase letters are included.
            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        `lower_case`=True {bool}
            If True, lowercase letters are included.
            abcdefghijklmnopqrstuvwxyz

        `digits`=True {bool}
            If True, digits are included.
            0123456789

        `symbols`=False {bool}
            If True, symbols are included.
            !"#$%&'()*+,-./:;<=>?@[]^_`{|}~

        `exclude`=[] {string|list}
            Characters to exclude from the random _string.

        Return
        ----------
        `return` {str}
            A random string of N length.
    '''

    uppercase = _obj.get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = _obj.get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = _obj.get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = _obj.get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = _obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    choices = ''
    if uppercase is True:
        choices += _string.ascii_uppercase
    if lowercase is True:
        choices += _string.ascii_lowercase
    if digits is True:
        choices += _string.digits
    if symbols is True:
        choices += _string.punctuation

    if len(exclude) > 0:
        if isinstance(exclude, str):
            exclude = list(exclude)
        for exd in exclude:
            choices = choices.replace(exd, '')

    return ''.join(_random.SystemRandom().choice(choices) for _ in range(length))

def letter(length=1,upper=True,lower=True):
    '''
        Generate a random letter or multiple letters.

        ----------

        Arguments
        -------------------------
        [`length`=1] {int}
            The number of characters that the string should contain.

        [`upper`=True] {bool}
            If True, uppercase letters are included.
            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        [`lower`=True] {bool}
            If True, lowercase letters are included.
            abcdefghijklmnopqrstuvwxyz

        Return {str}
        ----------------------
        The randomly generated letter(s)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-30-2022 10:03:25
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: letter
        * @xxx [07-30-2022 10:04:30]: documentation for letter
    '''


    return rand(length,upper_case=upper,lower_case=lower,digits=False)

def css_class(length=12):
    '''
        Generate a random string that is safe to use as a css class.

        ----------

        Arguments
        -------------------------
        `length` {int}
            How long the string should be.

        Return {str}
        ----------------------
        The randomly generate class string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-29-2022 14:45:19
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: css_class
        * @xxx [07-29-2022 14:46:00]: documentation for css_class
    '''


    value = rand(length)
    rand(1,digits=False)
    value = _re.sub(r'^[0-9]',letter(),value)
    return value

def uuid():
    return uuid.uuid4()


def text(minimum=10,maximum=500,null_bias=0):
    '''
        Wrapper method for faker().text()
        This adds the ability to randomly return null instead of the _string.

        ----------

        Arguments
        -------------------------
        [`minimum`=10] {int}
            The minimum number of characters the text must contain.
        [`maximum`=500] {int}
            The maximum number of characters the text must contain.
        [`null_bias`=0] {int}
            The odds [0-100] that the method will return None.


        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-16-2022 09:43:01
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: text
        # @xxx [05-16-2022 09:49:18]: documentation for text
    '''

    if isinstance(null_bias,(bool)):
        null_bias = 50 if null_bias is True else 0

    if null_bias:
        if faker().boolean(null_bias):
            return None

    val = faker().text()[:_random.randint(minimum,maximum)]
    val = val.replace("'","")
    return val

def credit_card_number(bias=100)->str:
    '''
        Generate a random valid credit card number.
        
        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of the generator returning a value,
            if this is 0 it will always return None.

        Return {str,None}
        ----------------------
        The credit card number as a string, or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-24-2023 12:02:39
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: credit_card_number
        * @xxx [04-24-2023 12:04:36]: documentation for credit_card_number
    '''
    if faker().boolean(bias):
        return faker().credit_card_number()
    return None

# word = faker().english_word
# '''Generate a random english word'''

def ip_address(bias=100):
    '''
        Generate a random IPv4 address.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of the generator returning a value,
            if this is 0 it will always return None.

        Return {str,None}
        ----------------------
        The ipv4 address, or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-24-2023 12:04:41
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: ip_address
        * @xxx [04-24-2023 12:05:15]: documentation for ip_address
    '''
    if faker().boolean(bias):
        return faker().ipv4()
    return None

def ip_address_ipv6(bias=100):
    '''
        Generate a random IPv6 address.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of the generator returning a value,
            if this is 0 it will always return None.

        Return {str,None}
        ----------------------
        The ipv6 address, or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-24-2023 12:04:41
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: ip_address
        * @xxx [04-24-2023 12:05:15]: documentation for ip_address
    '''
    if faker().boolean(bias):
        return faker().ipv6()
    return None



host_name = faker().hostname
'''Generate a random web host name'''
def hostname(bias=100):
    '''
        Generate a random hostname name
        ----------

        Return {str}
        ----------------------
        A random hostname name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: hostname
        * @xxx [03-07-2023 08:51:54]: documentation for hostname
    '''
    if boolean(bias) is False:
        return None
    return faker().hostname()

def http_method(bias=100):
    '''
        Generate a random http_method name
        ----------

        Return {str}
        ----------------------
        A random http_method name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: http_method
        * @xxx [03-07-2023 08:51:54]: documentation for http_method
    '''
    if boolean(bias) is False:
        return None
    return faker().http_method()

def user_agent_chrome(bias=100):
    '''
        Generate a random user_agent_chrome name
        ----------

        Return {str}
        ----------------------
        A random user_agent_chrome name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent_chrome
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent_chrome
    '''
    if boolean(bias) is False:
        return None
    return faker().chrome()

def user_agent_firefox(bias=100):
    '''
        Generate a random user_agent_firefox name
        ----------

        Return {str}
        ----------------------
        A random user_agent_firefox name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent_firefox
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent_firefox
    '''
    if boolean(bias) is False:
        return None
    return faker().firefox()


def user_agent_internet_explorer(bias=100):
    '''
        Generate a random user_agent_internet_explorer name
        ----------

        Return {str}
        ----------------------
        A random user_agent_internet_explorer name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent_internet_explorer
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent_internet_explorer
    '''
    if boolean(bias) is False:
        return None
    return faker().internet_explorer()


def user_agent_opera(bias=100):
    '''
        Generate a random user_agent_opera name
        ----------

        Return {str}
        ----------------------
        A random user_agent_opera name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent_opera
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent_opera
    '''
    if boolean(bias) is False:
        return None
    return faker().opera()

def user_agent_safari(bias=100):
    '''
        Generate a random user_agent_safari name
        ----------

        Return {str}
        ----------------------
        A random user_agent_safari name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent_safari
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent_safari
    '''
    if boolean(bias) is False:
        return None
    return faker().safari()

def user_agent(bias=100):
    '''
        Generate a random user_agent name
        ----------

        Return {str}
        ----------------------
        A random user_agent name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: user_agent
        * @xxx [03-07-2023 08:51:54]: documentation for user_agent
    '''
    if boolean(bias) is False:
        return None
    return faker().user_agent()







def phone(bias=100):
    '''
        Generate a random phone number or None.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of returning a phone number.

            If bias = 100 it will always return a phone number and never None.


        Return {str|None}
        ----------------------
        A random fake phone number or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: phone
        * @xxx [06-03-2022 07:25:42]: documentation for phone
    '''

    if faker().boolean(bias):
        return faker().phone_number()
    return None

def email(bias=100):
    '''
        Generate a random email or None.
        This is a wrapper for faker.email() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of returning an email.

            If bias = 100 it will always return an email and never None.


        Return {str|None}
        ----------------------
        A random fake email or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: email
        * @xxx [06-03-2022 07:25:42]: documentation for email
    '''
    if faker().boolean(bias):
        return faker().free_email()
    return None

def url(bias=100):
    '''
        Generate a random url or None.
        This is a wrapper for faker.url() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood of returning a url.

            If bias = 100 it will always return a url and never None.


        Return {str|None}
        ----------------------
        A random fake url or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: url
        * @xxx [06-03-2022 07:25:42]: documentation for url
    '''
    if faker().boolean(bias):
        return faker().url()
    return None

def abstract_name(bias=100):
    '''
        Generate an abstract (non-human) name consisting of an adjective and a noun.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood (0-100) of it returning an abstract name vs returning None

            If bias = 100 it will always return an abstract_name and never None.

        Return {str|None}
        ----------------------
        The abstract name or None if the bias is provided.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:36:04
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: abstract_name
        * @xxx [06-03-2022 07:38:26]: documentation for abstract_name
    '''
    # bias = _obj.get_kwarg(['bias'], 100, (int), **kwargs)
    if faker().boolean(bias):
        return f"{_rand_adjective()} {_rand_noun()}".title()
    return None

def _rand_adjective():
    global ADJECTIVES
    if ADJECTIVES is None:
        path = f"Lib/site-packages/colemen_utilities/random_utils/adjectives.txt"
        if _f.exists(path) is False:
            path = f"{os.getcwd()}/colemen_utilities/random_utils/adjectives.txt"
        options = _f.read.to_array(path)
        ADJECTIVES = options
    else:
        options = ADJECTIVES
    # options = [
    #     "adorable",
    #     "adventurous",
    #     "aggressive",
    #     "agreeable",
    #     "alert",
    #     "alive",
    #     "amused",
    #     "angry",
    #     "annoyed",
    #     "annoying",
    #     "anxious",
    #     "arrogant",
    #     "ashamed",
    #     "attractive",
    #     "average",
    #     "awful",
    #     "bad",
    #     "beautiful",
    #     "better",
    #     "bewildered",
    #     "black",
    #     "bloody",
    #     "blue",
    #     "blue-eyed",
    #     "blushing",
    #     "bored",
    #     "brainy",
    #     "brave",
    #     "breakable",
    #     "bright",
    #     "busy",
    #     "calm",
    #     "careful",
    #     "cautious",
    #     "charming",
    #     "cheerful",
    #     "clean",
    #     "clear",
    #     "clever",
    #     "cloudy",
    #     "clumsy",
    #     "colorful",
    #     "combative",
    #     "comfortable",
    #     "concerned",
    #     "condemned",
    #     "confused",
    #     "cooperative",
    #     "courageous",
    #     "crazy",
    #     "creepy",
    #     "crowded",
    #     "cruel",
    #     "curious",
    #     "cute",
    #     "dangerous",
    #     "dark",
    #     "dead",
    #     "defeated",
    #     "defiant",
    #     "delightful",
    #     "depressed",
    #     "determined",
    #     "different",
    #     "difficult",
    #     "disgusted",
    #     "distinct",
    #     "disturbed",
    #     "dizzy",
    #     "doubtful",
    #     "drab",
    #     "dull",
    #     "eager",
    #     "easy",
    #     "elated",
    #     "elegant",
    #     "embarrassed",
    #     "enchanting",
    #     "encouraging",
    #     "energetic",
    #     "enthusiastic",
    #     "envious",
    #     "evil",
    #     "excited",
    #     "expensive",
    #     "exuberant",
    #     "fair",
    #     "faithful",
    #     "famous",
    #     "fancy",
    #     "fantastic",
    #     "fierce",
    #     "filthy",
    #     "fine",
    #     "foolish",
    #     "fragile",
    #     "frail",
    #     "frantic",
    #     "friendly",
    #     "frightened",
    #     "funny",
    #     "gentle",
    #     "gifted",
    #     "glamorous",
    #     "gleaming",
    #     "glorious",
    #     "good",
    #     "gorgeous",
    #     "graceful",
    #     "grieving",
    #     "grotesque",
    #     "grumpy",
    #     "handsome",
    #     "happy",
    #     "healthy",
    #     "helpful",
    #     "helpless",
    #     "hilarious",
    #     "homeless",
    #     "homely",
    #     "horrible",
    #     "hungry",
    #     "hurt",
    #     "ill",
    #     "important",
    #     "impossible",
    #     "inexpensive",
    #     "innocent",
    #     "inquisitive",
    #     "itchy",
    #     "jealous",
    #     "jittery",
    #     "jolly",
    #     "joyous",
    #     "kind",
    #     "lazy",
    #     "light",
    #     "lively",
    #     "lonely",
    #     "long",
    #     "lovely",
    #     "lucky",
    #     "magnificent",
    #     "misty",
    #     "modern",
    #     "motionless",
    #     "muddy",
    #     "mushy",
    #     "mysterious",
    #     "nasty",
    #     "naughty",
    #     "nervous",
    #     "nice",
    #     "nutty",
    #     "obedient",
    #     "obnoxious",
    #     "odd",
    #     "old-fashioned",
    #     "open",
    #     "outrageous",
    #     "outstanding",
    #     "panicky",
    #     "perfect",
    #     "plain",
    #     "pleasant",
    #     "poised",
    #     "poor",
    #     "powerful",
    #     "precious",
    #     "prickly",
    #     "proud",
    #     "putrid",
    #     "puzzled",
    #     "quaint",
    #     "real",
    #     "relieved",
    #     "repulsive",
    #     "rich",
    #     "scary",
    #     "selfish",
    #     "shiny",
    #     "shy",
    #     "silly",
    #     "sleepy",
    #     "smiling",
    #     "smoggy",
    #     "sore",
    #     "sparkling",
    #     "splendid",
    #     "spotless",
    #     "stormy",
    #     "strange",
    #     "stupid",
    #     "successful",
    #     "super",
    #     "talented",
    #     "tame",
    #     "tasty",
    #     "tender",
    #     "tense",
    #     "terrible",
    #     "thankful",
    #     "thoughtful",
    #     "thoughtless",
    #     "tired",
    #     "tough",
    #     "troubled",
    #     "ugliest",
    #     "ugly",
    #     "uninterested",
    #     "unsightly",
    #     "unusual",
    #     "upset",
    #     "uptight",
    #     "vast",
    #     "victorious",
    #     "vivacious",
    #     "wandering",
    #     "weary",
    #     "wicked",
    #     "wide-eyed",
    #     "wild",
    #     "witty",
    #     "worried",
    #     "worrisome",
    #     "wrong",
    #     "zany",
    #     "zealous"]
    
    return _rand_option(options)

def _rand_noun():
    global NOUNS
    if NOUNS is None:
        path = f"Lib/site-packages/colemen_utilities/random_utils/nouns.txt"
        if _f.exists(path) is False:
            path = f"{os.getcwd()}/colemen_utilities/random_utils/nouns.txt"
        options = _f.read.to_array(path)
        NOUNS = options
    else:
        options = NOUNS
    # options = ["Actor",
    #     "Gold",
    #     "Painting",
    #     "Advertisement",
    #     "Grass",
    #     "Parrot",
    #     "Afternoon",
    #     "Greece",
    #     "Pencil",
    #     "Airport",
    #     "Guitar",
    #     "Piano",
    #     "Ambulance",
    #     "Hair",
    #     "Pillow",
    #     "Animal",
    #     "Hamburger",
    #     "Pizza",
    #     "Answer",
    #     "Helicopter",
    #     "Planet",
    #     "Apple",
    #     "Helmet",
    #     "Plastic",
    #     "Army",
    #     "Holiday",
    #     "Portugal",
    #     "Australia",
    #     "Honey",
    #     "Potato",
    #     "Balloon",
    #     "Horse",
    #     "Queen",
    #     "Banana",
    #     "Hospital",
    #     "Quill",
    #     "Battery",
    #     "House",
    #     "Rain",
    #     "Beach",
    #     "Hydrogen",
    #     "Rainbow",
    #     "Beard",
    #     "Ice",
    #     "Raincoat",
    #     "Bed",
    #     "Insect",
    #     "Refrigerator",
    #     "Belgium",
    #     "Insurance",
    #     "Restaurant",
    #     "Boy",
    #     "Iron",
    #     "River",
    #     "Branch",
    #     "Island",
    #     "Rocket",
    #     "Breakfast",
    #     "Jackal",
    #     "Room",
    #     "Brother",
    #     "Jelly",
    #     "Rose",
    #     "Camera",
    #     "Jewellery",
    #     "Russia",
    #     "Candle",
    #     "Jordan",
    #     "Sandwich",
    #     "Car",
    #     "Juice",
    #     "School",
    #     "Caravan",
    #     "Kangaroo",
    #     "Scooter",
    #     "Carpet",
    #     "King",
    #     "Shampoo",
    #     "Cartoon",
    #     "Kitchen",
    #     "Shoe",
    #     "China",
    #     "Kite",
    #     "Soccer",
    #     "Church",
    #     "Knife",
    #     "Spoon",
    #     "Crayon",
    #     "Lamp",
    #     "Stone",
    #     "Crowd",
    #     "Lawyer",
    #     "Sugar",
    #     "Daughter",
    #     "Leather",
    #     "Sweden",
    #     "Death",
    #     "Library",
    #     "Teacher",
    #     "Denmark",
    #     "Lighter",
    #     "Telephone",
    #     "Diamond",
    #     "Lion",
    #     "Television",
    #     "Dinner",
    #     "Lizard",
    #     "Tent",
    #     "Disease",
    #     "Lock",
    #     "Thailand",
    #     "Doctor",
    #     "London",
    #     "Tomato",
    #     "Dog",
    #     "Lunch",
    #     "Toothbrush",
    #     "Dream",
    #     "Machine",
    #     "Traffic",
    #     "Dress",
    #     "Magazine",
    #     "Train",
    #     "Easter",
    #     "Magician",
    #     "Truck",
    #     "Egg",
    #     "Manchester",
    #     "Uganda",
    #     "Eggplant",
    #     "Market",
    #     "Umbrella",
    #     "Egypt",
    #     "Match",
    #     "Van",
    #     "Elephant",
    #     "Microphone",
    #     "Vase",
    #     "Energy",
    #     "Monkey",
    #     "Vegetable",
    #     "Engine",
    #     "Morning",
    #     "Vulture",
    #     "England",
    #     "Motorcycle",
    #     "Wall",
    #     "Evening",
    #     "Nail",
    #     "Whale",
    #     "Eye",
    #     "Napkin",
    #     "Window",
    #     "Family",
    #     "Needle",
    #     "Wire",
    #     "Finland",
    #     "Nest",
    #     "Xylophone",
    #     "Fish",
    #     "Nigeria",
    #     "Yacht",
    #     "Flag",
    #     "Night",
    #     "Yak",
    #     "Flower",
    #     "Notebook",
    #     "Zebra",
    #     "Football",
    #     "Ocean",
    #     "Zoo",
    #     "Forest",
    #     "Oil",
    #     "Garden",
    #     "Fountain",
    #     "Orange",
    #     "Gas",
    #     "France",
    #     "Oxygen",
    #     "Girl",
    #     "Furniture",
    #     "Oyster",
    #     "Glass",
    #     "Garage",
    #     "Ghost"
    #     ]
    
    return _rand_option(options)

def _rand_option(options):
    list_len = len(options)
    try:
        return options[_random.randint(0, list_len)]
    except IndexError:
        return _rand_option(options)

def female_first_last_name()->tuple:
    '''
        Generate a random female first and last name

        ----------

        Return {tuple}
        ----------------------
        A tuple (first,last)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 11:48:42
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: female_first_last_name
        * @xxx [06-05-2022 11:49:20]: documentation for female_first_last_name
    '''

    
    fake = faker()
    return (fake.first_name_female(), fake.last_name())

def last_name():
    '''
        Generate a random last name.
        ----------

        Return {str}
        ----------------------
        A randomly generate last name.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-15-2022 18:42:34
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: last_name
        * @TODO []: documentation for last_name
    '''
    fake = faker()
    return fake.last_name()



def male_first_last_name()->tuple:
    '''
        Generate a random male first and last name

        ----------

        Return {tuple}
        ----------------------
        A tuple (first,last)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 11:48:42
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: male_first_last_name
        * @xxx [06-05-2022 11:49:20]: documentation for male_first_last_name
    '''    
    fake = faker()
    return (fake.first_name_male(), fake.last_name())

def male_first_name():
    fake = faker()
    return fake.first_name_male()

def female_first_name():
    fake = faker()
    return fake.first_name_female()

def common_animal():
    '''
        Get a random common animal.

        ----------


        Return {str}
        ----------------------
        The name of a random animal.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-21-2022 07:53:39
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: common_animal
        * @xxx [07-21-2022 07:54:09]: documentation for common_animal
    '''


    return _rand_option(_ru.COMMON_ANIMALS)

def threat():
    '''
        Randomly generate a shitty threat.

        ----------


        Return {str}
        ----------------------
        A random threat.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-21-2022 08:04:21
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: threat
        * @xxx [07-21-2022 08:04:40]: documentation for threat
    '''
    exrex_threats = [
        f"you (could|might|may|will) die (horribly|slowly|by drowning in (chipmunks|hamsters|chainsaws|ferrets|{common_animal()}))",
        f"your (pets|family|friends|family and friends|loved ones) will be (haunted|eaten|stalked|starred at menacingly) by (snail|rabbit|kitten|{common_animal()}) ghosts",
    ]

    threat_string = _rand_option(exrex_threats)
    threat_string = _rand_option(list(_exrex.generate(threat_string)))
    threat_string = threat_string.replace("__RANDOM_ANIMAL__",common_animal())
    return threat_string

def gender(bias=100,return_int=False)->str:
    '''
        Randomly generate a gender "female", "male", "other"

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood (0-100) of it returning a gender vs returning None

            If bias = 100 it will always return a gender and never None.

        [`return_int`=False] {bool}
            If True it will return the index of the option instead of the string:
            - 0 = female
            - 1 = male
            - 2 = other

        Return {str}
        ----------------------
        The gender.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:11:34
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: gender
        * @xxx [06-04-2022 10:12:06]: documentation for gender
    '''
    options = ["female","male","other"]

    if return_int is False:
        if faker().boolean(bias):
            return _ru.option(options)
    if return_int is True:
        if faker().boolean(bias):
            return _random.randint(0,len(options)-1)
    return None

    # return _ru.option(["male","female"])


def user(**kwargs)->dict:
    '''
        Randomly generate a user data dictionary.

        ----------

        Keyword Arguments
        -------------------------
        [`gender`=None] {str|None}
            The gender of the user (male,female), if not provided one is randomly selected.

        [`password`=None] {str|None}
            The password for the user, if not provided one is randomly generated.

        Return {dict}
        ----------------------
        A user dictionary:
        {
            `gender`:"female",
            `first_name`:"Sarah",
            `last_name`:"Paulson",
            `password`:"Zxbp43JMGuPm",
            `email`:"dork@gmail.com",
            `phone`:"806.355.2586",
            `birthday`:123456789,
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:12:17
        `memberOf`: rand_generation
        `version`: 0.0.0
        `method_name`: user
        * @xxx [06-04-2022]: documentation for user
    '''


    fake = faker()

    data = {
        "gender":"",
        "first_name":"",
        "last_name":"",
        "password":_obj.get_kwarg(['password','pass'], rand(), (None,str), **kwargs),
        "email":"",
        "phone":"",
        "birthday":past_date(),
    }

    ugen = _obj.get_kwarg(['gender'], None, (None,str), **kwargs)
    # data['password'] = _obj.get_kwarg(['password','pass'], rand(), (None,str), **kwargs)

    if ugen is None:
        data['gender'] = gender()

    if isinstance(ugen,(str)):
        gen = _csu.determine_gender(ugen)
        if gen is None:
            data['gender'] = gender()
        else:
            data['gender'] = gen

    if data['gender'] == "female":
        data['first_name'] = fake.first_name_female()
    if data['gender'] == "male":
        data['first_name'] = fake.first_name_male()
    data['last_name'] = fake.last_name()
    data['email'] = fake.free_email()
    data['phone'] = fake.phone_number()

    return data


def file_extension():
    return _rand_option(_ru.COMMON_FILE_EXTENSIONS)

def dir_path(**kwargs):
    '''
        Generate a random directory path.

        ----------

        Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Keyword Arguments
        -------------------------
        [`depth`=2] {int}
            How many directories should be generated.

        [`divider`="\\"] {str}
            The directory divider

        [`drive`=random] {str}
            The drive letter

        Return {str}
        ----------------------
        The randomly generated dir path.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-30-2022 10:41:55
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: dir_path
        * @xxx [07-30-2022 10:44:25]: documentation for dir_path
    '''
    divider = "/" if _os_platform == "linux" else "\\"

    depth = _obj.get_kwarg(['depth'], 2, (int), **kwargs)
    if depth < 0:
        depth = 0
    divider = _obj.get_kwarg(['divider'], _os_divider, (str), **kwargs)
    drive = _obj.get_kwarg(['drive'], None, (str), **kwargs)    
    dirs = []
    for _ in range(depth):
        dirs.append(_rand_noun())
    dirs = divider.join(dirs)
    path = dirs
    # dirs = os.path.join(dirs)
    if _os_platform == "Windows" or drive is not None:
        path = f"{drive}:{divider}"
        if len(dirs) > 0:
            path = f"{drive}:{divider}{dirs}{divider}"
    return path

def file_path(**kwargs):
    '''
        Generate a random file path.

        ----------

        Keyword Arguments
        -------------------------
        [`depth`=2] {int}
            How many directories should be generated.

        [`divider`="\\"] {str}
            The directory divider

        [`file_name`=random] {str}
            The name of the file, this should include the file extension.
            If it does not have an extension, a random one is generated.

        [`drive`=random] {str}
            The drive letter

        Return {str}
        ----------------------
        The randomly generated file path.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-30-2022 10:22:59
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: file_path
        * @xxx [07-30-2022 10:29:45]: documentation for file_path
    '''

    
    depth = _obj.get_kwarg(['depth'], 2, (int), **kwargs)
    if depth < 0:
        depth = 0

    divider = _obj.get_kwarg(['divider'], _os_divider, (str), **kwargs)
    file_name = _obj.get_kwarg(['file_name'], _rand_noun(), (str), **kwargs)
    drive = _obj.get_kwarg(['drive'], None, (str), **kwargs)
    if drive is None and _os_platform == "Windows":
        drive = letter(1,True,False)


    base_dir = dir_path(depth=depth,divider=divider,drive=drive)

    path = f"{base_dir}{divider}{file_name}"

    extension = _f.get_ext(path)
    if len(extension) == 0:
        path = f"{base_dir}{file_name}.{file_extension()}"

    return path



# ---------------------------------------------------------------------------- #
#                              GEOGRAPHY / ADDRESS                             #
# ---------------------------------------------------------------------------- #


def country():
    '''
        Generate a random country name
        ----------

        Return {str}
        ----------------------
        A random country name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: country
        * @xxx [03-07-2023 08:51:52]: documentation for country
    '''
    return faker().country()

def city():
    '''
        Generate a random city name
        ----------

        Return {str}
        ----------------------
        A random city name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: city
        * @xxx [03-07-2023 08:51:54]: documentation for city
    '''
    return faker().city()

def postcode():
    '''
        Generate a random postcode name
        ----------

        50995

        Return {str}
        ----------------------
        A random postcode name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: postcode
        * @xxx [03-07-2023 08:51:54]: documentation for postcode
    '''
    return faker().postcode()
zipcode = postcode

def street_address():
    '''
        Generate a random street_address name
        ----------

        Return {str}
        ----------------------
        A random street_address name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: street_address
        * @xxx [03-07-2023 08:51:54]: documentation for street_address
    '''
    return faker().street_address()


def state():
    '''
        Generate a random state name
        ----------

        Return {str}
        ----------------------
        A random state name

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-07-2023 08:50:50
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: state
        * @xxx [03-07-2023 08:51:54]: documentation for state
    '''
    return faker().state()

latitude = faker().latitude()
'''Randomly generate a latitudinal coordinate'''
longitude = faker().longitude()
'''Randomly generate a longitudinal coordinate'''

def http_status_code(bias:int=100)->int:
    '''
        Generate a random HTTP status code.
        ----------

        Arguments
        -------------------------

        [`bias`=100] {int}
            The likelihood (0-100) of it returning an value vs returning None

            If bias = 100 it will always return a value and never None.

        Return {int,None}
        ----------------------
        A random status code or None

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 12:09:08
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: http_status_code
        * @xxx [03-15-2023 12:10:29]: documentation for http_status_code
    '''
    valid_status_codes = ["100","101","102","103","200","201","202","203","204","205","206","207","208","226","300","301","302","303","304","305","306","307","308","400","401","402","403","404","405","406","407","408","409","410","411","412","413","414","415","416","417","418","421","422","423","424","425","426","428","429","431","451","500","501","502","503","504","505","506","507","508","510","511"]
    if faker().boolean(bias):
        return int(_ru.option(valid_status_codes))
    return None


def http_request_method(bias:int=100)->str:
    '''
        Generate a random HTTP request method.
        ----------

        Arguments
        -------------------------

        [`bias`=100] {int}
            The likelihood (0-100) of it returning an value vs returning None

            If bias = 100 it will always return a value and never None.

        Return {str,None}
        ----------------------
        A random request method or None

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 12:09:08
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: http_request_method
        * @xxx [03-15-2023 12:10:29]: documentation for http_request_method
    '''
    valid_request_methods = ["connect","delete","get","head","options","patch","post","put","trace"]
    if faker().boolean(bias):
        return _ru.option(valid_request_methods)
    return None


def list_of_strings(length=3,bias:int=100)->Iterable[str]:
    out = []
    for x in range(length):
        out.append(abstract_name())
    return out
def list_of_integers(length=3,minimum=1,maximum=100,exclude=None,bias:int=100)->Iterable[str]:
    out = []
    for x in range(length):
        out.append(number(minimum,maximum))
    if isinstance(exclude,(list)):
        no = []
        for o in out:
            if o not in exclude:
                no.append(o)
        out = no
    return out
