from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone
from .models import (
    Subject, RegulatoryDocument, CourseMaterial, ControlTest, 
    Question, StudentResult, AssessmentCriteria, UserProgress
)
import random

def home(request):
    subject = Subject.objects.first()
    if not subject:
        subject = Subject.objects.create(
            name="DISCRETE STRUCTURES",
            code="DS101",
            total_hours=120,
            lecture_hours=30,
            practical_hours=18,
            lab_hours=24,
            independent_hours=48
        )
    
    # Statistics
    stats = {
        'total_hours': subject.total_hours,
        'lectures': subject.lecture_hours,
        'practicals': subject.practical_hours,
        'labs': subject.lab_hours,
        'independent': subject.independent_hours
    }
    
    # Recent materials
    recent_materials = CourseMaterial.objects.filter(
        subject=subject, 
        is_active=True
    ).order_by('-created_at')[:6]
    
    context = {
        'subject': subject,
        'stats': stats,
        'recent_materials': recent_materials,
    }
    return render(request, 'home.html', context)

def regulatory_documents(request, doc_type_slug=None):
    subject = Subject.objects.first()
    
    if doc_type_slug:
        # Map slug to display name for breadcrumb and title
        document_type_map = dict(RegulatoryDocument.DOCUMENT_TYPES)
        # Find the actual document type value from the slug
        actual_doc_type = next((key for key, value in document_type_map.items() if key == doc_type_slug), None)

        if actual_doc_type:
            documents = RegulatoryDocument.objects.filter(subject=subject, document_type=actual_doc_type)
            doc_type_display = document_type_map.get(actual_doc_type, 'Noma\'lum tur')
            context = {
                'documents': documents,
                'doc_type_display': doc_type_display,
                'subject': subject,
                'is_filtered': True, # Flag to indicate filtered view
            }
            return render(request, 'regulatory_documents.html', context)
        else:
            # If slug is invalid, redirect to all documents or show error
            messages.error(request, "Noto'g'ri hujjat turi tanlandi.")
            return redirect('regulatory_documents')
    else:
        # Original logic for displaying all grouped documents
        documents = RegulatoryDocument.objects.filter(subject=subject)
        
        grouped_docs = {}
        for doc in documents:
            doc_type = doc.get_document_type_display()
            if doc_type not in grouped_docs:
                grouped_docs[doc_type] = []
            grouped_docs[doc_type].append(doc)
        
        context = {
            'grouped_documents': grouped_docs,
            'subject': subject,
            'is_filtered': False, # Flag to indicate all documents view
        }
        return render(request, 'regulatory_documents.html', context)

def course_materials(request, material_type=None):
    subject = Subject.objects.first()
    materials = CourseMaterial.objects.filter(subject=subject, is_active=True)
    
    if material_type:
        materials = materials.filter(material_type=material_type)
    
    # Group by material type if no specific type requested
    if not material_type:
        grouped_materials = {}
        for material in materials:
            mat_type = material.get_material_type_display()
            if mat_type not in grouped_materials:
                grouped_materials[mat_type] = []
            grouped_materials[mat_type].append(material)
        
        context = {
            'grouped_materials': grouped_materials,
            'subject': subject,
        }
        return render(request, 'course_materials_grouped.html', context)
    
    context = {
        'materials': materials,
        'material_type': material_type,
        'material_type_display': dict(CourseMaterial.MATERIAL_TYPES).get(material_type, ''),
        'subject': subject,
    }
    return render(request, 'course_materials.html', context)

def material_detail(request, material_id):
    material = get_object_or_404(CourseMaterial, id=material_id, is_active=True)
    
    # Update user progress if logged in
    if request.user.is_authenticated:
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course_material=material
        )
        progress.last_accessed = timezone.now()
        progress.save()
    
    context = {
        'material': material,
    }
    return render(request, 'material_detail.html', context)

def controls_list(request, control_type_slug=None): # control_type_slug parametri qo'shildi
    subject = Subject.objects.first()
    
    if control_type_slug:
        # Slugni haqiqiy control_type qiymatiga o'tkazish
        control_type_map = dict(ControlTest.CONTROL_TYPES)
        actual_control_type = next((key for key, value in control_type_map.items() if key == control_type_slug), None)

        if actual_control_type:
            controls = ControlTest.objects.filter(subject=subject, is_active=True, control_type=actual_control_type).order_by('title')
            control_type_display = control_type_map.get(actual_control_type, 'Noma\'lum tur')
            
            # Foydalanuvchi natijalarini qo'shish
            if request.user.is_authenticated:
                for control in controls:
                    user_result = StudentResult.objects.filter(
                        user=request.user,
                        control_test=control,
                        completed_at__isnull=False
                    ).first()
                    control.user_result = user_result
            
            context = {
                'controls': controls, # Filtrlangan testlar ro'yxati
                'control_type_display': control_type_display,
                'subject': subject,
                'is_filtered': True, # Filtrlangan ko'rinish ekanligini bildiradi
            }
            return render(request, 'controls.html', context)
        else:
            messages.error(request, "Noto'g'ri nazorat turi tanlandi.")
            return redirect('controls')
    else:
        # Avvalgi mantiq: barcha testlarni guruhlab ko'rsatish
        controls = ControlTest.objects.filter(subject=subject, is_active=True).order_by('control_type', 'title')
        
        grouped_controls = {}
        for control in controls:
            control_type = control.get_control_type_display()
            if control_type not in grouped_controls:
                grouped_controls[control_type] = []
            grouped_controls[control_type].append(control)
        
        # Foydalanuvchi natijalarini qo'shish
        for control_type, control_list in grouped_controls.items():
            for control in control_list:
                if request.user.is_authenticated:
                    user_result = StudentResult.objects.filter(
                        user=request.user,
                        control_test=control,
                        completed_at__isnull=False
                    ).first()
                    control.user_result = user_result
        
        context = {
            'grouped_controls': grouped_controls,
            'subject': subject,
            'is_filtered': False, # Barcha testlar ko'rinishi ekanligini bildiradi
        }
        return render(request, 'controls.html', context)

@login_required
def take_test(request, test_id):
    test = get_object_or_404(ControlTest, id=test_id, is_active=True)
    
    # Check if user already took this test
    existing_result = StudentResult.objects.filter(
        user=request.user, 
        control_test=test,
        completed_at__isnull=False
    ).first()
    
    if existing_result:
        messages.info(request, 'Siz bu testni allaqachon topshirgansiz.')
        return redirect('test_result', result_id=existing_result.id)
    
    # Savollarni tanlash logikasi
    all_questions = list(test.questions.filter(is_active=True).prefetch_related('answers'))
    
    if test.control_type == 'midterm' and len(all_questions) >= test.num_questions_to_display:
        # Oraliq nazorat uchun tasodifiy 20 ta savol tanlash
        questions = random.sample(all_questions, test.num_questions_to_display)
    else:
        # Yakuniy nazorat yoki yetarli savol bo'lmaganda barcha mavjud savollarni ko'rsatish
        questions = all_questions
    
    # Savollarni tartiblash (agar tasodifiy tanlangan bo'lsa ham)
    questions.sort(key=lambda q: q.order)
    
    if request.method == 'POST':
        # Process test submission
        result, created = StudentResult.objects.get_or_create(
            user=request.user,
            control_test=test,
            defaults={'started_at': timezone.now()}
        )
        
        total_points = 0
        earned_points = 0
        
        # Faqat ko'rsatilgan savollar bo'yicha ballarni hisoblash
        for question in questions:
            total_points += question.points
            
            if question.question_type == 'multiple_choice':
                selected_answer_id = request.POST.get(f'question_{question.id}')
                if selected_answer_id:
                    selected_answer = question.answers.filter(id=selected_answer_id).first()
                    if selected_answer:
                        is_correct = selected_answer.is_correct
                        points = question.points if is_correct else 0
                        earned_points += points
                        
                        # Save student answer
                        from .models import StudentAnswer
                        StudentAnswer.objects.create(
                            student_result=result,
                            question=question,
                            selected_answer=selected_answer,
                            is_correct=is_correct,
                            points_earned=points
                        )
            
            elif question.question_type == 'written':
                written_answer = request.POST.get(f'written_{question.id}', '')
                # For written questions, manual grading is needed
                from .models import StudentAnswer
                StudentAnswer.objects.create(
                    student_result=result,
                    question=question,
                    written_answer=written_answer,
                    is_correct=False,  # Will be graded manually
                    points_earned=0
                )
        
        # Calculate final score
        result.score = earned_points
        result.total_points = total_points
        result.percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        result.passed = result.percentage >= test.passing_score
        result.completed_at = timezone.now()
        result.save()
        
        return redirect('test_result', result_id=result.id)
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'take_test.html', context)

@login_required
def test_result(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id, user=request.user)
    
    context = {
        'result': result,
    }
    return render(request, 'test_result.html', context)

@login_required
def results_list(request):
    results = StudentResult.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).order_by('-completed_at')
    
    context = {
        'results': results,
    }
    return render(request, 'results_list.html', context)

def assessment_criteria(request):
    subject = Subject.objects.first()
    criteria = AssessmentCriteria.objects.filter(subject=subject)
    
    context = {
        'criteria': criteria,
        'subject': subject,
    }
    return render(request, 'assessment_criteria.html', context)

@login_required
def update_progress(request, material_id):
    if request.method == 'POST':
        material = get_object_or_404(CourseMaterial, id=material_id)
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course_material=material
        )
        progress.completed = True
        progress.progress_percentage = 100
        progress.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})
