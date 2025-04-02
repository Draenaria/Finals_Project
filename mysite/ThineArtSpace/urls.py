"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import (index,
                    profile,
                    register,
                    char_search,
                    group_search,
                    setting_search,
                    species_search,
                    UserCharacterListView,
                    CharacterDetailView,
                    UserGroupListView,
                    GroupDetailView,
                    UserSettingListView,
                    SettingDetailView,
                    UserSpeciesListView,
                    SpeciesDetailView,
                    CharacterCreateView,
                    CharacterUpdateView,
                    CharacterDeleteView,
                    SpeciesCreateView,
                    SpeciesUpdateView,
                    SpeciesDeleteView,
                    GroupCreateView,
                    GroupUpdateView,
                    GroupDeleteView,
                    SettingCreateView,
                    SettingDeleteView,
                    SettingUpdateView)


urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('characters/', UserCharacterListView.as_view(), name='characters'),
    path('characters/<int:pk>', CharacterDetailView.as_view(), name='character'),
    path("characters/new", CharacterCreateView.as_view(), name="character_new"),
    path("characters/<int:pk>/update", CharacterUpdateView.as_view(), name="character_update"),
    path("characters/<int:pk>/delete", CharacterDeleteView.as_view(), name="character_delete"),
    path('settings/', UserSettingListView.as_view(), name='settings'),
    path('settings/<int:pk>', SettingDetailView.as_view(), name='setting'),
    path("settings/new", SettingCreateView.as_view(), name="setting_new"),
    path("settings/<int:pk>/update", SettingUpdateView.as_view(), name="setting_update"),
    path("settings/<int:pk>/delete", SettingDeleteView.as_view(), name="setting_delete"),
    path('groups/', UserGroupListView.as_view(), name='groups'),
    path('groups/<int:pk>', GroupDetailView.as_view(), name='group'),
    path("groups/new", GroupCreateView.as_view(), name="group_new"),
    path("groups/<int:pk>/update", GroupUpdateView.as_view(), name="group_update"),
    path("groups/<int:pk>/delete", GroupDeleteView.as_view(), name="group_delete"),
    path('species/', UserSpeciesListView.as_view(), name='species'),
    path('species/<int:pk>', SpeciesDetailView.as_view(), name='species'),
    path("species/new", SpeciesCreateView.as_view(), name="species_new"),
    path("species/<int:pk>/update", SpeciesUpdateView.as_view(), name="species_update"),
    path("species/<int:pk>/delete", SpeciesDeleteView.as_view(), name="species_delete"),
    path('char_search/', char_search, name='char_search'),
    path('group_search/', group_search, name='group_search'),
    path('sett_search/', setting_search, name='sett_search'),
    path('spec_search/', species_search, name='spec_search'),

]