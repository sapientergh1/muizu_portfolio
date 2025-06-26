from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.timezone import now, timedelta
from .models import Profile, Experience, Project, Skill, Education, ContactMessage


class CustomAdminSite(AdminSite):
    """
    Custom Admin Site with enhanced dashboard functionality
    """
    site_header = "Muizu Iddrisu Portfolio Admin"
    site_title = "Portfolio Admin"
    index_title = "Portfolio Dashboard"
    
    def index(self, request, extra_context=None):
        """
        Custom admin index view with dashboard widgets
        """
        extra_context = extra_context or {}
        
        # Get statistics for dashboard
        stats = {
            'total_projects': Project.objects.count(),
            'total_experiences': Experience.objects.count(),
            'total_skills': Skill.objects.count(),
            'total_contacts': ContactMessage.objects.count(),
            'recent_contacts': ContactMessage.objects.filter(
                created_at__gte=now() - timedelta(days=7)
            ).count(),
            'featured_projects': Project.objects.filter(featured=True).count(),
        }
        
        # Get recent activity
        recent_projects = Project.objects.order_by('-created_at')[:5]
        recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
        recent_experiences = Experience.objects.order_by('-start_date')[:3]
        
        # Project statistics by type
        project_types = Project.objects.values('type').annotate(
            count=Count('type')
        ).order_by('-count')
        
        # Skill usage statistics
        skill_usage = Skill.objects.annotate(
            project_count=Count('project')
        ).order_by('-project_count')[:10]
        
        extra_context.update({
            'stats': stats,
            'recent_projects': recent_projects,
            'recent_contacts': recent_contacts,
            'recent_experiences': recent_experiences,
            'project_types': project_types,
            'skill_usage': skill_usage,
        })
        
        return super().index(request, extra_context)
    
    def get_urls(self):
        """
        Add custom URLs to the admin site
        """
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_view(self.analytics_view), name='analytics'),
            path('reports/', self.admin_view(self.reports_view), name='reports'),
        ]
        return custom_urls + urls
    
    def analytics_view(self, request):
        """
        Custom analytics view
        """
        # Monthly project creation statistics
        monthly_projects = []
        for i in range(12):
            month_start = now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = Project.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            monthly_projects.append({
                'month': month_start.strftime('%B %Y'),
                'count': count
            })
        
        # Contact form submissions over time
        monthly_contacts = []
        for i in range(12):
            month_start = now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = ContactMessage.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            monthly_contacts.append({
                'month': month_start.strftime('%B %Y'),
                'count': count
            })
        
        context = {
            'title': 'Analytics Dashboard',
            'monthly_projects': monthly_projects,
            'monthly_contacts': monthly_contacts,
            'opts': self.model._meta if hasattr(self, 'model') else None,
        }
        
        return TemplateResponse(request, 'admin/analytics.html', context)
    
    def reports_view(self, request):
        """
        Custom reports view
        """
        # Generate various reports
        reports_data = {
            'project_summary': {
                'total': Project.objects.count(),
                'featured': Project.objects.filter(featured=True).count(),
                'by_type': Project.objects.values('type').annotate(
                    count=Count('type')
                ),
            },
            'experience_summary': {
                'total': Experience.objects.count(),
                'current': Experience.objects.filter(end_date__isnull=True).count(),
                'by_type': Experience.objects.values('type').annotate(
                    count=Count('type')
                ),
            },
            'skill_summary': {
                'total': Skill.objects.count(),
                'most_used': Skill.objects.annotate(
                    usage_count=Count('project')
                ).order_by('-usage_count')[:10],
            },
            'contact_summary': {
                'total': ContactMessage.objects.count(),
                'this_month': ContactMessage.objects.filter(
                    created_at__gte=now().replace(day=1)
                ).count(),
                'by_subject': ContactMessage.objects.values('subject').annotate(
                    count=Count('subject')
                ),
            }
        }
        
        context = {
            'title': 'Reports Dashboard',
            'reports_data': reports_data,
            'opts': self.model._meta if hasattr(self, 'model') else None,
        }
        
        return TemplateResponse(request, 'admin/reports.html', context)


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')


# Enhanced ModelAdmin classes with better customization
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'phone', 'location']
    search_fields = ['name', 'title', 'email']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'email', 'phone', 'location')
        }),
        ('Professional Details', {
            'fields': ('bio', 'profile_image')
        }),
    )


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'type', 'start_date', 'end_date', 'is_current']
    list_filter = ['type', 'start_date', 'end_date', 'is_current']
    search_fields = ['title', 'organization', 'description']
    date_hierarchy = 'start_date'
    filter_horizontal = ['technologies']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'featured', 'created_at', 'get_technologies']
    list_filter = ['type', 'featured', 'created_at', 'technologies']
    search_fields = ['title', 'description']
    filter_horizontal = ['technologies']
    date_hierarchy = 'created_at'
    
    def get_technologies(self, obj):
        return ", ".join([tech.name for tech in obj.technologies.all()[:3]])
    get_technologies.short_description = 'Technologies'


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'get_project_count']
    list_filter = ['category', 'proficiency']
    search_fields = ['name', 'description']
    
    def get_project_count(self, obj):
        return obj.project_set.count()
    get_project_count.short_description = 'Projects Using This Skill'


class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['start_date', 'end_date', 'is_current']
    search_fields = ['degree', 'institution', 'field_of_study']
    date_hierarchy = 'start_date'


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['subject', 'created_at', 'is_read']
    search_fields = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected contacts as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected contacts as unread"


# Register models with custom admin site
custom_admin_site.register(Profile, ProfileAdmin)
custom_admin_site.register(Experience, ExperienceAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(Skill, SkillAdmin)
custom_admin_site.register(Education, EducationAdmin)
custom_admin_site.register(ContactMessage, ContactMessageAdmin)

