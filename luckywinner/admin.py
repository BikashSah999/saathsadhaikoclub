from django.contrib import admin
from .models import Luckydraw, Participants, Winner
# Register your models here.
admin.site.register(Luckydraw)
admin.site.register(Participants)
admin.site.register(Winner)