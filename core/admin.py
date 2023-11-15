from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Person  # Import your Person model

class PersonCreationForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ('email',)  # Add 'email' to the fields

class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm
    model = Person
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Register the Person model with the custom admin
admin.site.register(Person, PersonAdmin)