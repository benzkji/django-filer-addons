from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.forms import widgets
from django import forms
from filer.models import File
from cms.api import add_plugin


class FilerMultiUploadInlineMixin(object):
    # TODO: add at first or last position?
    # TODO: check file_field correctness!
    # TODO: connect with filer_gui enhanced file field?!!
    """
    adds a dropzone at the beginning of the inline. uploaded files will be
    added to the inline, the new file_id being set on the "file_field".
    """
    file_field = 'file'
    # upload_folder = get_folder_by_path('uploads', True)
    extra = 0
    hide_add_inline = False
    # extra_css_class = 'sortable-inline sortable-tabular-inline'
    extra_css_class = 'sortable-inline sortable-tabular-inline'

    @property
    def media(self):
        original_media = super(FilerMultiUploadInlineMixin, self).media
        js = (
            settings.STATIC_URL + 'filer/js/libs/dropzone.min.js',
            settings.STATIC_URL + 'filer_gui/js/multiupload_inline.js',
        )
        css = {
            'all': (settings.STATIC_URL + 'filer_gui/css/multiupload_base.css',)
        }
        new_media = widgets.Media(js=js, css=css)
        return original_media + new_media

    @property
    def template(self):
        if isinstance(self, admin.StackedInline):
            return 'admin/filer_gui/multiupload_stacked.html'
        if isinstance(self, admin.TabularInline):
            return 'admin/filer_gui/multiupload_tabular.html'
        raise ImproperlyConfigured('Class {0}.{1} must also derive from'
                                   ' admin.TabularInline or'
                                   ' admin.StackedInline'
                                   .format(self.__module__, self.__class__))


"""
we need:
- element in form or on page with a custom classname and data attrs,
  totrigger js
possible solutions:
- 1 hack change form, add stuff there. only one uploader per plugin possible!
- 2 use custom form with custom widget. widget can be positioned in form...
- 3 check def get_fields() (no luck for now)
    https://stackoverflow.com/questions/8007095/dynamic-fields-in-django-admin

implemented:
- mix between 1 and 2 (as a form is definitly needed)
"""


class FilerMultiUploadPluginForm(forms.ModelForm):
    filer_gui_added_files = forms.ModelMultipleChoiceField(
        queryset=File.objects.all(),
        required=False
    )


class FilerMultiUploadPluginMixin(object):
    upload_child_plugin = None
    upload_file_field = 'file'
    form = FilerMultiUploadPluginForm
    # upload_folder = get_folder_by_path('uploads', True)
    change_form_template = 'admin/filer_gui/multiupload_plugin_changeform.html'

    @property
    def media(self):
        original_media = super(FilerMultiUploadPluginMixin, self).media
        js = (
            settings.STATIC_URL + 'filer/js/libs/dropzone.min.js',
            # settings.STATIC_URL + 'filer/js/addons/dropzone.init.js',
            settings.STATIC_URL + 'filer_gui/js/multiupload_plugin.js',
        )
        css = {
            'all': (settings.STATIC_URL + 'filer_gui/css/multiupload_base.css',)  # noqa
        }
        new_media = widgets.Media(js=js, css=css)
        return original_media + new_media

    def save_model(self, request, obj, form, change):
        response = super(FilerMultiUploadPluginMixin, self).save_model(
            request, obj, form, change
        )
        # print "-----"
        # print form.cleaned_data['filer_gui_added_files']
        for file in form.cleaned_data['filer_gui_added_files']:
            placeholder = obj.placeholder
            parent_plugin = obj
            plugin_data = {
                self.upload_file_field: file,
            }
            added_plugin = add_plugin(
                 placeholder,
                 self.upload_child_plugin,
                 'de',
                 'first-child',
                 parent_plugin,
                 **plugin_data
            )
            added_plugin.move(parent_plugin, 'first-child')
        return response