.. _customisation-views-label:

####################
Customisation: Views
####################

The photologue views and urls can be tweaked to better suit your project. The technique described on this page
is not specific to Photologue - it can be applied to any 3rd party library. 

Create a customisation application
----------------------------------
For clarity, it's best to put our customisation code in a new application; let's call it
``photologue_custom``; create the application and add it to your ``INSTALLED_APPS`` setting.

We will also want to customise urls:

1. Create a urls.py that will contain our customised urls:


.. code-block:: python

	from django.conf.urls import *

	urlpatterns = patterns('',
	                       
	                       # Nothing to see here... for now.

	                       )


2. These custom urls will override the main Photologue urls, so place them just before Photologue 
in the project's main urls.py file:

.. code-block:: python

	... other code
	(r'^photologue/', include('photologue_custom.urls')),
	(r'^photologue/', include('photologue.urls')),

	... other code

Now we're ready to make some changes.

Changing pagination
-------------------

The list pages of Photologue (both Gallery and Photo) display 20 objects per page. Let's change this value.
Edit our new urls.py file, and add:


.. code-block:: python

	from django.conf.urls import *

	from photologue.views import GalleryListView
	
	urlpatterns = patterns('',
	                       
	                       url(r'^gallery/page/(?P<page>[0-9]+)/$',
    	                       GalleryListView.as_view(paginate_by=5), name='pl-gallery-list'),

	                       )


We've copied the urlpattern for
`the gallery list view from Photologue itself <https://github.com/jdriscoll/django-photologue/blob/master/photologue/urls.py>`_,
and changed it slightly by passing in ``paginate_by=5``.

And that's it - now when that page is requested, our customised version will be called first, with pagination
set to 5 items.

Values that can be overridden from urls.py
------------------------------------------

GalleryListView
~~~~~~~~~~~~~~~

* paginate_by: number of items to display per page.

PhotoListView
~~~~~~~~~~~~~

* paginate_by: number of items to display per page.
