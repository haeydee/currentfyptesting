from django.contrib import admin
from .models import Milestone, StudentProfile

class MilestoneInLine(admin.TabularInline):
    model = Milestone
    extra = 0

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_pelajar', 'kumpulan', 'program', 'kod_kursus')
    list_filter = ('kumpulan', 'program', 'kod_kursus')
    search_fields = ('nama', 'no_pelajar', 'kumpulan__name')
    inlines = [MilestoneInLine]
