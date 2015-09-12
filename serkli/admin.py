from django.contrib import admin

# Register your models here.
from .models import Member, Circle

#class AttendeeAdmin(admin.ModelAdmin):
#    fields = ['checked_in', 'attendee_name', 'attendee_email', 'attendee_id', 'event']

class MemberInline(admin.TabularInline):
    model = Member

class CircleAdmin(admin.ModelAdmin):
#    fields = ['event_date', 'event_name', 'event_id']
#    list_display = ('event_date', 'event_name')
#    list_filter = ['event_date']
    inlines = [MemberInline]

admin.site.register(Circle, CircleAdmin)
#admin.site.register(Attendee)
