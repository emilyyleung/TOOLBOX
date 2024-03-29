from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

class ListCheckerForm(forms.Form):
    # listA = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':100}), label="Enter list A", max_length=99999) # If you want to control rows and columns
    # listB = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':100}), label="Enter list B", max_length=99999)

    listA = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlTextarea3'}), label="List A", max_length=99999)
    listB = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlTextarea3'}	), label="List B", max_length=99999)

    listA_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'List A Title'}))
    listB_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'List B Title'}))


    def __init__(self, *args, **kwargs):
        ''' remove any labels here if desired
        '''
        super(ListCheckerForm, self).__init__(*args, **kwargs)

        self.fields['listA_title'].label = ''
        self.fields['listB_title'].label = ''
	# def __init__(self, *args, **kwargs):
	# 	super(ListCheckerForm,self).__init__(*args, **kwargs)

 #        # self.helper = FormHelper
 #        # self.helper.form_method = "POST"

 #        self.fields['listA_title'].label = ''