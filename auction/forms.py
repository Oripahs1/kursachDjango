from django import forms

class ParserForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')
