from django import forms
from django.contrib.auth.models import User

from .models import Character, Species, Setting, Group, Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class CharacterImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['image']

class CharacterCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = ['image','name','gender','setting','species','age', 'birthday','appearance','backstory',  'hobbies',    'occupation',
            'groups', 'group_role', 'variant_of_character', 'char_credit']

class SpeciesCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Species
        fields = ['image','name', 'setting','appearance', 'description','parent_species', 'variant_of_species','spec_credit', ]



class SettingCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Setting
        fields = ['name', 'description', 'parent_setting', 'variant_of_setting', 'sett_credit']

class GroupCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['image','name', 'setting', 'description', 'parent_group', 'variant_of_group', 'setting_relation_tag','group_credit']

