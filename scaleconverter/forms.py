from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

SCALES = (
	('', 'Choose...'),
	(5, '1:5'),
	(10, '1:10'),
	(20, '1:20'),
	(50, '1:50'),
	(100, '1:100'),
	(200, '1:200'),
	(500, '1:500'),
	(1000, '1:1000')
)

PAPERSIZES = (
	('', 'Choose...'),
	('A5', 'A5'),
	('A4', 'A4'),
	('A3', 'A3'),
	('A2', 'A2'),
	('A1', 'A1'),
	('A0', 'A0'),
)

class ScaleConverterForm(forms.Form):
    view_scale = forms.ChoiceField(choices=SCALES)
    original_drawing_size = forms.ChoiceField(choices=PAPERSIZES)
    printed_drawing_size = forms.ChoiceField(choices=PAPERSIZES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.helper = FormHelper
        # self.helper.form_method = "POST"