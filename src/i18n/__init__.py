# src/i18n/__init__.py
#
# Usage:
# import {modname}
# from {modname} import {ClassName}, {ClassName}, ...

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .text import PronounTranslation, Translation, TranslationContext, TranslationDomain, TranslationDomainLanguage, TranslationLanguages
