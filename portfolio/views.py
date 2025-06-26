from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Profile, Skill, Experience, Project, Education, ContactMessage


def home(request):
    """Home page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    featured_projects = Project.objects.filter(featured=True)[:3]
    recent_experiences = Experience.objects.all()[:3]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'recent_experiences': recent_experiences,
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    """About page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    skills = Skill.objects.all().order_by('category', 'name')
    education = Education.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'education': education,
    }
    return render(request, 'portfolio/about.html', context)


def experience(request):
    """Experience page view"""
    teaching_experiences = Experience.objects.filter(type='teaching')
    software_experiences = Experience.objects.filter(type='software')
    academic_experiences = Experience.objects.filter(type='academic')
    other_experiences = Experience.objects.filter(type='other')
    
    context = {
        'teaching_experiences': teaching_experiences,
        'software_experiences': software_experiences,
        'academic_experiences': academic_experiences,
        'other_experiences': other_experiences,
    }
    return render(request, 'portfolio/experience.html', context)


def projects(request):
    """Projects page view"""
    web_projects = Project.objects.filter(type='web')
    mobile_projects = Project.objects.filter(type='mobile')
    teaching_projects = Project.objects.filter(type='teaching')
    academic_projects = Project.objects.filter(type='academic')
    other_projects = Project.objects.filter(type='other')
    
    context = {
        'web_projects': web_projects,
        'mobile_projects': mobile_projects,
        'teaching_projects': teaching_projects,
        'academic_projects': academic_projects,
        'other_projects': other_projects,
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail(request, project_id):
    """Project detail view"""
    project = get_object_or_404(Project, id=project_id)
    related_projects = Project.objects.filter(type=project.type).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)


def contact(request):
    """Contact page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, 'portfolio/contact.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission"""
    try:
        data = json.loads(request.body)
        
        # Create contact message
        contact_message = ContactMessage.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! I will get back to you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'There was an error sending your message. Please try again.'
        }, status=400)


def skills_api(request):
    """API endpoint for skills data"""
    skills = Skill.objects.all().values('name', 'category', 'proficiency', 'description')
    skills_by_category = {}
    
    for skill in skills:
        category = skill['category']
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    return JsonResponse(skills_by_category)


def projects_api(request):
    """API endpoint for projects data"""
    projects = Project.objects.all().values(
        'id', 'title', 'description', 'type', 'url', 'github_url', 'featured', 'created_at'
    )
    
    projects_list = list(projects)
    for project in projects_list:
        project['created_at'] = project['created_at'].isoformat()
    
    return JsonResponse({'projects': projects_list})

