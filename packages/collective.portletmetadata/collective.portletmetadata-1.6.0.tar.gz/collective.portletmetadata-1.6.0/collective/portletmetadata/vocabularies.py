from collective.portletmetadata.interfaces import IMetadataSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class CssClassesVocabulary(object):
    """Vocabulary for css classes, stored in the registry."""

    def __call__(self, context):
        result = []

        try:
            settings = getUtility(IRegistry).forInterface(IMetadataSettings)
        except Exception:
            return SimpleVocabulary(result)

        if settings.css_classes:
            for css_class in settings.css_classes:
                value = css_class
                if "|" in css_class:
                    value, title = css_class.split("|", 1)
                else:
                    value = title = css_class
                result.append(SimpleTerm(value=value, title=title))

        return SimpleVocabulary(result)
