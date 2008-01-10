INSTALLATION

2. Unzip the "photologue" directory into your django project directory.
3. Add 'photologue' your installed_apps setting:

INSTALLED_APPS = (
    # other installed apps
    'photologue',
)

4. Add this to yourproject.urls:

urlpatterns += patterns('',
        (r'^photologue/', include('photologue.urls')),
)

Be sure your MEDIA_URL and MEDIA_ROOT settings are correct!

OPTIONAL STEPS

1. Create a new PhotoSize with the name "thumbnail" to get thumbnail previews in the admin interface (optional).
2. Copy the included example templates into one of your TEMPLATE_DIRS (under a subdirectory named "photologue") and modify as needed.
