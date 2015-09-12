from django.contrib import admin

# Register your models here.
from .models import Attendee, Event

#class AttendeeAdmin(admin.ModelAdmin):
#    fields = ['checked_in', 'attendee_name', 'attendee_email', 'attendee_id', 'event']

class AttendeeInline(admin.TabularInline):
    model = Attendee

class EventAdmin(admin.ModelAdmin):
    fields = ['event_date', 'event_name', 'event_id']
    list_display = ('event_date', 'event_name')
    list_filter = ['event_date']
    inlines = [AttendeeInline]

admin.site.register(Event, EventAdmin)
#admin.site.register(Attendee)
