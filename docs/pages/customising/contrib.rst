########################################
Customisation: third-party contributions
########################################

Photologue has a 'contrib' folder that includes some
useful tweaks to the base project. At the moment, we have just one contribution:

Bootstrap templates
-------------------
Replaces the normal templates with a new set that work well with `Bootstrap <http://twitter.github.io/bootstrap/index.html>`_.

To use these, edit your ``TEMPLATE_DIRS`` setting:

.. code-block:: python

    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/bootstrap/templates'),
        ... other folders containing Photologue templates should come after...
    )

The templates are incomplete - for example, we are missing templates for date-filtered galleries and photos.
Pull requests are welcome!
