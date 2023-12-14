from .messagefactory import MessageFactory as _
from plone.autoform import directives as form
from zope import schema
from zope.interface import Interface


class IBrowserLayer(Interface):
    """browser layer for the collective.portletmetadata package"""


class IMetadataSettings(Interface):
    """Global site specific settings"""

    css_classes = schema.Tuple(
        title=_("CSS Classes"),
        description=_(
            "Please enter the list of CSS classes, one per line. "
            "Format: class or class|descriptive title."
        ),
        required=False,
        value_type=schema.TextLine(),
    )


class IPortletMetadata(Interface):
    """Schema for portlet metadata"""

    is_local = schema.Bool(title=_("Local portlet"), description=_(" "), required=False)

    css_class = schema.Choice(
        title=_("CSS class"),
        description=_(" "),
        vocabulary="collective.portletmetadata.CssClasses",
        required=False,
    )

    custom_css_classes = schema.TextLine(
        title=_("Custom CSS classes"),
        description=_(
            "Freely add any (Bootstrap) classes, "
            "on top of the restricted classes above."
        ),
        required=False,
    )
    form.write_permission(
        custom_css_classes="collective.portletmetadata.ManageMetadata"
    )

    exclude_search = schema.Bool(
        title=("Exclude from search"),
        description=_(" "),
        required=False,
        default=True,
    )
