import subprocess
import os
import polib
import copy
import codecs


def prereleaser_middle(data):
    """
    1. Run the unit tests one last time before we make a release.
    2. Update the CONTRIBUTORS.txt file.

    Note: Install polib (https://pypi.python.org/pypi/polib).

    """
    print('Running unit tests.')
    subprocess.check_output(["python", "example_project/manage.py", "test", "photologue"])

    print('Running PEP8 check.')
    # See setup.cfg for configuration options.
    subprocess.check_output(["pep8"])

    print('Updating CONTRIBUTORS.txt')

    # This command will get the author of every commit.
    output = subprocess.check_output(["git", "log", "--format='%aN'"])

    # Convert to a list.
    contributors_list = [unicode(contributor.strip("'"), 'utf-8')
                         for contributor in output.split("\n")]

    # Now add info from the translator files. This is incomplete, we can only list
    # the 'last contributor' to each translation.
    for language in os.listdir('photologue/locale/'):
        filename = 'photologue/locale/{0}/LC_MESSAGES/django.po'.format(language)
        po = polib.pofile(filename)
        last_translator = po.metadata['Last-Translator']
        contributors_list.append(last_translator[:last_translator.find('<') - 1])

    # Now we want to only show each contributor once, and to list them by how many
    # contributions they have made - a rough guide to the effort they have put in.
    contributors_dict = {}

    for author in contributors_list:
        author_copy = copy.copy(author)

        if author_copy in ('', '(no author)', 'FULL NAME'):
            # Skip bad data.
            continue

        # The creator of this project should always appear first in the list - so
        # don't add him to this list, but hard-code his name.
        if author_copy in ('Justin Driscoll', 'justin.driscoll'):
            continue

        # Handle contributors who appear under multiple names.
        if author_copy == 'richardbarran':
            author_copy = 'Richard Barran'

        if author_copy in contributors_dict:
            contributors_dict[author_copy] += 1
        else:
            contributors_dict[author_copy] = 1

    with codecs.open('CONTRIBUTORS.txt', 'w', encoding='utf8') as f:
        f.write('Photologue is made possible by all the people who have contributed'
                ' to it. A non-exhaustive list follows:\n\n')
        f.write('Justin Driscoll\n')
        for i in sorted(contributors_dict, key=contributors_dict.get, reverse=True):
            f.write(i + '\n')
