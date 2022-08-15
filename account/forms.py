from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'input'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'input'}
        )