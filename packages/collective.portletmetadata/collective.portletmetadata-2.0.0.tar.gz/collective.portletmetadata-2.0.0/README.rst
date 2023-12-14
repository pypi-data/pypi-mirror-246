collective.portletmetadata
==========================

About
-----

collective.portletmetadata is a collection of patches that makes it possible edit
settings for each portlet assignment. We denote these settings for metadata thereby
the name of the product.

Out of the box the product provides the following features:

* Possibility for creating local portlets, i.e. portlets that will not be inherited
  even though child settings imply so.
* Possibility for adding a CSS class for a portlet assignment. These are defined
  in the controlpanel (stored in registry).
  Since version 1.6 you can add any CSS classes (for example from Bootstrap) in a portlet, without first defining it in the control panel.
  This is restricted by a permission, so if you do not like this, you can take this permission away from some roles.
  The field for choosing a pre-defined class is always available.
* Possibility for excluding a portlet from being indexed by Google.


Plone version compatibility
---------------------------

* Version 2.0: Plone 6 only.
* Version 1.5: Plone 5 and 6
* Version 1.3: Plone 5
* Version 1.2: Plone 4.3


Usage
-----

Whenever the product is installed a "*" will be visible in the ``@@manage-portlets``
view for each assignment. Whenever the user selects this option, he/she can edit
the metadata as described above.

See a short guide `here <http://bo.geekworld.dk/introducing-collective-portletmetadata/>`_.


Related work
------------

Ideally, these features should be built into ``plone.app.portlets``.
See `issue 13 <https://github.com/collective/collective.portletmetadata/issues/13>`_.


Author
------

* Bo Simonsen <bo@headnet.dk>


Maintainer
----------

* Maurits van Rees <m.van.rees@zestsoftware.nl>


