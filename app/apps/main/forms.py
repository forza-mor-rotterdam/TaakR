from django import forms


class RadioSelect(forms.RadioSelect):
    option_template_name = "widgets/radio_option.html"


class RadioSelectSimple(forms.RadioSelect):
    option_template_name = "widgets/radio_option_simple.html"
