# -*- coding: utf-8 -*-
from django.contrib import admin

from information.models import Company, Food, Person, Tag

# Register your models here.
admin.site.register(Company)
admin.site.register(Tag)
admin.site.register(Food)
admin.site.register(Person)
