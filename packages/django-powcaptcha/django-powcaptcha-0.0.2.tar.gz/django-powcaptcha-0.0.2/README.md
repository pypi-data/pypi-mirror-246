# Django PowCaptcha

Django PowCaptcha form field/widget integration app.

## Installation

1. Install with `pip install django-powcaptcha`.

2. Add `'django_powcaptcha'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    ...,
    'django_powcaptcha',
    ...
]
```

3. Add settings.

For example:

```python
POWCAPTCHA_API_URL = 'https://captcha.yourdomain.com'
POWCAPTCHA_API_TOKEN = 'MyPOWCAPTCHAPrivateKey456'
```

## Usage

### Form

The quickest way to add PowCaptcha to a form is to use the included
`PowCaptchaForm` class. For example:

```python
from django_powcaptcha.forms import PowCaptchaForm

class FormWithCaptcha(PowCaptchaForm):
    ...
```
