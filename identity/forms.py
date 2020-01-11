# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from django.forms.fields import ChoiceField

from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group


BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))


class UserForm(forms.Form):

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    name = forms.CharField(
        label=_('User Name'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
        label=_('Email'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password_confirm = forms.CharField(
        label=_('Confirm Password'),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    project = ChoiceField(
        label=_('Primary Project'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))

    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'},
                            choices=BOOLEAN_CHOICES), initial=True)

    def clean_password(self):
        if 'password' in self.data:
            if self.data['password'] != self.data.get('password_confirm'):
                raise forms.ValidationError(_('Passwords did not match'))

            return self.data['password']


class CreateUserForm(UserForm):

    role = ChoiceField(label=u'Role', required=True,
                       widget=forms.Select(attrs={'class': 'form-control'}))


class UpdateUserForm(UserForm):

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        for field in ('password', 'password_confirm', 'project'):
            self.fields[field].required = False

        self.fields['project'].widget.attrs['disabled'] = 'True'


class ProjectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        user = kwargs.get('initial').get('user')

        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['group'].required = True

        action = kwargs.get('initial').get('action')

        if action == 'update':
            self.fields['name'].widget.attrs['readonly'] = 'True'

    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    action = forms.CharField(widget=forms.HiddenInput(), required=False)

    name = forms.CharField(
        label=_('Project Name'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                '^[a-zA-Z0-9_-]*$',
                message=_('Project Name must be an alphanumeric.')
            )
        ]
    )

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'},
            choices=BOOLEAN_CHOICES), initial=True)

    group = forms.ModelChoiceField(
        label=_('Group'),
        required=True,
        queryset=Group.objects.all())

    def clean_description(self):
        if 'description' in self.data:
            description = self.data['description']
            if len(description.strip()) == 0:
                raise forms.ValidationError(
                    _('Project description cannot be empty.'))

            return self.data['description']


class DeleteProjectConfirm(forms.Form):

    user = forms.CharField(
        label=_('User'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm project user'),
            }
        )
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm password')
            }
        )
    )
