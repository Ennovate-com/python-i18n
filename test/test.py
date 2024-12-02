# test.py
#
# License: GNU LESSER GENERAL PUBLIC LICENSE
#   https://www.gnu.org/software/gettext/manual/html_node/GNU-LGPL.html
#
# This file and its contents and all others related to this software are provided
# AS IS, WITHOUT ANY WARRANTY OR CONDITION, EXPRESS OR IMPLIED.

import i18n, logging, unittest
from typing import ClassVar, Final
from test.sample_strings import people, StringWithPronoun


master_locale: str = 'en'

t_langs = i18n.TranslationLanguages()
if t_langs._langs[0] in ( 'en_us', 'en' ):
  test_language_lists = ( ( None,), ( 'en', ), ( 'en_US', 'en' ) )
    # None defaults to locale.getlocale(category = locale.LC_CTYPE)
    # Currently have only English translations
else:
  test_language_lists = ( ( 'en', ), ( 'en_US', 'en' ) )


class TestPronouns(unittest.TestCase):

  @staticmethod
  def get_translation(key: str):
    match key:
      case 'en 2 1 PronounPerson.Third_Person pizza male':
        return 'When John goes out to eat, he usually orders pizza.'
      case 'en 2 1 PronounPerson.Third_Person a burger female':
        return 'When Jane goes out to eat, she usually orders a burger.'
      case 'en 6 1 PronounPerson.Third_Person chicken neutral':
        return 'When Jamie goes out to eat, they usually orders chicken.'
      case 'en 6 1 PronounPerson.Third_Person tacos neutral':
        return 'When Jordan goes out to eat, they usually orders tacos.'
      case 'en 6 2 PronounPerson.Third_Person pizza':
        return 'When John and Kenny go out to eat, they both usually order pizza.'
      case 'en 6 2 PronounPerson.Third_Person a burger':
        return 'When Jane and Karen go out to eat, they both usually order a burger.'
      case 'en 10 2 PronounPerson.Third_Person chicken':
        return 'When Jamie and Lou go out to eat, they both usually order chicken.'
      case 'en 10 2 PronounPerson.Third_Person tacos':
        return 'When Jordan and Lisa go out to eat, they both usually order tacos.'
      case 'en 10 3 PronounPerson.Third_Person pizza':
        return 'When John, Kenny and Martin go out to eat, they all usually order pizza.'
      case 'en 10 3 PronounPerson.Third_Person a burger':
        return 'When Jane, Karen and Mary go out to eat, they all usually order a burger.'
      case 'en 14 3 PronounPerson.Third_Person chicken':
        return 'When Jamie, Lou and Nate go out to eat, they all usually order chicken.'
      case 'en 14 3 PronounPerson.Third_Person tacos':
        return 'When Jordan, Lisa and Nancy go out to eat, they all usually order tacos.'
      case 'en 14 4 PronounPerson.Third_Person pizza':
        return 'When John, Kenny, Martin and Paul go out to eat, they all usually order pizza.'
      case 'en 14 4 PronounPerson.Third_Person a burger':
        return 'When Jane, Karen, Mary and Penny go out to eat, they all usually order a burger.'
      case 'en 1 pizza male':
        return 'When he goes out to eat, he usually orders pizza.'
      case 'en 1 a burger female':
        return 'When she goes out to eat, she usually orders a burger.'
      case 'en 1 chicken neutral':
        return 'When they goes out to eat, they usually orders chicken.'
      case 'en 1 tacos neutral':
        return 'When they goes out to eat, they usually orders tacos.'
      case 'en 2 pizza':
        return 'When they go out to eat, they both usually order pizza.'
      case 'en 2 a burger':
        return 'When they go out to eat, they both usually order a burger.'
      case 'en 2 chicken':
        return 'When they go out to eat, they both usually order chicken.'
      case 'en 2 tacos':
        return 'When they go out to eat, they both usually order tacos.'
      case 'en >2 pizza':
        return 'When they go out to eat, they all usually order pizza.'
      case 'en >2 a burger':
        return 'When they go out to eat, they all usually order a burger.'
      case 'en >2 chicken':
        return 'When they go out to eat, they all usually order chicken.'
      case 'en >2 tacos':
        return 'When they go out to eat, they all usually order tacos.'
      case _:
        raise ValueError(f"Translation not found for '{key}'")

  def test_pronoun_strings_without_context(self) -> None:

    text_dict = dict()

    done_langs = set()

    for langs in list(dict.fromkeys(test_language_lists)):

      for l in langs:
        assert isinstance(l, str | None), l
      t_langs = i18n.TranslationLanguages(*langs)

      pt = t_langs.pronouns
        # generates warning if same language as another test

      ctc = t_langs.conjunctions
      and_conj = ctc.get('and')

      test_td = i18n.TranslationDomain('test')
      test_tdl = i18n.TranslationDomainLanguage(test_td, t_langs)
      if test_tdl.language in done_langs:
        break
      else:
        done_langs.add(test_tdl.language)

      tt = i18n.Translation(test_tdl)
        # generates warning if same language as another test

      for s in StringWithPronoun.strings_without_context:

        if s.numbers == None:

          text_dict.clear()
          if s.person == None:
            text_dict['determiner'] = pt.determiner(s.person, gender = s.gender)
          else:
            with self.subTest(langs = langs, pronoun_type = s.pronoun_type, person = s.person, gender = s.gender):
              text_dict['pronoun'] = pt.pronoun(s.pronoun_type, s.person, gender = s.gender)
          if s.names == None:
            with self.subTest(langs = langs, pronoun_type = s.pronoun_type, person = s.person, gender = s.gender):
              text_dict['names'] = pt.pronoun_subject(s.person, gender = s.gender)
          else:
            text_dict['names'] = f' {and_conj} '.join(', '.join(name for name in s.names).rsplit(', ', 1))
          text_dict['food'] = 'pizza'

          with self.subTest(langs = langs, msgid = s.msgid):
            self.assertEqual(tt.get(s.msgid, text_dict), s.get_translation_for_language(t_langs._langs[0]))
              # t_langs - after None in _language_codes has been replaced in _TranslationLanguages.__init__

        else:
          for n in s.numbers:

            text_dict.clear()
            if s.person == None:
              text_dict['determiner'] = pt.determiner(s.person, n, gender = s.gender)
            else:
              text_dict['pronoun'] = pt.pronoun(s.pronoun_type, s.person, n, gender = s.gender)
            if s.names == None:
              text_dict['names'] = pt.pronoun_subject(s.person, n, gender = s.gender)
            else:
              text_dict['names'] = f' {and_conj} '.join(', '.join(name for name in s.names).rsplit(', ', 1))
            text_dict['food'] = 'pizza'

            with self.subTest(langs = langs, msgid = s.msgid, n = n, person = s.person, gender = s.gender):
              self.assertEqual(tt.nget(s.msgid, s.msgid_plural, n, text_dict, s.person), s.get_translation_for_language(t_langs._langs[0]))
                # t_langs - after None in _language_codes has been replaced in _TranslationLanguages.__init__

    return None

  def test_pronoun_strings_with_context(self) -> None:

    text_dict = dict()

    done_langs = set()

    for langs in list(dict.fromkeys(test_language_lists)):

      for l in langs:
        assert isinstance(l, str | None), l
      t_langs = i18n.TranslationLanguages(*langs)

      pt = t_langs.pronouns
        # generates warning if same language as another test

      ctc = t_langs.conjunctions
      and_conj = ctc.get('and')

      test_td = i18n.TranslationDomain('test')
      test_tdl = i18n.TranslationDomainLanguage(test_td, t_langs)
      if test_tdl.language in done_langs:
        break
      else:
        done_langs.add(test_tdl.language)

      tt = i18n.Translation(test_tdl)
        # generates warning if same language as another test

      for context, value in StringWithPronoun.strings_with_context_dict.items():
        assert isinstance(context, str), type(key)
        assert isinstance(value, list), type(value)

        ttc = i18n.TranslationContext(tt, context)

        for s in value:

          if s.numbers == None:

            text_dict.clear()
            if s.person == None:
              text_dict['determiner'] = pt.determiner(s.person, gender = s.gender)
            else:
              text_dict['pronoun'] = pt.pronoun(s.pronoun_type, s.person, gender = s.gender)
            if s.names == None:
              text_dict['names'] = pt.pronoun_subject(s.person, gender = s.gender)
            else:
              text_dict['names'] = f' {and_conj} '.join(', '.join(name for name in s.names).rsplit(', ', 1))
            text_dict['food'] = 'pizza'

            with self.subTest(context = context, langs = langs, msgid = s.msgid):
              self.assertEqual(ttc.get(s.msgid, text_dict), s.get_translation_for_language(t_langs._langs[0]))
                # t_langs - after None in _language_codes has been replaced in _TranslationLanguages.__init__

          else:
            for n in s.numbers:

              text_dict.clear()
              if s.person == None:
                text_dict['determiner'] = pt.determiner(s.person, n, gender = s.gender)
              else:
                text_dict['pronoun'] = pt.pronoun(s.pronoun_type, s.person, n, gender = s.gender)
              if s.names == None:
                text_dict['names'] = pt.pronoun_subject(s.person, n, gender = s.gender)
              else:
                text_dict['names'] = f' {and_conj} '.join(', '.join(name for name in s.names).rsplit(', ', 1))
              text_dict['food'] = 'pizza'

              with self.subTest(context = context, langs = langs, msgid = s.msgid, n = n, person = s.person, gender = s.gender):
                self.assertEqual(ttc.nget(s.msgid, s.msgid_plural, n, text_dict, s.person), s.get_translation_for_language(t_langs._langs[0]))
                  # t_langs - after None in _language_codes has been replaced in _TranslationLanguages.__init__

    return None

  def test_persons_without_context(self) -> None:

    text_dict = dict()

    msgid = '/sentence/with_pronoun/subject/test1'
    msgid_plural = msgid
    pronoun_type = i18n.PronounTranslation.PronounTypeEnum.Subject
    pronoun_person = i18n.PronounTranslation.PronounPersonEnum.Third_Person

    done_langs = set()

    for langs in list(dict.fromkeys(test_language_lists)):

      for l in langs:
        assert isinstance(l, str | None), l
      t_langs = i18n.TranslationLanguages(*langs)

      pt = t_langs.pronouns
        # generates warning if same language as another test

      ctc = t_langs.conjunctions
      and_conj = ctc.get('and')

      test_td = i18n.TranslationDomain('test')
      test_tdl = i18n.TranslationDomainLanguage(test_td, t_langs)
      if test_tdl.language in done_langs:
        break
      else:
        done_langs.add(test_tdl.language)

      tt = i18n.Translation(test_tdl)
        # generates warning if same language as another test

      people_dict = { 'pizza': [], 'a burger': [], 'chicken': [], 'tacos': [] }
      i = 0
      for j in range(2, 15, 4):

        while i < j:
          p = people[i]
          people_dict[p.always_orders].append(p)
          i += 1

        for food, who_likes_it in people_dict.items():

          n = len(who_likes_it)
          if n == 0:
            break

          text_dict.clear()
          if n == 1:
            text_dict['pronoun'] = pt.pronoun(pronoun_type, pronoun_person, n, gender = who_likes_it[0].gender)
            gender = f' {who_likes_it[0].gender.value}'
          else:
            text_dict['pronoun'] = pt.pronoun(pronoun_type, pronoun_person, n)
            gender = ''
          text_dict['food'] = food

        # With pronoun rather than names as first subject
          text_dict['names'] = f' {and_conj} '.join(', '.join(p.name for p in who_likes_it).rsplit(', ', 1))
          key = f'{tt.language} {j} {n} {pronoun_person} {food}{gender}'
          with self.subTest(lang = tt.language, j = j, n = n, pronoun_person = pronoun_person, gender = who_likes_it[0].gender if n == 1 else None, food = food):
            self.assertEqual(tt.nget(msgid, msgid_plural, n, text_dict, pronoun_person), TestPronouns.get_translation(key))

        # With pronoun rather than names as first subject
          if n == 1:
            text_dict['names'] = pt.pronoun_subject(pronoun_person, n, gender = who_likes_it[0].gender)
          else:
            text_dict['names'] = pt.pronoun_subject(pronoun_person, n)
          key = f"{tt.language} {'>2' if n > 2 else n} {food}{gender}"
          with self.subTest(lang = tt.language, j = j, n = n, pronoun_person = pronoun_person, gender = who_likes_it[0].gender if n == 1 else None, food = food):
            self.assertEqual(tt.nget(msgid, msgid_plural, n, text_dict, pronoun_person), TestPronouns.get_translation(key))

    return None


mainName = '__main__'

if __name__ != mainName:
  print(f'Main routine name is not expected "{mainName}" __name__: {__name__}')
else:

  logger = logging.getLogger(mainName)
  assert logger.name == '__main__', logger.name
# Tests use root logger rather than "__main__" logger
  logging.getLogger(None).setLevel(logging.ERROR)
# Suppress warnings from all loggers
#  logging.disable(logging.WARNING)
  logging.info(f'Main routine __name__: "{__name__}" root logger mainName: "{mainName}" effectiveLevel = {logger.getEffectiveLevel()}')
    # NOTSET: 0, DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50

  unittest.main()
