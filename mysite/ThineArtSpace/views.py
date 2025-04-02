from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import User
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import CharacterCreateUpdateForm, SpeciesCreateUpdateForm, SettingCreateUpdateForm, \
    GroupCreateUpdateForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import (Character,
                     Setting,
                     Group,
                     Species)

# Create your views here.
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f"Email can't be empty!")
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'User with email {new_email} is already registered!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profile updated")
            return redirect('profile')


    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)



def index(request):
    num_characters=Character.objects.all().count()
    num_settings=Setting.objects.all().count()
    num_groups=Group.objects.all().count()
    num_users=User.objects.all().count()
    num_species=Species.objects.all().count()
    context={
        'num_characters': num_characters,
        'num_settings': num_settings,
        'num_groups': num_groups,
        'num_users': num_users,
        'num_species': num_species,
    }
    return render(request, template_name="index.html", context=context)

@csrf_protect
def register(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is taken!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Username with the email {email} is already registered!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Username {username} is already registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('register')
    return render(request, 'register.html')

class UserCharacterListView(LoginRequiredMixin ,generic.ListView):
    model = Character
    template_name = "my_characters.html"
    context_object_name = "characters"
    paginate_by = 10

    def get_queryset(self):
        return Character.objects.filter(created_by=self.request.user)

class CharacterDetailView(generic.DetailView):
    model = Character
    template_name = "character.html"
    context_object_name = "character"

class UserSettingListView(LoginRequiredMixin, generic.ListView):
    model = Setting
    template_name = "my_settings.html"
    context_object_name = "settings"
    paginate_by = 10

    def get_queryset(self):
        return Setting.objects.filter(created_by=self.request.user)

class SettingDetailView(generic.DetailView):
    model = Setting
    template_name = "setting.html"
    context_object_name = "setting"

class UserGroupListView(LoginRequiredMixin ,generic.ListView):
    model = Group
    template_name = "my_groups.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        return Group.objects.filter(created_by=self.request.user)

class GroupDetailView(generic.DetailView):
    model = Group
    template_name = "group.html"
    context_object_name = "group"

class UserSpeciesListView(LoginRequiredMixin ,generic.ListView):
    model = Species
    template_name = "my_species.html"
    context_object_name = "species"
    paginate_by = 10

    def get_queryset(self):
        return Species.objects.filter(created_by=self.request.user)

class SpeciesDetailView(generic.DetailView):
    model = Species
    template_name = "species.html"
    context_object_name = "species"

def char_search(request):
    query=request.GET.get('query')
    if query:
        char_search_results = Character.objects.filter(Q(name__icontains=query) | Q(age__icontains=query) | Q(backstory__icontains=query) | Q(hobbies__icontains=query) | Q(appearance__icontains=query) | Q(birthday__icontains=query) | Q(occupation__icontains=query) | Q(char_credit__icontains=query) | Q(group_role__icontains=query) | Q(gender__icontains=query)  | Q(setting__name__icontains=query) | Q(groups__name__icontains=query) | Q(species__name__icontains=query))
    else:
        char_search_results = Character.objects.all()
    context = {
        "query": query,
        "chars": char_search_results,
    }
    return render(request, template_name="char_search.html", context=context)

def group_search(request):
    query=request.GET.get('query')
    if query:
        group_search_results = Group.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(group_credit__icontains=query) | Q(setting__name__icontains=query))
    else:
        group_search_results = Group.objects.all()
    context = {
        "query": query,
        "groups": group_search_results,
    }
    return render(request, template_name="group_search.html", context=context)

def species_search(request):
    query=request.GET.get('query')
    if query:
        spec_search_results = Species.objects.filter(Q(name__icontains=query) | Q(appearance__icontains=query) | Q(description__icontains=query) |  Q(spec_credit__icontains=query) |  Q(setting__name__icontains=query))
    else:
        spec_search_results = Species.objects.all()
    context = {
        "query": query,
        "specs": spec_search_results,
    }
    return render(request, template_name="spec_search.html", context=context)

def setting_search(request):
    query=request.GET.get('query')
    if query:
        sett_search_results = Setting.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(sett_credit__icontains=query))
    else:
        sett_search_results = Setting.objects.all()
    context = {
        "query": query,
        "setts": sett_search_results,
    }
    return render(request, template_name="sett_search.html", context=context)

class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
    model = Character
    fields = ['image','name','gender','setting','species','age', 'birthday','appearance','backstory',  'hobbies',    'occupation',
            'groups', 'group_role', 'variant_of_character', 'char_credit']
    template_name = 'character_form.html'
    success_url = "/ThineArtSpace/characters/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CharacterUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Character
    template_name = 'character_form.html'
    success_url = "/ThineArtSpace/characters/"
    form_class = CharacterCreateUpdateForm

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CharacterDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Character
    template_name = 'character_delete.html'
    success_url = "/ThineArtSpace/characters/"
    context_object_name = "character"

    def test_func(self):
        return self.get_object().created_by == self.request.user

class SpeciesCreateView(LoginRequiredMixin, generic.CreateView):
    model = Species
    fields = ['image','name', 'setting','appearance', 'description','parent_species', 'variant_of_species','spec_credit', ]
    template_name = 'species_form.html'
    success_url = "/ThineArtSpace/species/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SpeciesUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Species
    template_name = 'species_form.html'
    success_url = "/ThineArtSpace/species/"
    form_class = SpeciesCreateUpdateForm

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SpeciesDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Species
    template_name = 'species_delete.html'
    success_url = "/ThineArtSpace/species/"
    context_object_name = "species"

    def test_func(self):
        return self.get_object().created_by == self.request.user

class SettingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Setting
    fields = ['name', 'description', 'parent_setting', 'variant_of_setting', 'sett_credit']
    template_name = 'setting_form.html'
    success_url = "/ThineArtSpace/settings/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SettingUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Setting
    template_name = 'setting_form.html'
    success_url = "/ThineArtSpace/settings/"
    form_class = SettingCreateUpdateForm

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SettingDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Setting
    template_name = 'setting_delete.html'
    success_url = "/ThineArtSpace/settings/"
    context_object_name = "setting"

    def test_func(self):
        return self.get_object().created_by == self.request.user

class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ['image','name', 'setting', 'description', 'parent_group', 'variant_of_group', 'setting_relation_tag','group_credit']
    template_name = 'group_form.html'
    success_url = "/ThineArtSpace/groups/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Group
    template_name = 'group_form.html'
    success_url = "/ThineArtSpace/groups/"
    form_class = GroupCreateUpdateForm

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Group
    template_name = 'group_delete.html'
    success_url = "/ThineArtSpace/groups/"
    context_object_name = "groups"

    def test_func(self):
        return self.get_object().created_by == self.request.user

