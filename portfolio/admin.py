from django.contrib import admin
from .models import Profile, Skill, Experience, Project, Education, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'created_at']
    search_fields = ['name', 'title', 'email']
    list_filter = ['created_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'type', 'start_date', 'end_date', 'is_current']
    list_filter = ['type', 'is_current', 'start_date']
    search_fields = ['title', 'organization']
    filter_horizontal = ['technologies']
    date_hierarchy = 'start_date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'featured', 'created_at']
    list_filter = ['type', 'featured', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['technologies']
    date_hierarchy = 'created_at'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['degree', 'institution', 'field_of_study']
    date_hierarchy = 'start_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = [mark_as_read]

