import os
from django.test import TestCase, modify_settings
from filer.models import File, Folder

from filer_addons.filer_signals import conf as signals_conf
from filer_addons.tests.utils import create_django_file, create_superuser

try:
    reload
except NameError:
    from importlib import reload


@modify_settings(INSTALLED_APPS={
    'append': 'filer_addons.filer_signals',
})
class ConsistentFilenamesTests(TestCase):

    def setUp(self):
        reload(signals_conf)
        self.superuser = create_superuser()
        self.client.login(username='admin', password='secret')
        self.folder = Folder.objects.create(name='test')
        self.another_folder = Folder.objects.create(name='test')

    def tearDown(self):
        self.delete_files()
        for folder in Folder.objects.all():
            folder.delete()

    def delete_files(self):
        for f in File.objects.all():
            f.delete()

    def create_file(self, **kwargs):
        """
        two files
        kwargs size: tuple, img dimension
        kwargs name: filename
        :param kwargs:
        :return:
        """
        filename = 'file.jpg'
        if kwargs.get('name', None):
            filename = kwargs['name']
        size = (50, 50, )
        if kwargs.get('size', None):
            size = kwargs['size']
        django_file = create_django_file(filename=filename, size=size)
        file_obj = File.objects.create(
            owner=self.superuser,
            original_filename=filename,
            file=django_file,
        )
        file_obj.save()
        return file_obj

    def test_has_correct_filename_simple(self):
        """
        basics. if this breaks, filer has gone nuts completely!
        :return:
        """
        file_obj = self.create_file()
        original_name_only, original_suffix = os.path.splitext(
            file_obj.original_filename
        )
        new_name_only, new_name_suffix = os.path.splitext(
            os.path.basename(file_obj.file.name)
        )
        self.assertTrue(new_name_only.startswith(original_name_only))
        self.assertEquals(new_name_suffix, original_suffix)

    def test_has_correct_name_after_file_update(self):
        """
        change the file, filename should, too
        :return:
        """
        file_obj = self.create_file()
        new_django_file = create_django_file(filename='other.jpg')
        file_obj.file = new_django_file
        file_obj.save()
        original_name_only, original_suffix = os.path.splitext(
            file_obj.original_filename
        )
        new_name_only, new_name_suffix = os.path.splitext(
            os.path.basename(file_obj.file.name)
        )
        self.assertTrue(new_name_only.startswith(original_name_only))
        self.assertEquals(new_name_suffix, original_suffix)

    def test_has_correct_name_after_original_name_update(self):
        """
        change the file, filename should, too
        :return:
        """
        file_obj = self.create_file()
        file_obj.original_filename = 'something_different.jpg'
        file_obj.save()
        original_name_only, original_suffix = os.path.splitext(
            file_obj.original_filename
        )
        new_name_only, new_name_suffix = os.path.splitext(
            os.path.basename(file_obj.file.name)
        )
        self.assertTrue(new_name_only.startswith(original_name_only))
        self.assertEquals(new_name_suffix, original_suffix)
