from collective.portletmetadata.testing import FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from unittest import TestCase

import transaction


class TestFunctional(TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        # We have a Search portlet on the left.
        self.metadata_url = (
            f"{self.portal_url}/++contextportlets++plone.leftcolumn"
            "/testportlet.search/edit-portlet-metadata"
        )
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        # Create an extra Folder so we can test making a portlet local.
        self.portal.invokeFactory("Folder", id="folder", title="Test Folder")
        transaction.commit()

    def get_browser(self):
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization", f"Basic {TEST_USER_NAME}:{TEST_USER_PASSWORD}"
        )
        browser.handleErrors = False
        return browser

    def test_search_portlet_appears(self):
        # Test the situation before doing any changes.
        # Open the portal, check that the search portlet is there.
        browser = self.get_browser()
        browser.open(self.portal_url)
        self.assertIn("portal-column-one", browser.contents)
        self.assertIn("portletSearch", browser.contents)

        # Open the test folder, check that the search portlet is there.
        browser.open(f"{self.portal_url}/folder")
        self.assertIn("portal-column-one", browser.contents)
        self.assertIn("portletSearch", browser.contents)

        # By default there is no hint for Google to exclude this part of the page
        # from search.
        self.assertNotIn("googleoff", browser.contents)
        self.assertNotIn("googleon", browser.contents)

        # There should not be a "None" CSS class.
        self.assertNotIn('class="None', browser.contents)

    def test_manage_portlets_view(self):
        # Test the situation before doing any changes.
        # Manage the portlets in the left column of the portal.
        # This should contain a link to edit the metadata of this portlet.
        browser = self.get_browser()
        browser.open(f"{self.portal_url}/@@topbar-manage-portlets/plone.leftcolumn")
        # TODO Strangely the portlet *itself* does not even show up here.
        # self.assertIn("portletmanager-plone-leftcolumn", browser.contents)
        # self.assertIn(self.metadata_url, browser.contents)

        # Open the metadata, check that expected options are there.
        browser.open(self.metadata_url)

        # local portlet
        local = browser.getControl(label="Local portlet")
        self.assertFalse(local.selected)

        # CSS with values from control panel, currently empty.
        css = browser.getControl(label="CSS class")
        self.assertEqual(css.value, ["--NOVALUE--"])
        self.assertEqual(css.options, ["--NOVALUE--"])

        # Custom free CSS classes
        custom_css = browser.getControl(label="Custom CSS classes")
        self.assertFalse(custom_css.value)

        # Exclude from (Google) search
        exclude = browser.getControl(label="Exclude from search")
        self.assertTrue(exclude.selected)

        # We have a Save button.
        self.assertTrue(browser.getControl(label="Save"))

    def test_css_classes(self):
        # Site admin can see our control panel:
        browser = self.get_browser()
        browser.open(f"{self.portal_url}/@@overview-controlpanel")
        cp_url = f"{self.portal_url}/@@portletmetadata-controlpanel"
        self.assertIn(cp_url, browser.contents)

        # Open it and add CSS classes.
        browser.open(cp_url)
        textarea = browser.getControl(label="CSS Classes")
        wanted_value = "fs-1 p-3|Large font\nfs-3 p-2"
        textarea.value = wanted_value
        browser.getControl(label="Save").click()

        # Reload to check that the value is really saved.
        browser.open(cp_url)
        textarea = browser.getControl(label="CSS Classes")
        self.assertEqual(textarea.value, wanted_value)

        # Open the metadata portlet settings and edit the CSS class fields.
        browser.open(self.metadata_url)

        # CSS with values from control panel
        css = browser.getControl(label="CSS class")
        self.assertEqual(css.value, ["--NOVALUE--"])
        self.assertEqual(css.options, ["--NOVALUE--", "fs-1 p-3", "fs-3 p-2"])
        css.value = ["fs-1 p-3"]

        # Custom free CSS classes
        custom_css = browser.getControl(label="Custom CSS classes")
        self.assertFalse(custom_css.value)
        custom_css.value = "m-1 text-decoration-underline"

        browser.getControl(label="Save").click()

        # Check the effect on the search portlet as shown in the folder.
        browser.open(f"{self.portal_url}/folder")
        self.assertIn("portal-column-one", browser.contents)
        self.assertIn("portletSearch", browser.contents)
        self.assertIn(
            'class="fs-1 p-3 m-1 text-decoration-underline"', browser.contents
        )

    def test_local_portlet(self):
        # Make our test portlet a local portlet.
        browser = self.get_browser()
        browser.open(self.metadata_url)
        local = browser.getControl(label="Local portlet")
        local.selected = True
        browser.getControl(label="Save").click()

        # It should still be visible on the site root.
        browser.open(self.portal_url)
        self.assertIn("portal-column-one", browser.contents)
        self.assertIn("portletSearch", browser.contents)

        # It should no longer appear in the folder.
        browser.open(f"{self.portal_url}/folder")

        # The column is there, but it is empty.
        # TODO: It would be nice if we could remove it.
        # self.assertNotIn("portal-column-one", browser.contents)
        self.assertNotIn("portletSearch", browser.contents)

    def test_exclude_from_search(self):
        # Exclude our test portlet from searching by Google.
        # This is the default already, but it is only active once we save the form.
        browser = self.get_browser()
        browser.open(self.metadata_url)
        exclude = browser.getControl(label="Exclude from search")
        self.assertTrue(exclude.selected)
        browser.getControl(label="Save").click()

        # There is a hint for Google to exclude this part of the page
        # from search.
        # We expect it in this order:
        off_text = "<!-- googleoff: all -->"
        portlet_text = "portletSearch"
        on_text = "<!-- googleon: all -->"
        browser.open(f"{self.portal_url}/folder")
        self.assertIn("portal-column-one", browser.contents)
        self.assertIn(portlet_text, browser.contents)
        self.assertIn(off_text, browser.contents)
        self.assertIn(on_text, browser.contents)
        self.assertTrue(
            browser.contents.index(off_text) < browser.contents.index(portlet_text)
        )
        self.assertTrue(
            browser.contents.index(portlet_text) < browser.contents.index(on_text)
        )

        # Switch it off.
        browser.open(self.metadata_url)
        exclude = browser.getControl(label="Exclude from search")
        exclude.selected = False
        browser.getControl(label="Save").click()

        # The hint is gone.
        browser.open(f"{self.portal_url}/folder")
        self.assertIn("portletSearch", browser.contents)
        self.assertNotIn("googleoff", browser.contents)
