from django.contrib import admin

# Register your models here.
from .models import Member, Circle, Reminder

#class AttendeeAdmin(admin.ModelAdmin):
#    fields = ['checked_in', 'attendee_name', 'attendee_email', 'attendee_id', 'event']

class MemberInline(admin.TabularInline):
    model = Member

class CircleAdmin(admin.ModelAdmin):
    inlines = [MemberInline]

admin.site.register(Circle, CircleAdmin)
admin.site.register(Reminder)
