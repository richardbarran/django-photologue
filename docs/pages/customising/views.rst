.. _customisation-views-label:

#############################
Customisation: Views and Urls
#############################

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
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),

    ... other code

Now we're ready to make some changes.

Changing pagination from our new urls.py
----------------------------------------

The list pages of Photologue (both Gallery and Photo) display 20 objects per page. Let's change this value.
Edit our new urls.py file, and add:


.. code-block:: python

    from django.conf.urls import *

    from photologue.views import GalleryListView
    
    urlpatterns = patterns('',
                           
                           url(r'^gallerylist/$',
                               GalleryListView.as_view(paginate_by=5), name='photologue_custom-gallery-list'),

                           )


We've copied the urlpattern for
`the gallery list view from Photologue itself <https://github.com/jdriscoll/django-photologue/blob/master/photologue/urls.py>`_,
and changed it slightly by passing in ``paginate_by=5``.

And that's it - now when that page is requested, our customised urls.py will be called first, with pagination
set to 5 items.

Values that can be overridden from urls.py
------------------------------------------

GalleryListView
~~~~~~~~~~~~~~~

* paginate_by: number of items to display per page.

PhotoListView
~~~~~~~~~~~~~

* paginate_by: number of items to display per page.

Changing views.py to create a RESTful api
-----------------------------------------
More substantial customisation can be carried out by writing custom views. For example,
it's easy to change a Photologue view to return JSON objects rather than html webpages. For this 
quick demo, we'll use the 
`django-braces library <http://django-braces.readthedocs.org/en/latest/index.html>`_
to override the view returning a list of all photos.

Add the following code to views.py in ``photologue_custom``:

.. code-block:: python

    from photologue.views import PhotoListView

    from braces.views import JSONResponseMixin


    class PhotoJSONListView(JSONResponseMixin, PhotoListView):

        def render_to_response(self, context, **response_kwargs):
            return self.render_json_object_response(context['object_list'],
                                                    **response_kwargs)

And call this new view from urls.py; here we are replacing the standard Photo list page provided by Photologue:

.. code-block:: python

    from .views import PhotoJSONListView

    urlpatterns = patterns('',

                       # Other urls...

                       url(r'^photolist/$',
                           PhotoJSONListView.as_view(),
                           name='photologue_custom-photo-json-list'),

                       # Other urls as required...
                       )


And that's it! Of course, this is simply a demo and a real RESTful api would be rather more complex.





