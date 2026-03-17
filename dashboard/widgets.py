from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class TinyMCEWidget(forms.Textarea):
    """
    TinyMCE widget for Django forms.
    Loads TinyMCE from local static files.
    """

    class Media:
        js = (
            'tinymce/tinymce.min.js',
            'js/tinymce-init.js',
        )

    def __init__(self, attrs=None):
        default_attrs = {'cols': 80, 'rows': 30}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        return mark_safe(f'''
            <div class="tinymce-wrapper">
                {rendered}
            </div>
        ''')
