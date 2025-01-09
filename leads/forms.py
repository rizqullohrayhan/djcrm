from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Lead, Agent, Category


User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'profile_picture',
        ]

    def clean_profile_picture(self):
        image = self.cleaned_data['profile_picture']

        if image:
            # Periksa ukuran file (dalam byte)
            if image.size > 200 * 1024:  # 200 KB
                raise ValidationError("Ukuran gambar tidak boleh lebih dari 200 KB.")
        return image


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )
