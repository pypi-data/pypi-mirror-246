from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer

import collective.portletmetadata


# The 'tests' directory is a package with zcml and a GS profile,
# which loads the zcml of our main package as well, and installs it.
FIXTURE = PloneWithPackageLayer(
    zcml_package=collective.portletmetadata.tests,
    zcml_filename="configure.zcml",
    gs_profile_id="collective.portletmetadata.tests:default",
    name="CollectivePortletMetadataFixture",
)
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="CollectivePortletMetadata:IntegrationTesting",
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="CollectivePortletMetadata:FunctionalTesting",
)
