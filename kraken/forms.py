from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

class DirectoryForm(forms.Form):
    directory = forms.CharField(widget=forms.Textarea, label="Enter directory path(s)", max_length=99999)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = "post"