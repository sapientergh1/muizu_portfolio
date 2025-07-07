from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Education, Experience, Skill, Profile

# Example: Static views sitemap
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # Add your static view names here
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)

#Project model sitemap
class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class EducationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Education.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class ExperienceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Experience.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class SkillSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.4

    def items(self):
        return Skill.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class ProfileSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Profile.objects.all()

    def lastmod(self, obj):
        return obj.updated_at