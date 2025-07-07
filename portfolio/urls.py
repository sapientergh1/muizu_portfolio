from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from portfolio.sitemaps import (
    StaticViewSitemap,
    ProjectSitemap,
    EducationSitemap,
    ExperienceSitemap,
    SkillSitemap,
    ProfileSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'education': EducationSitemap,
    'experience': ExperienceSitemap,
    'skills': SkillSitemap,
    'profiles': ProfileSitemap,
}

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('experience/', views.experience, name='experience'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('api/skills/', views.skills_api, name='skills_api'),
    path('api/projects/', views.projects_api, name='projects_api'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

