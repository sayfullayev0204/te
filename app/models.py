from django.db import models
from django.contrib.auth.models import User

# Fan
class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    total_hours = models.IntegerField(default=0)
    lecture_hours = models.IntegerField(default=0)
    practical_hours = models.IntegerField(default=0)
    lab_hours = models.IntegerField(default=0)
    independent_hours = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

# Meyoriy hujjatlar
class RegulatoryDocument(models.Model):
    DOCUMENT_TYPES = [
        ('course_program', 'Fan dasturi'),
        ('work_program', 'Ishchi dastur'),
        ('calendar_plan', 'Kalendar reja'),
        ('literature', 'Adabiyotlar'),
        ('glossary', 'Glossariyalar'),
    ]
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    pdf_file = models.FileField(upload_to='regulatory_documents/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Meyoriy hujjat"
        verbose_name_plural = "Meyoriy hujjatlar"
        ordering = ['document_type', 'title']
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.title}"

# Fan ma'lumotlari
class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('lecture', 'Ma\'ruza'),
        ('practical', 'Amaliy mashg\'ulot'),
        ('laboratory', 'Laboratoriya ishi'),
        ('independent', 'Mustaqil ish'),
        ('video', 'Video darslar'),
    ]
    
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='course_materials/pdfs/', blank=True, null=True)
    video_file = models.FileField(upload_to='course_materials/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube yoki boshqa video URL")
    duration_minutes = models.IntegerField(default=0, help_text="Dars davomiyligi (daqiqa)")
    credits = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Fan ma'lumoti"
        verbose_name_plural = "Fan ma'lumotlari"
        ordering = ['material_type', 'order', 'title']
    
    def __str__(self):
        return f"{self.get_material_type_display()} - {self.title}"
    
    def get_file_url(self):
        if self.material_type == 'video':
            return self.video_file.url if self.video_file else self.video_url
        return self.pdf_file.url if self.pdf_file else None
class ControlTest(models.Model):
    CONTROL_TYPES = [
        ('midterm', 'Oraliq nazorat'),
        ('final', 'Yakuniy nazorat'),
    ]
    
    title = models.CharField(max_length=200)
    control_type = models.CharField(max_length=20, choices=CONTROL_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    time_limit_minutes = models.IntegerField(default=90)
    total_questions = models.IntegerField(default=20, help_text="Test uchun mavjud savollar havzasining umumiy soni")
    num_questions_to_display = models.IntegerField(default=20, help_text="Foydalanuvchiga ko'rsatiladigan savollar soni")
    passing_score = models.IntegerField(default=60, help_text="O'tish bali (%)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_control_type_display()} - {self.title} ({self.num_questions_to_display}/{self.total_questions})"

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Test savol'),
        ('written', 'Yozma savol'),
    ]
    
    control_test = models.ForeignKey(ControlTest, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.TextField()
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Savol {self.order}: {self.question_text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.answer_text[:30]}"

# Natijalar (Results)
class StudentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    control_test = models.ForeignKey(ControlTest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'control_test']
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.control_test.title} - {self.percentage}%"

class StudentAnswer(models.Model):
    student_result = models.ForeignKey(StudentResult, on_delete=models.CASCADE, related_name='student_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    written_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.student_result.user.username} - {self.question.question_text[:30]}..."

# Baholash mezonlari
class AssessmentCriteria(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='assessment_criteria/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Baholash mezoni"
        verbose_name_plural = "Baholash mezonlari"
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"

# Foydalanuvchi jarayoni
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress_percentage = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Foydalanuvchi jarayoni"
        verbose_name_plural = "Foydalanuvchi jarayonlari"
        unique_together = ['user', 'course_material']
    
    def __str__(self):
        return f"{self.user.username} - {self.course_material.title} - {self.progress_percentage}%"