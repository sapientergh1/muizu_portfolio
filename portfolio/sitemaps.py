from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Education, Experience, Skill, Profile

# Static views sitemap
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['portfolio:home', 'portfolio:about', 'portfolio:contact']

    def location(self, item):
        return reverse(item)

# Project model sitemap
class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('portfolio:project_detail', kwargs={'pk': obj.pk})  # or slug, adjust accordingly


class ExperienceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Experience.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('portfolio:about')

