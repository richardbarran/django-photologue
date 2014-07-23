########################################
Customisation: third-party contributions
########################################

Photologue has a 'contrib' folder that includes some
useful tweaks to the base project. At the moment, we have just one contribution:

Old-style templates
-------------------
Replaces the normal templates with the templates that used to come with
Photologue 2.X. Use these if you have an existing project that extends these 
'old-style' templates.

To use these, edit your ``TEMPLATE_DIRS`` setting:

.. code-block:: python

    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_TEMPLATE_DIR, 'contrib/old_style_templates'),
        ... other folders containing Photologue templates should come after...
    )

