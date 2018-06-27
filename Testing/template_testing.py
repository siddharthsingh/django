from django.conf import settings
from django.template import Template, TemplateSyntaxError
from django.test import TestCase

from future.backports.test.support import import_module


class TemplatesTest(TestCase):

    # part of this function has been copied from https://gist.github.com/magopian/4086398
    #  modified by Siddharth Singh
    def test_templates(self):
        """Templates can compile properly and there's no mismatched tags"""
        # get app template dirs
        template_dirs = []
        apps = [app for app in settings.INSTALLED_APPS]
        for app in apps:
            mod = import_module(app)
            template_dirs.append(path.join(path.dirname(mod.__file__),
                                 'templates'))

        # find all templates (*.html)
        print("this is template dirs",template_dirs)
        templates = []
        for template_dir in template_dirs:
            templates += glob.glob('%s/*.html' % template_dir)
            for root, dirnames, filenames in walk(template_dir):
                for dirname in dirnames:
                    template_folder = path.join(root, dirname)
                    templates += glob.glob('%s/*.html' % template_folder)
        for template in templates:
            # print(template)
            with open(template, 'r') as f:
                source = f.read()
                # template compilation fails on impaired or invalid blocks tags
                try:
                    Template(source)
                except TemplateSyntaxError as e:
                    raise TemplateSyntaxError('%s in %s' % (e, template))
                # check for badly formatted tags or filters
                self.assertEqual(source.count('{%'),
                                 source.count('%}'),
                                 "Found impaired {%% and %%} in %s" % template)
                self.assertEqual(source.count('{{'),
                                 source.count('}}'),
                                 "Found impaired {{ and }} in %s" % template)

                # create an object of BeautifulSoup
                soup = BeautifulSoup(f, 'html.parser')
                # Check if the HTML File has a title tag
                self.assertIsNotNone(soup.title, "Template -> " + str(template)+" Does not have a title Tag\n")
                # check if the title tag is empty
                self.assertIsNotNone(soup.title.string, "Template -> " + str(template) + " Does not have a title\n")
                # check if head tag is defined more than once
                self.assertEquals(len(soup.find_all('head')), 1, "Head Tag defined more than once")
