#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muizu_portfolio.settings')
django.setup()

from portfolio.models import Profile, Skill, Experience, Project, Education

def populate_data():
    # Clear existing data
    Profile.objects.all().delete()
    Skill.objects.all().delete()
    Experience.objects.all().delete()
    Project.objects.all().delete()
    Education.objects.all().delete()
    
    # Create Profile
    profile = Profile.objects.create(
        name="Muizu Iddrisu",
        title="Teacher • Software Engineer • Student",
        bio="Passionate about bridging the gap between education and technology. I create innovative solutions while inspiring the next generation of learners and developers.",
        email="muizu.iddrisu@example.com",
        phone="+233 123 456 789",
        location="Ghana"
    )
    print(f"Created profile: {profile.name}")
    
    # Create Skills
    skills_data = [
        ("Django", "programming", 90, "Advanced web framework for Python"),
        ("JavaScript", "programming", 85, "Frontend and backend development"),
        ("React", "programming", 80, "Modern frontend library"),
        ("Python", "programming", 95, "Primary programming language"),
        ("HTML/CSS", "programming", 90, "Frontend markup and styling"),
        ("Classroom Management", "teaching", 95, "Effective classroom leadership"),
        ("Curriculum Development", "teaching", 85, "Educational content creation"),
        ("Student Assessment", "teaching", 90, "Evaluation and feedback methods"),
        ("Research Methods", "academic", 80, "Academic research techniques"),
        ("Data Analysis", "academic", 75, "Statistical analysis and interpretation"),
        ("Academic Writing", "academic", 85, "Scholarly communication"),
    ]
    
    for name, category, proficiency, description in skills_data:
        skill = Skill.objects.create(
            name=name, 
            category=category, 
            proficiency=proficiency, 
            description=description
        )
        print(f"Created skill: {skill.name}")
    
    # Create Experiences
    experiences_data = [
        ("Senior Software Engineer", "TechCorp Ghana", "software", "2022-01-01", None, "Leading development of web applications using Django and React. Mentoring junior developers and implementing best practices."),
        ("Mathematics Teacher", "Ghana Education Service", "teaching", "2020-09-01", "2023-06-30", "Teaching mathematics to senior high school students. Developed innovative teaching methods using technology."),
        ("Graduate Student", "University of Ghana", "academic", "2021-09-01", None, "Pursuing Master's degree in Computer Science. Research focus on educational technology and machine learning."),
        ("Freelance Web Developer", "Self-Employed", "software", "2019-06-01", "2021-12-31", "Developed custom websites and web applications for small businesses and NGOs."),
        ("Teaching Assistant", "University of Cape Coast", "teaching", "2018-09-01", "2020-06-30", "Assisted professors with undergraduate computer science courses. Conducted lab sessions and graded assignments."),
    ]
    
    for title, organization, exp_type, start_str, end_str, description in experiences_data:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str) if end_str else None
        experience = Experience.objects.create(
            title=title,
            organization=organization,
            type=exp_type,
            start_date=start_date,
            end_date=end_date,
            description=description,
            is_current=(end_date is None)
        )
        print(f"Created experience: {experience.title}")
    
    # Create Projects
    projects_data = [
        ("Portfolio Website", "Personal portfolio website built with Django and React", "web", "https://muizu-portfolio.com", "https://github.com/muizu/portfolio", True),
        ("School Management System", "Complete school management system for tracking students, teachers, and courses", "web", "https://school-mgmt.com", "https://github.com/muizu/school-mgmt", True),
        ("Math Learning App", "Mobile app for interactive mathematics learning", "mobile", "", "https://github.com/muizu/math-app", False),
        ("Educational Research Platform", "Platform for conducting and analyzing educational research", "academic", "https://edu-research.com", "https://github.com/muizu/edu-research", True),
        ("Teaching Resource Hub", "Collection of teaching materials and resources", "teaching", "https://teaching-hub.com", "https://github.com/muizu/teaching-hub", False),
        ("Data Visualization Tool", "Tool for creating interactive data visualizations", "web", "https://dataviz-tool.com", "https://github.com/muizu/dataviz", False),
    ]
    
    for title, description, proj_type, url, github_url, featured in projects_data:
        project = Project.objects.create(
            title=title,
            description=description,
            type=proj_type,
            url=url,
            github_url=github_url,
            featured=featured
        )
        print(f"Created project: {project.title}")
    
    # Create Education
    education_data = [
        ("Master of Science in Computer Science", "University of Ghana", "2021-09-01", None, "Specializing in Educational Technology and Machine Learning"),
        ("Bachelor of Science in Mathematics", "University of Cape Coast", "2016-09-01", "2020-06-30", "First Class Honours. Focus on Applied Mathematics and Statistics"),
        ("Diploma in Education", "University of Education, Winneba", "2020-01-01", "2020-12-31", "Professional teaching qualification"),
    ]
    
    for degree, institution, start_str, end_str, description in education_data:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str) if end_str else None
        education = Education.objects.create(
            degree=degree,
            institution=institution,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        print(f"Created education: {education.degree}")
    
    print("\nData population completed successfully!")

if __name__ == "__main__":
    populate_data()

