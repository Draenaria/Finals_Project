
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile-pics/default.png", upload_to="profile-pics/")

    def __str__(self):
        return f"{self.user}'s profile"

    class Meta:
        verbose_name="Profile"
        verbose_name_plural="Profiles"


class Setting(models.Model):
    name=models.CharField(verbose_name="Name", max_length=200)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name="creator_settings")
    description=models.TextField(verbose_name="Description")
    parent_setting=models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_settings")
    variant_of_setting = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="variants")
    sett_credit = models.TextField(verbose_name="Credit", null=True, blank=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['name'], name='unique_setting_name')
        ]
        verbose_name="Setting"
        verbose_name_plural="Settings"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):

        if self.created_by:
            self.creator_name = self.created_by.username
        super().save(*args, **kwargs)

class Group(models.Model):
    name=models.CharField(verbose_name="Name", max_length=100)
    created_by=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name="creator_groups")
    setting=models.ForeignKey(to=Setting, on_delete=models.SET_NULL, null=True, blank=True, related_name="setting_groups")
    description=models.TextField(verbose_name="Description")
    TAG_CHOICES = [
        ('canon', 'Canon'),
        ('fanon', 'Fanon'),
    ]
    setting_relation_tag=models.CharField(max_length=5, choices=TAG_CHOICES, default='fanon')
    parent_group=models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_groups")
    variant_of_group=models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="variants")
    group_credit = models.TextField(verbose_name="Credit", null=True, blank=True)
    image = models.ImageField(verbose_name="Image", upload_to='groups', null=True, blank=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['name', 'setting'], name='unique_group_name_setting')
        ]
        verbose_name="Group"
        verbose_name_plural="Groups"

    def clean(self):
        existing_group = Group.objects.filter(name=self.name, setting=self.setting).first()

        if existing_group:
            if existing_group.created_by != self.created_by:
                raise ValidationError(f"You cannot create a group with the name '{self.name}'.")

        super().clean()

    def __str__(self):
        if self.setting != 'null' and self.setting != 'None' and self.setting != 'blank':
            return f"{self.name} - ({self.setting.name})"
        else:
            return f'{self.name}'

    def save(self, *args, **kwargs):
        self.clean()

        if self.created_by:
            self.creator_name = self.created_by.username

        super().save(*args, **kwargs)

class Species(models.Model):
    name=models.CharField(verbose_name="Name", max_length=200)
    appearance = models.TextField(verbose_name="Appearance")
    description = models.TextField(verbose_name="Description")
    setting=models.ForeignKey(to=Setting, on_delete=models.SET_NULL, null=True, blank=True, related_name="setting_species")
    TAG_CHOICES = [
        ('canon', 'Canon'),
        ('fanon', 'Fanon'),
    ]
    setting_relation_tag = models.CharField(max_length=5, choices=TAG_CHOICES, default='fanon')
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name="creator_species")
    parent_species = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_species")
    variant_of_species = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="variants")
    image = models.ImageField(verbose_name="Image", upload_to='species', null=True, blank=True)
    spec_credit = models.TextField(verbose_name="Credit", null=True, blank=True)

    def __str__(self):
        if self.setting != 'null' and self.setting!= 'none' and self.setting!='blank':
            return f'{self.name} - {self.setting.name}'
        else:
            return f'{self.name}'

    def save(self, *args, **kwargs):

        if self.created_by:
            self.creator_name = self.created_by.username

        super().save(*args, **kwargs)

    class Meta:
        verbose_name="Species"
        verbose_name_plural = "Species"


class Character(models.Model):
    name=models.CharField(verbose_name="Name", max_length=100)
    age=models.CharField(verbose_name="Age", max_length=100)
    backstory=models.TextField(verbose_name="Backstory")
    TAG_CHOICES = [
        ('canon', 'Canon'),
        ('fanon', 'Fanon'),
    ]
    species_relation_tag = models.CharField(max_length=5, choices=TAG_CHOICES, default='fanon')
    group_relation_tag = models.CharField(max_length=5, choices=TAG_CHOICES, default='fanon')
    setting_relation_tag = models.CharField(max_length=5, choices=TAG_CHOICES, default='fanon')
    species=models.ForeignKey(to="Species", on_delete=models.SET_NULL, null=True, blank=True, related_name="species_characters")
    species_name=models.CharField(max_length=200, null=True, blank=True)
    hobbies=models.TextField(verbose_name="Hobbies", null=True, blank=True)
    appearance=models.TextField(verbose_name="Appearance")
    created_by=models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name="creator_characters")
    setting=models.ForeignKey(to=Setting, on_delete=models.SET_NULL, null=True, blank=True,related_name="setting_characters")
    birthday=models.CharField(verbose_name="Birthday", default="Unknown", max_length=100)
    occupation=models.TextField(verbose_name="Occupation", blank=True, null=True)
    image=models.ImageField(verbose_name="Image", upload_to='characters', null=True, blank=True, default='character_default/default.png')
    char_credit=models.TextField(verbose_name="Credit", null=True, blank=True)
    groups = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="group_characters")
    group_role=models.CharField(verbose_name="Group role", max_length=200, null=True, blank=True, default="Unknown")
    variant_of_character=models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True, related_name="variants")
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('agender', 'Agender'),
        ('trans male', 'Trans male'),
        ('trans female', 'Trans female'),
        ('multigender', 'Multigender'),
        ('nonbinary', 'Nonbinary'),
    ]

    gender=models.CharField(verbose_name="Gender", max_length=100, choices=GENDER_CHOICES, default="agender")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.created_by:
            self.creator_name = self.created_by.username
        super().save(*args, **kwargs)


    class Meta:
        verbose_name="Character"
        verbose_name_plural="Characters"


