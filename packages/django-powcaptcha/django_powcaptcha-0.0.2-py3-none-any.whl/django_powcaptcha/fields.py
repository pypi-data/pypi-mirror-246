from django import forms

from django_powcaptcha.widgets import PowCaptchaChallengeWidget


class PowCaptchaChallengeField(forms.CharField):
    required = True
    widget = PowCaptchaChallengeWidget
