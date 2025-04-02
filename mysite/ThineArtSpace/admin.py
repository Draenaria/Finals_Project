from django.contrib import admin
from .models import (Character,
                     Setting,
                     Group,
                     Species,
                     Profile,)

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'created_by']
    list_filter = ['species', 'groups', 'gender', 'created_by', 'setting', 'groups']
    search_fields = ['backstory', 'age', 'name', 'hobbies', 'appearance', 'birthday', 'occupation', 'char_credit', 'group_role', ]

class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']
    list_filter = ['created_by']
    search_fields = ['name', 'created_by', 'description']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'setting','created_by', 'setting_relation_tag']
    list_filter = ['created_by', 'setting', 'setting_relation_tag']
    search_fields = ['name', 'created_by', 'setting', 'description']

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']
    list_filter = ['created_by', 'setting']
    search_fields = ['name', 'created_by', 'description', 'appearance']




admin.site.register(Character, CharacterAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Profile)