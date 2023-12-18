from django.conf import settings
from django.forms import widgets

from django_powcaptcha.client import get_challenge


class PowCaptchaChallengeWidget(widgets.Widget):
    input_type = 'hidden'
    template_name = 'django_powcaptcha/widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update(
            {
                'captcha_url': settings.POWCAPTCHA_API_URL,
                'captcha_challenge': get_challenge(),
                'captcha_callback': 'myCaptchaCallback',
            }
        )
        return context
