from django import forms


class DateTimeAwareField(forms.DateTimeField):
    input_formats = ['%Y-%m-%dT%H:%M:%S.%fZ']
