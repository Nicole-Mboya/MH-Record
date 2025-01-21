from django.contrib import admin
from .models import Appointment, EmotionLog, Journal, ContactInfo

admin.site.register(Appointment)
admin.site.register(EmotionLog)
admin.site.register(Journal)
admin.site.register(ContactInfo)
