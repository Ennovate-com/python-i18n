# sample_strings.py
#
# License: GNU LESSER GENERAL PUBLIC LICENSE
#   https://www.gnu.org/software/gettext/manual/html_node/GNU-LGPL.html
#
# This file and its contents and all others related to this software are provided
# AS IS, WITHOUT ANY WARRANTY OR CONDITION, EXPRESS OR IMPLIED.

from typing import Final

import i18n


class _StringForTesting(object):
  __slots__ = ( '_structured_msgid', '_numbers', '_context', '_msgid_plural', '_translations_dict' )

  @property
  def msgid(self) -> str:
    return self._structured_msgid

  @property
  def numbers(self) -> list[int]:
    return self._numbers

  @property
  def context(self) -> str:
    return self._context

  @property
  def msgid_plural(self) -> str:
    return self._msgid_plural

  def __init__(self, _structured_msgid: str, /, numbers: list[int] | None, context = None, msgid_plural = None) -> None:
    assert isinstance(_structured_msgid, str), type(_structured_msgid)
    assert isinstance(numbers, tuple | list | None), type(numbers)
    assert isinstance(context, str | None), type(context)
    self._structured_msgid = _structured_msgid
    self._numbers = numbers
    self._context = context
    if numbers == None:
      assert msgid_plural == None, numbers
    elif msgid_plural == None:
       self._msgid_plural = _structured_msgid
    else:
       self._msgid_plural = msgid_plural
    self._translations_dict = dict()
    return None

  def get_translation_for_language(self, _lang: str) -> str:
    assert _lang in self._translations_dict, _lang
    return self._translations_dict[_lang]

  def set_translation_for_languages(self, _translation: str, *_locales: str) -> None:
    for l in _locales:
      assert l not in self._translations_dict, l
      self._translations_dict[l] = _translation
    return None


class StringWithPronoun(_StringForTesting):
  strings_without_context: Final[list] = [ ]
  strings_with_context_dict: Final[dict] = dict()
  __slots__ = ( '_pronoun_type', '_person', '_names', '_gender' )

  @property
  def pronoun_type(self) -> str:
    return self._pronoun_type

  @property
  def person(self) -> str:
    return self._person

  @property
  def names(self) -> str:
    return self._names

  @property
  def gender(self) -> str:
    return self._gender

  def __init__(self, _structured_msgid: str, _pronoun_type: i18n.PronounTranslation.PronounTypeEnum, _person: i18n.PronounTranslation.PronounPersonEnum, /, numbers: list[int] | None = None, context = None, msgid_plural = None, names: list[str] | None = None, gender: i18n.PronounTranslation.GenderEnum = None) -> None:
    super().__init__(_structured_msgid, numbers if names == None else (len(names),), context, msgid_plural)
    if _person == i18n.PronounTranslation.PronounPersonEnum.Third_Person and (self._numbers == None or 1 in self._numbers) and gender == None:
      raise ValueError('gender must be specified when person is Third_Person and number of persons is 1')
    self._pronoun_type = _pronoun_type
    self._person = _person
    if context == None:
      StringWithPronoun.strings_without_context.append(self)
    elif context in StringWithPronoun.strings_with_context_dict.keys():
      StringWithPronoun.strings_with_context_dict[context].append(self)
    else:
      StringWithPronoun.strings_with_context_dict[context] = [ self ]
    self._names = names
    self._gender = gender
    return None


# Placeholders for pronouns (and only pronouns or determiners) should start with "{pronoun", ex: "{pronoun}", "{pronoun1}", "{pronoun2}"


## Subject ##

pronoun_type = i18n.PronounTranslation.PronounTypeEnum.Subject

# First Person - Singular

person = i18n.PronounTranslation.PronounPersonEnum.First_Person

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,))
s.set_translation_for_languages('When I go out to eat, I usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), 'test_context')
s.set_translation_for_languages('When I go out to eat, I usually order pizza.', 'en', 'en_US')

# First Person - Plural, 2

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (2,))
s.set_translation_for_languages('When we go out to eat, we both usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (2,), 'test_context')
s.set_translation_for_languages('When we go out to eat, we both usually order pizza.', 'en', 'en_US')

# First Person - Plural, more than 2

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6))
s.set_translation_for_languages('When we go out to eat, we all usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6), 'test_context')
s.set_translation_for_languages('When we go out to eat, we all usually order pizza.', 'en', 'en_US')

# Second Person - Singular

person = i18n.PronounTranslation.PronounPersonEnum.Second_Person

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,))
s.set_translation_for_languages('When you go out to eat, you usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), 'test_context')
s.set_translation_for_languages('When you go out to eat, you usually order pizza.', 'en', 'en_US')

# Second Person - Plural, 2

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (2,))
s.set_translation_for_languages('When you go out to eat, you both usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (2,), 'test_context')
s.set_translation_for_languages('When you go out to eat, you both usually order pizza.', 'en', 'en_US')

# Second Person - Plural, more than 2

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6))
s.set_translation_for_languages('When you go out to eat, you all usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6), 'test_context')
s.set_translation_for_languages('When you go out to eat, you all usually order pizza.', 'en', 'en_US')

# Third Person - Singular, Male

person = i18n.PronounTranslation.PronounPersonEnum.Third_Person

names = ( 'John', )

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), names = names, gender = i18n.PronounTranslation.GenderEnum.Male)
s.set_translation_for_languages('When John goes out to eat, he usually orders pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), 'test_context', names = names, gender = i18n.PronounTranslation.GenderEnum.Male)
s.set_translation_for_languages('When John goes out to eat, he usually orders pizza.', 'en', 'en_US')

# Third Person - Singular, Female
names = ( 'Jane', )

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), names = names, gender = i18n.PronounTranslation.GenderEnum.Female)
s.set_translation_for_languages('When Jane goes out to eat, she usually orders pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (1,), 'test_context', names = names, gender = i18n.PronounTranslation.GenderEnum.Female)
s.set_translation_for_languages('When Jane goes out to eat, she usually orders pizza.', 'en', 'en_US')

# Third Person - Plural, two names

names = ( 'John', 'Jane' )

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, names = names)
s.set_translation_for_languages('When John and Jane go out to eat, they both usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, 'test_context', names = names)
s.set_translation_for_languages('When John and Jane go out to eat, they both usually order pizza.', 'en', 'en_US')

# Third Person - Plural, "they"

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6))
s.set_translation_for_languages('When they go out to eat, they all usually order pizza.', 'en', 'en_US')

s = StringWithPronoun('/sentence/with_pronoun/subject/test1', pronoun_type, person, (3, 6), 'test_context')
s.set_translation_for_languages('When they go out to eat, they all usually order pizza.', 'en', 'en_US')


## Object ##

pronoun_type = i18n.PronounTranslation.PronounTypeEnum.Object


## Possessive ##

pronoun_type = i18n.PronounTranslation.PronounTypeEnum.Possessive


## Reflexive ##

pronoun_type = i18n.PronounTranslation.PronounTypeEnum.Reflexive


## Possessive Determiner ##

pronoun_type = None


# People


class Person(object):
  __slots__ = ( '_name', '_gender', '_always_orders' )

  @property
  def name(self) -> str:
    return self._name

  @property
  def gender(self) -> str:
    return self._gender

  @property
  def always_orders(self) -> str:
    return self._always_orders

  def __init__(self, _name: str, _gender: i18n.PronounTranslation.GenderEnum, _always_orders: str) -> None:
    self._name = _name
    self._gender = _gender
    self._always_orders = _always_orders
    return None


people = []
people.append(Person('John',   i18n.PronounTranslation.GenderEnum.Male,    'pizza'    ))
people.append(Person('Jane',   i18n.PronounTranslation.GenderEnum.Female,  'a burger' ))
people.append(Person('Jamie',  i18n.PronounTranslation.GenderEnum.Neutral, 'chicken'  ))
people.append(Person('Jordan', i18n.PronounTranslation.GenderEnum.Neutral, 'tacos'    ))
people.append(Person('Kenny',  i18n.PronounTranslation.GenderEnum.Male,    'pizza'    ))
people.append(Person('Karen',  i18n.PronounTranslation.GenderEnum.Female,  'a burger' ))
people.append(Person('Lou',    i18n.PronounTranslation.GenderEnum.Male,    'chicken'  ))
people.append(Person('Lisa',   i18n.PronounTranslation.GenderEnum.Female,  'tacos'    ))
people.append(Person('Martin', i18n.PronounTranslation.GenderEnum.Male,    'pizza'    ))
people.append(Person('Mary',   i18n.PronounTranslation.GenderEnum.Female,  'a burger' ))
people.append(Person('Nate',   i18n.PronounTranslation.GenderEnum.Male,    'chicken'  ))
people.append(Person('Nancy',  i18n.PronounTranslation.GenderEnum.Female,  'tacos'    ))
people.append(Person('Paul',   i18n.PronounTranslation.GenderEnum.Male,    'pizza'    ))
people.append(Person('Penny',  i18n.PronounTranslation.GenderEnum.Female,  'a burger' ))
