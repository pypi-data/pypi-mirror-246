from django import forms

from django_powcaptcha.client import validate_captcha, PowCaptchaValidationException
from django_powcaptcha.fields import PowCaptchaChallengeField


class PowCaptchaForm(forms.Form):
    powcaptcha_challenge = PowCaptchaChallengeField()
    powcaptcha_nonce = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()

        challenge = cleaned_data.get('powcaptcha_challenge', '')
        nonce = cleaned_data.get('powcaptcha_nonce', '')

        try:
            validate_captcha(challenge, nonce)
        except PowCaptchaValidationException:
            raise forms.ValidationError('Failed to validate captcha')

        return cleaned_data
