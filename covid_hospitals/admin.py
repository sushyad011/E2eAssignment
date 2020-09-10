from django.contrib import admin
from .models import Bed, Patient


class BedAdmin(admin.ModelAdmin):
    readonly_fields = ['bed_id']

admin.site.register(Bed,BedAdmin)
admin.site.register(Patient)

