from django.contrib import admin
from . import models

class IrisImagesTabularInline(admin.TabularInline):
    model = models.IrisImages
    extra = 1

class UserBiometryAdmin(admin.ModelAdmin):
    class Meta:
        model = models.UserBiometry
    inlines = (IrisImagesTabularInline,)

admin.site.register(models.UserBiometry,UserBiometryAdmin)
