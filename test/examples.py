# examples.py
#
# License: GNU LESSER GENERAL PUBLIC LICENSE
#   https://www.gnu.org/software/gettext/manual/html_node/GNU-LGPL.html
#
# This file and its contents and all others related to this software are provided
# AS IS, WITHOUT ANY WARRANTY OR CONDITION, EXPRESS OR IMPLIED.

import asyncio, i18n, logging
from enum import Enum
from typing import Final
from test.sample_strings import people, StringWithPronoun
from i18n import PronounTranslation


master_locale: str = 'en'
test_language_lists = ( ( None,), ( 'en', ), ( 'en_US', 'en' ) )
  # None defaults to locale.getlocale(category = locale.LC_CTYPE)


async def main() -> None:

    done_langs = set()
    text_dict = dict()

    for langs in test_language_lists:

      for l in langs:
        assert isinstance(l, str | None), l
    # The following code is a good example use - part 1
      t_langs = i18n.TranslationLanguages(*langs)

      pt = t_langs.pronouns
        # generates warning if same language as a prior loop iteration

      ctc = t_langs.conjunctions
      and_conj = ctc.get('and')

      test_td = i18n.TranslationDomain('test')
      test_tdl = i18n.TranslationDomainLanguage(test_td, t_langs)
      if test_tdl.language in done_langs:
        break
      else:
        done_langs.add(test_tdl.language)

      tt = i18n.Translation(test_tdl)
        # generates warning if same language as a prior loop iteration

      text_dict.clear()

      print('')
      print(f"== Strings without context, language = '{tt.language}' from {langs} ==")

      prev_person = None
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

          if s.person != prev_person:
            print(f'-- {s.person} --')
          print(tt.get(s.msgid, text_dict))
          prev_person = s.person

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
            text_dict['food'] = 'a burger' if n % 2 == 0 else 'pizza'

            if s.person != prev_person:
              print(f'-- {s.person} --')
            print(tt.nget(s.msgid, s.msgid_plural, n, text_dict, s.person))
            prev_person = s.person

      for context, value in StringWithPronoun.strings_with_context_dict.items():
        assert isinstance(context, str), type(key)
        assert isinstance(value, list), type(value)

        ttc = i18n.TranslationContext(tt, context)

        print('')
        print(f"== Strings with context '{context}', language = '{ttc.language}' from {langs} ==")

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

            if s.person != prev_person:
              print(f'-- {s.person} --')
            print(ttc.get(s.msgid, text_dict))
            prev_person = s.person

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
              text_dict['food'] = 'a burger' if n % 2 == 0 else 'pizza'

              if s.person != prev_person:
                print(f'-- {s.person} --')
              print(ttc.nget(s.msgid, s.msgid_plural, n, text_dict, s.person))
              prev_person = s.person

    # People

      print('')
      print('== People ==')
      print('')

      msgid = '/sentence/with_pronoun/subject/test1'
      msgid_plural = msgid
      pronoun_type = PronounTranslation.PronounTypeEnum.Subject
      pronoun_person = PronounTranslation.PronounPersonEnum.Third_Person

      people_dict = { 'chicken': [], 'tacos': [], 'pizza': [], 'a burger': [] }
      i = 0
      for j in range(2, 15, 4):
        while i < j:
          p = people[i]
          people_dict[p.always_orders].append(p)
          i += 1
        for food, who_likes_it in people_dict.items():
        # The following code is a good example use - part 2
          if len(who_likes_it) > 0:
            n = len(who_likes_it)
            text_dict.clear()
            text_dict['names'] = f' {and_conj} '.join(', '.join(p.name for p in who_likes_it).rsplit(', ', 1))
            text_dict['food'] = food

          # With names as first subject
            if n == 1:
              text_dict['pronoun'] = pt.pronoun(pronoun_type, pronoun_person, n, gender = who_likes_it[0].gender)
            else:
              text_dict['pronoun'] = pt.pronoun(pronoun_type, pronoun_person, n)
            print(tt.nget(msgid, msgid_plural, n, text_dict, pronoun_person))

          # With pronoun rather than names as first subject
            if n == 1:
              text_dict['names'] = pt.pronoun_subject(pronoun_person, n, gender = who_likes_it[0].gender)
            else:
              text_dict['names'] = pt.pronoun_subject(pronoun_person, n)
            print(tt.nget(msgid, msgid_plural, n, text_dict, pronoun_person))

    print('')
    return None


mainName = '__main__'

if __name__ != mainName:
  print(f'Main routine name is not expected "{mainName}" __name__: {__name__}')
else:

  logger = logging.getLogger(mainName)
  logging_format = '%(filename)-7s %(lineno)-4d %(funcName)-8s %(levelname)-8s %(message)s'
  logging.basicConfig(format = logging_format, level = logging.WARNING)
  logging.info(f'Main routine __name__: "{__name__}" root logger mainName: "{mainName}" effectiveLevel = {logger.getEffectiveLevel()}')
    # NOTSET: 0, DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50

  asyncio.run(main(), debug = None) # respect global debug mode settings
