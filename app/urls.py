from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Meyoriy hujjatlar
    path('regulatory-documents/', views.regulatory_documents, name='regulatory_documents'),
    path('regulatory-documents/<str:doc_type_slug>/', views.regulatory_documents, name='regulatory_documents_type'),
    
    # Fan ma'lumotlari
    path('course-materials/', views.course_materials, name='course_materials'),
    path('course-materials/<str:material_type>/', views.course_materials, name='course_materials_type'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
    
    # Nazoratlar
    path('controls/', views.controls_list, name='controls'),
    path('controls/<str:control_type_slug>/', views.controls_list, name='controls_type'), # Yangi URL
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('test-result/<int:result_id>/', views.test_result, name='test_result'),
    
    # Natijalar
    path('results/', views.results_list, name='results'),
    
    # Baholash mezonlari
    path('assessment-criteria/', views.assessment_criteria, name='assessment_criteria'),
    
    # AJAX
    path('update-progress/<int:material_id>/', views.update_progress, name='update_progress'),
]
