from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.File)
admin.site.register(models.Comment)
admin.site.register(models.Team)
admin.site.register(models.TeamMember)
admin.site.register(models.UserBrowseFile)
admin.site.register(models.UserKeptFile)
admin.site.register(models.Modify)
admin.site.register(models.Mod)

