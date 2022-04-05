from django.test import TestCase
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file, create_superuser


class ManagementCommandsTests(TestCase):
    def setUp(self):
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

    # TODO: write more management command tests
    def test_delete_thumbnails(self):
        from django.core.management import call_command
        call_command('filer_addons', 'delete_thumbnails', )
        # import django
        # from django.core.management import call_command
        # if django.VERSION[:2] < (2, 1):
        #     call_command('filer_addons', 'delete_thumbnails', )
        # else:
        #     call_command('filer_addons' )
        #     from filer_addons.filer_utils.management.commands import delete_thumbnails  # noqa
        #     call_command(delete_thumbnails.Command(), )
        # check for thumb dir not existing

    def test_unused_files_command(selfs):
        pass

    def test_orphaned_files_command(selfs):
        pass

    def test_import_existing_files_command(selfs):
        pass
