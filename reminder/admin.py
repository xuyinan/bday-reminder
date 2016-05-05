from django.contrib import admin

# Register your models here.
from reminder.models import DoctorProfile, PatientProfile, LogHistory


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_doctor', 'num_of_patients')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'date_of_birth', 'email', 'cell_phone')

class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'doctor', 'patients', 'birthday_message', 'subject', 'message_path')


admin.site.register(DoctorProfile, DoctorAdmin)
admin.site.register(PatientProfile, PatientAdmin)
admin.site.register(LogHistory, LogAdmin)
