Installation

Step 1 - Download Photologue

Photologue can be downloaded below or from the project page. Older versions are also available from the project page and users who like to live on the edge can checkout a copy of the latest trunk revision.

Step 2 - Add Photologue To Your Project

Copy the entire Photologue application folder (the folder named 'photologue' that contains 'models.py') to a location on your Python path such as your project root. Your project root is typically the directory where your 'settings.py' is found.

Step 3 - Configure Your Settings

Add 'photologue' to your INSTALLED_APPS setting:

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
    )

Confirm that your MEDIA_ROOT and MEDIA_URL settings are correct.

If you want to tweak things even more you can also over-ride a few default settings (optional, see documentation for more information on the available settings).

Step 4 - Register Photologue with the Django Admin

Add the following to your projects urls.py file:

    from django.contrib import admin
    
    admin.autodiscover()

Step 4 - Sync Your Database

Run the 'manage.py syndb' command to create the appropriate tables. After the database in initialized, Photologue will walk you through creating some default models.

Additional documentation available here:

http://code.google.com/p/django-photologue/w/list
