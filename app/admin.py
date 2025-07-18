from django.contrib import admin
from .models import (
    Subject, RegulatoryDocument, CourseMaterial, ControlTest, 
    Question, Answer, StudentResult, StudentAnswer, AssessmentCriteria, UserProgress
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'total_hours', 'lecture_hours', 'practical_hours', 'lab_hours', 'independent_hours']
    search_fields = ['name', 'code']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'code', 'description')
        }),
        ('Soat taqsimoti', {
            'fields': ('total_hours', 'lecture_hours', 'practical_hours', 'lab_hours', 'independent_hours')
        }),
    )

@admin.register(RegulatoryDocument)
class RegulatoryDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'subject', 'created_at']
    list_filter = ['document_type', 'subject', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['document_type', 'title']

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'subject', 'duration_minutes', 'credits', 'is_active', 'created_at']
    list_filter = ['material_type', 'subject', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['material_type', 'order', 'title']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'material_type', 'subject', 'description', 'order', 'is_active')
        }),
        ('Fayl ma\'lumotlari', {
            'fields': ('pdf_file', 'video_file', 'video_url')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('duration_minutes', 'credits')
        }),
    )

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['answer_text', 'is_correct', 'order']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'question_type', 'control_test', 'points', 'order', 'is_active']
    list_filter = ['question_type', 'control_test', 'is_active']
    search_fields = ['question_text']
    ordering = ['control_test', 'order']
    inlines = [AnswerInline]
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Savol matni'

@admin.register(ControlTest)
class ControlTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'control_type', 'subject', 'num_questions_to_display', 'total_questions', 'time_limit_minutes', 'passing_score', 'is_active']
    list_filter = ['control_type', 'subject', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['control_type', 'title']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'control_type', 'subject', 'description')
        }),
        ('Test sozlamalari', {
            'fields': ('time_limit_minutes', 'total_questions', 'num_questions_to_display', 'passing_score', 'is_active')
        }),
    )

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'control_test', 'score', 'total_points', 'percentage', 'passed', 'completed_at']
    list_filter = ['passed', 'control_test', 'completed_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['percentage', 'passed']
    ordering = ['-completed_at']

@admin.register(AssessmentCriteria)
class AssessmentCriteriaAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['title', 'description']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course_material', 'progress_percentage', 'completed', 'time_spent_minutes', 'last_accessed']
    list_filter = ['completed', 'course_material__material_type', 'course_material__subject']
    search_fields = ['user__username', 'course_material__title']
    ordering = ['-last_accessed']
