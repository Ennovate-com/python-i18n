# src/i18n/text.py
#
# License: GNU LESSER GENERAL PUBLIC LICENSE
#   https://www.gnu.org/software/gettext/manual/html_node/GNU-LGPL.html
#
# This file and its contents and all others related to this software are provided
# AS IS, WITHOUT ANY WARRANTY OR CONDITION, EXPRESS OR IMPLIED.
#
# Strings are stored in sentence case - first word capitalized
# Use lower(...) to convert to lower case
# Use title(...) to convert to title case

import errno, gettext, inspect, locale, logging, os, sys, traceback
from enum import Enum
from types import FrameType
from typing import ClassVar, Final


message_locale_category: Final[int] = locale.LC_MESSAGES
message_locale_category_dirname: Final[str] = 'LC_MESSAGES'


class TranslationLanguages(object):
  i18n_contexts: Final[dict] = dict()
  __slots__: ( '_langs' )
      # _langs is a tuple or list of language codes
      # called "language code" for (language_code, encoding) = locale.getDefaultLocale()
      # called "languages" in gettext.translation(domain, localedir=None, languages=None, class_=None, fallback=False)¶

  def _i18n_context(self, _context: str):
    if _context not in self.i18n_contexts:
      self.i18n_contexts[_context] = TranslationContext(Translation(TranslationDomainLanguage(TranslationDomain('i18n'), self)), _context)
    return self.i18n_contexts[_context]

  @property
  def conjunctions(self):
    return self._i18n_context('conjunctions')

  @property
  def pronouns(self):
    return PronounTranslation(self, frame_summary = traceback.extract_stack(limit = 2)[0])

  def __init__(self, *_language_codes: tuple[str] | list[str]) -> None:
    super().__init__()
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    logging.info(f"Default shared locale directory is '{sys.base_prefix}/share/locales'")

    for i in range(0, len(_language_codes)):
      assert isinstance(_language_codes[i], str | None), f'language_codes[{i}] invalid type: {type(_language_codes[i])}'
    if len(_language_codes) == 0 or None in _language_codes:
      ( language_code, encoding ) = locale.getdefaultlocale()
      logging.info(f"( default locale ) language_code: {language_code} encoding: {encoding}")
      for lc in (locale.LC_COLLATE, locale.LC_CTYPE, locale.LC_MONETARY, locale.LC_NUMERIC, locale.LC_TIME, locale.LC_MESSAGES, ):
        ( language_code, encoding ) = locale.getlocale(category = lc)
        logging.info(f"locale category: {lc} language_code: {language_code} encoding: {encoding}")
      ( language_code, encoding ) = locale.getlocale(category = message_locale_category)
      if language_code == None:
        ( language_code, encoding ) = locale.getdefaultlocale()
        # language_code - ex: 'en_US' for US, encoding - 'UTF-8'
      assert language_code != None, language_code
      if len(_language_codes) == 0:
        langs = ( language_code, )
      else:
      # Replace "None" with the default language code
        i = _language_codes.index(None)
        if language_code in _language_codes:
          langs = filter(lambda l: l is not None, _language_codes)
        else:
          langs = _language_codes[:i] + ( language_code, ) + _language_codes[i + 1:]
      # Check for another instance of "None"
        if None in langs:
          raise ValueError(f'More than one of the supplied language_codes is None')
    else:
      langs = _language_codes

  # Fallback language is English ('en')
    if 'en' in _language_codes:
      self._langs = langs
    else:
      self._langs = ( *langs, 'en' )

    return None


class TranslationDomain(object):
  __slots__: ( '_domain', '_locdirpath' )

  def __init__(self, _domain: str) -> None:
    super().__init__()
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    assert isinstance(_domain, str), type(_domain)
    self._domain = _domain
#    moddirpath = os.path.dirname(os.path.abspath(__file__))
    framedirpath = os.path.dirname(os.path.abspath(inspect.currentframe().f_back.f_code.co_filename))
    self._locdirpath = os.path.join(framedirpath, 'i18n', 'locales')
    if not os.path.isdir(self._locdirpath):
      raise ValueError(f"Locale directory '{self._locdirpath}' does not exist")
    return None


class TranslationDomainLanguage(object):
# TranslationDomain with one of the languages from TranslationLanguages
  __slots__ = ( '_translation_domain', '_translation_languages', '_found_language' )

  @property
  def language(self):
    return self._found_language

  @property
  def key(self) -> str:
    return f'translation_domain: {self._translation_domain._domain} language_code: {self._found_language}'

  def __init__(self, _translation_domain: TranslationDomain, _translation_languages: TranslationLanguages) -> None:
    super().__init__()
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    assert isinstance(_translation_domain, TranslationDomain), type(_translation_domain)
    assert isinstance(_translation_languages, TranslationLanguages), type(_translation_languages)
    self._translation_domain = _translation_domain
    self._translation_languages = _translation_languages

    found_lang = None
    for l in _translation_languages._langs:
      mofilepath = os.path.join(_translation_domain._locdirpath, l, message_locale_category_dirname, f'{_translation_domain._domain}.mo')
      if os.path.isfile(mofilepath):
        logging.info(f"Found translation machine object file '{mofilepath}'")
        found_lang = l
        break
      else:
        logging.info(f"Translation machine object file '{mofilepath}' does not exist")

    if found_lang == None:

      found = False
      for l in _translation_languages._langs:
        pofilepath = os.path.join(_translation_domain._locdirpath, l, message_locale_category_dirname, f'{_translation_domain._domain}.po')
        if os.path.isfile(pofilepath):
          logging.info(f"Found translation portable object file '{pofilepath}'")
          found = True
          break
        else:
          logging.info(f"Translation portable object file '{pofilepath}' does not exist")
      if found:
        mofilepath = f"{pofilepath.rsplit('.', 1)[0]}.mo"
        raise FileNotFoundError(errno.ENOENT, f"Translation portable object file exists but machine object file does not exist - need to run msgfmt", pofilepath, None, mofilepath)
      else:
        raise FileNotFoundError(errno.ENOENT, f"Translation object files do not exist", _translation_domain._locdirpath)
# TO DO: if not found, fall back to customizable default language

    pofilepath = f"{mofilepath.rsplit('.', 1)[0]}.po"
    if os.path.getmtime(pofilepath) > os.path.getmtime(mofilepath):
      # exception OSError(errno, strerror[, filename[, winerror[, filename2]]])
      raise OSError(None, f"Translation portable object file is more recent than machine object file - need to run msgfmt", pofilepath, None, mofilepath)

    self._found_language = found_lang

    return None


class Translation(object):
  translations_dict: Final[dict] = dict()
  __slots__: ( '_translation_domain_language', '_translations' )
  # _translation - a gettext.GNUTranslations instance based on the domain, localedir, and languages (language codes)

  @property
  def language(self):
    return self._translation_domain_language.language

  def __init__(self, _translation_domain_language: TranslationDomainLanguage, *, frame_summary: traceback.FrameSummary = None) -> None:
    super().__init__()
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    assert isinstance(_translation_domain_language, TranslationDomainLanguage), f'Wrong type {type(_translation_domain_language).__qualname__} for translation_domain_language'
    if frame_summary == None:
      frame_summary = traceback.extract_stack(limit = 2)[0]
    self._translation_domain_language = _translation_domain_language

    key = str(_translation_domain_language.key)
    if key in Translation.translations_dict:

      ( original_frame_summary, self._translations ) = Translation.translations_dict[key]

      logging.warning(f'Already created Translation for ({key}) - reusing gettext.translation instance from cache')
      logging.warning(f'  Originally created at file "{original_frame_summary.filename}" line {original_frame_summary.lineno} in {original_frame_summary.name}')
      logging.warning(f'  Current invocation at file "{frame_summary.filename}" line {frame_summary.lineno} in {frame_summary.name}')

    else:

      self._original_frame_summary = frame_summary

      self._translations = gettext.translation(_translation_domain_language._translation_domain._domain, _translation_domain_language._translation_domain._locdirpath, languages =_translation_domain_language._translation_languages._langs, fallback = False)
        # fallback = True returns NullTranslation which returns the supplied message, not the default language
        # fallback = False raises OSError if no *.mo file is found
      logging.debug(f'domain: {_translation_domain_language._translation_domain._domain} language: {_translation_domain_language._found_language} _translations type: {type(self._translations)}') # gettext.GNUTranslations

      Translation.translations_dict[key] = ( frame_summary, self._translations )

    return None

  def get(self, _msgid: str, _text_dict: dict[str] = None):
    assert isinstance(_msgid, str)
    assert isinstance(_text_dict, dict | None)
    text = self._translations.gettext(_msgid)
    if _text_dict != None:
      text = text.format(**_text_dict)
    return text

#  def nget(self, _singular: str, _plural: str, _n: int, _text_dict: dict[str] = None, _person: PronounTranslation.PronounPersonEnum = None):
  def nget(self, _singular: str, _plural: str, _n: int, _text_dict: dict[str] = None, _person = None):
  # arguments - Optional string arguments which can be referenced in the message
  #             using the percent sign followed by the argument index %n.
  #             The count value is automatically included as the first argument (%1).
    assert isinstance(_singular, str)
    assert isinstance(_plural, str)
    assert isinstance(_n, int)
    assert isinstance(_text_dict, dict | None)
    assert isinstance(_person, PronounTranslation.PronounPersonEnum | None), type(_person)
#    assert isinstance(_gender, PronounTranslation.GenderEnum | None), type(_gender)
    n = 0 if _person in (PronounTranslation.PronounPersonEnum.First_Person, PronounTranslation.PronounPersonEnum.Second_Person) else _n
    text = self._translations.ngettext(_singular, _plural, n)
    index = text.find('{pronoun')
    if index != -1:
      placeholder = text[index : text.find('}', index) + 1]
      if _person == None:
        raise ValueError(f'PronounPerson must be specified when text contains {placeholder}')
# Neutral gender "they" can be singular, same as "he" or "she"
#      elif n == 1 and _person == PronounTranslation.PronounPersonEnum.Third_Person:
#        if _gender == None:
#          raise ValueError(f'Gender must be specified when text contains {placeholder}, n = 1 and person is {_person}')
#        elif _gender == PronounTranslation.GenderEnum.Neutral:
#          text = self._translations.ngettext(_singular, _plural, 0)
    if _text_dict != None:
      text = text.format(**_text_dict)
    return text


class PronounTranslation(Translation):
  PronounTypeEnum: Final[Enum] = Enum('PronounType', { 'Subject': 'subject', 'Object': 'object', 'Possessive': 'possessive', 'Reflexive': 'reflexive' } )
  PronounPersonEnum: Final[Enum] = Enum('PronounPerson', { 'First_Person': 'first', 'Second_Person': 'second', 'Third_Person': 'third' })
  GenderEnum: Final[Enum] = Enum('Gender', { 'Male': 'male', 'Female': 'female', 'Neutral': 'neutral' })
  __slots__ = ( )

  def __init__(self, _translation_languages: TranslationLanguages, *, frame_summary: traceback.FrameSummary = None) -> None:
    super().__init__(TranslationDomainLanguage(TranslationDomain('pronouns'), _translation_languages), frame_summary = traceback.extract_stack(limit = 2)[0] if frame_summary == None else frame_summary)
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    return None

  def _pronoun_or_determiner(self, _type: str, _person: PronounPersonEnum, _number: int, _gender: GenderEnum):
    assert isinstance(_type, str), type(_type)
    assert isinstance(_person, PronounTranslation.PronounPersonEnum), type(_person)
    assert isinstance(_number, int), type(_number)
    assert isinstance(_gender, PronounTranslation.GenderEnum | None), type(_gender)
    if _person == PronounTranslation.PronounPersonEnum.Third_Person and _number == 1 and _gender != PronounTranslation.GenderEnum.Neutral:
      if  _gender == None:
        raise ValueError('Gender must be specified when person is Third_Person and number of persons is 1')
      return self.get(f'{_person.value}_person/{_type}/{_gender.value}')
    else:
      msgid = f'{_person.value}_person/{_type}'
      return self.nget(msgid, msgid, _number)

  def pronoun(self, _type: PronounTypeEnum, _person: PronounPersonEnum, _number: int = 1, *, gender: GenderEnum = None):
    return self._pronoun_or_determiner(_type.value, _person, _number, gender)

  def pronoun_subject(self, _person: PronounPersonEnum, _number: int = 1, *, gender: GenderEnum = None):
    return self._pronoun_or_determiner(PronounTranslation.PronounTypeEnum.Subject.value, _person, 1 if _number == 1 else 0, gender)

  def determiner(self, _person: PronounPersonEnum, _number: int = 1, /, gender: GenderEnum = None):
    return self._pronoun_or_determiner('determiner', _person, _number, gender)


class TranslationContext(object):
  __slots__: ( '_translation', '_context' )

  @property
  def language(self):
    return self._translation.language

  def __init__(self, _translation: Translation, _context: str) -> None:
    super().__init__()
    logging.debug(f'{self.__class__.__qualname__} {inspect.currentframe().f_code.co_qualname}')
    assert isinstance(_translation, Translation), f'Wrong type {type(_translation).__qualname__} for translation'
    assert isinstance(_context, str), f'Wrong type {type(_context).__qualname__} for context'
    self._translation = _translation
    self._context = _context
    return None

  def get(self, _msgid: str, _text_dict: dict[str] = None):
    assert isinstance(_msgid, str)
    assert isinstance(_text_dict, dict | None)
    text = self._translation._translations.pgettext(self._context, _msgid)
    if _text_dict != None:
      text = text.format(**_text_dict)
    return text

  def nget(self, _singular: str, _plural: str, _n: int, _text_dict: dict[str] = None, _person: PronounTranslation.PronounPersonEnum = None):
  # arguments - Optional string arguments which can be referenced in the message
  #             using the percent sign followed by the argument index %n.
  #             The count value is automatically included as the first argument (%1).
    assert isinstance(_singular, str)
    assert isinstance(_plural, str)
    assert isinstance(_n, int)
    assert isinstance(_text_dict, dict | None)
    assert isinstance(_person, PronounTranslation.PronounPersonEnum | None), type(_person)
#    assert isinstance(_gender, PronounTranslation.GenderEnum | None), type(_gender)
    n = 0 if _person in (PronounTranslation.PronounPersonEnum.First_Person, PronounTranslation.PronounPersonEnum.Second_Person) else _n
    text = self._translation._translations.npgettext(self._context, _singular, _plural, n)
    index = text.find('{pronoun')
    if index != -1:
      placeholder = text[index : text.find('}', index) + 1]
      if _person == None:
        raise ValueError(f'PronounPerson must be specified when text contains {placeholder}')
# Neutral gender "they" can be singular, same as "he" or "she"
#      elif n == 1 and _person == PronounTranslation.PronounPersonEnum.Third_Person:
#        if _gender == None:
#          raise ValueError(f'Gender must be specified when text contains {placeholder}, n = 1 and person is {_person}')
#        elif _gender == PronounTranslation.GenderEnum.Neutral:
#          text = self._translations.ngettext(_singular, _plural, 0)
    if _text_dict != None:
      text = text.format(**_text_dict)
    return text
