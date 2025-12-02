from django.contrib import admin
from . import models

# Automatically register all models in master module
for model in models.__all__:
    admin.site.register(getattr(models, model))
