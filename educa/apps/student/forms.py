from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')
        labels = {'username': 'E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'name')
        labels = {'username': 'E-mail'}
