# International Translation Classes for Python (python-i18n)

## Description

This project provides classes for internationalization of text in Python code.
It uses GNU gettext as the basis for translations but provides for some additional features:
* Translated text can contain placeholders that are replaced by values of variables in code.
* Support for insertion of translated forms of pronouns (I, me, we, us, they, them, etc.) is directly supported.
* Structured msgids are used in the translation files.
The structured msgids assist in translation by providing information about the
person (first person, second person, third person) and
part of speech (subject, object, reflexive, possessive, possessive determiner)
for replacement of placeholders in the text.

## Installation

Currently, python-i18n can be installed from the source code as follows:

Change to the python-i18n directory and run pip install:


   ```
   pip install -e .
   ```
   
   or

   ```
   python3 -m pip install -e .
   ```

## Translation Files

The translation files follow the GNU gettext format.
However, Python-style (`format`) placeholders (names enclosed by curly braces) can be added.

### Translation Domains

Translation files should be organized by the applications or subsets of applications
where they will be used.
The term "domain" (meaning "a sphere of influence") refers to a name that identifies a specific set of text strings to be translated.
Text strings that are shared among multiple applications and/or subsets of applications
will share the same translation files by referring to the name of the domain.

For example, if three applications (A, B and C) use various strings
(a through z, where the single lower case letters represent the entire strings)
as follows:

* Applicaiton A uses strings a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r
* Application B uses strings a, b, c, d, e, f, g, h, i, s, t, u, v, w, x, y, z
* Application C uses strings j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

Then the translation files could be organized into three domains:

* domain "one" with the strings: a, b, c, d, e, f, g, h, i

* domain "two" with the strings: j, k, l, m, n, o, p, q, r

* and domain "three" with the strings: s, t, u, v, w, x, y, z

Application A would use domains "one" and "two",
Application B would use domains "one" and "three", and
Application C would use domains "two" and "three".

### Placeholders

* Placeholders for pronouns should start with `{pronoun`, for example:

    `{pronoun}`

    `{pronoun1}`

    `{pronoun2}`

    `{pronoun-for-actor}`

    Other placeholders should _not_ start with `{pronoun`.
    
    Call `PronounTranslation.pronoun(...)` to get the value to replace the `pronoun` placeholders.
    
    Sentences may also contain placeholders for names (`{names}` in the examples), which are used as subjects.
    These names could also be replaced with pronouns, by calling
    `PronounTranslation.pronoun_subject(...)` to get the value to replace the `names` placeholders.

## Providing Translated Text Strings

1. Under the directory containing the Python code that will call the translation methods,
    create the necessary directory structure. The first subdirectory should be `i18n`
    followed by `locales`, then the language code(s), and finally `LC_MESSAGES`.

    For example, for the translation files for the English language:

    ```
    mkdir -p i18n/locales/en/LC_MESSAGES
    ```

2. Create a `*.po` file for each domain, where the name of the file is the name of the domain.
    For example:

    File path: `src/i18n/locales/en/LC_MESSAGES/my-domain.po`

    The beginning of the file should look like this:

    ```
    msgid ""
    msgstr ""
    "Project-Id-Version: my-project 1.0\n"
    "PO-Revision-Date: yyyy-mm-dd hh:mm-zzzz\n"
    "Last-Translator: Name <name@domain.com>\n"
    "Language-Team: English <english@domain.com>\n"
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "Language: en\n"
    "Plural-Forms: nplurals=2; plural=n != 1;\n"
    ```

    Values such as the project name (`my-project`),
    the `PO-Revision-Date` date (`yyyy-mm-dd`), time (`hh:mm`) and time zone (`-zzzz`),
    and language (`English`, `en`) should be customized.

3. Add the translation strings in GNU gettext format, with or without plurals
    and with or without a context, as in these examples:

    ```
    msgid "/sentence/simple"
    msgstr "This is a simple sentence."
    ```

    ```
    msgid "/sentence/with_pronoun/subject/test1"
    msgid_plural "/sentence/with_pronoun/test1"
    msgstr[0] "When {names} goes out to eat, {pronoun} usually orders {food}."
    msgstr[1] "When {names} go out to eat, {pronoun} usually order {food}."
    ```

    with context:

    ```
    msgctxt "my-context"
    msgid "/sentence/simple"
    msgstr "This is a simple sentence."
    ```

    ```
    msgctxt "my-context"
    msgid "/sentence/with_pronoun/subject/test1"
    msgid_plural "/sentence/with_pronoun/test1"
    msgstr[0] "When {names} goes out to eat, {pronoun} usually orders {food}."
    msgstr[1] "When {names} go out to eat, {pronoun} usually order {food}."
    ```

    The `msgid` could also be a text string, possibly extracted
    from the code using `pygettext.py`.

4. Use `msgfmt` to compile the portable object (`*.po`) files to machine object (`*.mo`) format:

    `msgfmt `
    `msgfmt --check --output-file i18n/locales/xx/LC_MESSAGES/my-domain.mo i18n/locales/xx/LC_MESSAGES/my-domain`
    
    where `xx` is the language code.

## Example of Use

Part of the code in `test/examples.py` provides a good example of how to use the translation classes.

Running `text/examples.py` shows the type of output that can be produced.
Some good examples of this output:

```
== Strings without context, language = 'en' from (None,) ==
-- PronounPerson.First_Person --
When I go out to eat, I usually order pizza.
When we go out to eat, we all usually order pizza.
-- PronounPerson.Second_Person --
(Singular "you") When you go out to eat, you usually order pizza.
(Plural "you") When you go out to eat, you all usually order pizza.
-- PronounPerson.Third_Person --
When John goes out to eat, he usually orders pizza.
When Jane goes out to eat, she usually orders pizza.
When John and Jane go out to eat, they both usually order a burger.
When they go out to eat, they all usually order pizza.

== Strings with context 'test_context', language = 'en' from (None,) ==
-- PronounPerson.First_Person --
When I go out to eat, I usually order pizza.
When we go out to eat, we all usually order pizza.
-- PronounPerson.Second_Person --
When you go out to eat, you usually order pizza.
When you go out to eat, you both usually order a burger.
When you go out to eat, you all usually order pizza.
-- PronounPerson.Third_Person --
When John goes out to eat, he usually orders pizza.
When Jane goes out to eat, she usually orders pizza.
When they go out to eat, they all usually order pizza.

== People ==

When John goes out to eat, he usually orders pizza.
When he goes out to eat, he usually orders pizza.
When Jane goes out to eat, she usually orders a burger.
When she goes out to eat, she usually orders a burger.
When Jane and Karen go out to eat, they both usually order a burger.
When they go out to eat, they both usually order a burger.
When Jamie and Lou go out to eat, they both usually order chicken.
When they go out to eat, they both usually order chicken.
When Jordan and Lisa go out to eat, they both usually order tacos.
When they go out to eat, they both usually order tacos.
When John, Kenny and Martin go out to eat, they all usually order pizza.
When they go out to eat, they all usually order pizza.
When Jane, Karen and Mary go out to eat, they all usually order a burger.
When they go out to eat, they all usually order a burger.
When Jamie, Lou and Nate go out to eat, they all usually order chicken.
When they go out to eat, they all usually order chicken.
When Jordan, Lisa and Nancy go out to eat, they all usually order tacos.
When they go out to eat, they all usually order tacos.
When John, Kenny, Martin and Paul go out to eat, they all usually order pizza.
When they go out to eat, they all usually order pizza.
When Jane, Karen, Mary and Penny go out to eat, they all usually order a burger.
When they go out to eat, they all usually order a burger.
```

## Current Status

This project currently provides translations for the following languages:

* English only

Volunteers for translation to other languages are welcome.

## Adding Support for Additional Languages

1. For a new language, create the directory structure for the new language and
    copy any existing `*.po`files from the locale subdirectory (ex: `en`)
    for the language to be translated from. For example:

    ```
    mkdir -p src/i18n/i18n/locales/xx/LC_MESSAGES
    cp src/i18n/i18n/locales/xx/LC_MESSAGES/*.po src/i18n/i18n/locales/xx/LC_MESSAGES
    ```

    where `xx` is the new language.

2. Edit the `*.po` files to change the translated strings to the new language.

3. Use `msgfmt` to compile the portable object (`*.po`) files to machine object (`*.mo`) format:

    ```
    msgfmt --check --output-file src/i18n/i18n/locales/xx/LC_MESSAGES/i18n.mo src/i18n/i18n/locales/xx/LC_MESSAGES/i18n
    msgfmt --check --output-file src/i18n/i18n/locales/xx/LC_MESSAGES/pronouns.mo src/i18n/i18n/locales/xx/LC_MESSAGES/pronouns
    ```

# License

The files in this project and their contents are licensed under the
[GNU LESSER GENERAL PUBLIC LICENSE](https://www.gnu.org/software/gettext/manual/html_node/GNU-LGPL.html)
and are provided
AS IS, WITHOUT ANY WARRANTY OR CONDITION, EXPRESS OR IMPLIED.
