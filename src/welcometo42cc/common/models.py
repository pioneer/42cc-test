from django.db import models
from django.contrib.auth.models import User

# Monkey-patching User model
User.add_to_class('biography', models.TextField(max_length=400, blank=True))
User.add_to_class('birthdate', models.DateField(null=True, blank=True))
User.add_to_class('contacts', models.TextField(max_length=400, blank=True))
