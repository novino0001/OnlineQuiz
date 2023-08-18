from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',  views.home , name ='home' ),
    path('accounts/register' , views.register , name = "register"),
    path('all-category/',  views.all_category , name ='all_category' ),
    path('student-info/<int:category_id>',  views.student_info , name ='student_info' ),
    path('category-questions/<int:category_id>/<str:level>',  views.category_questions , name ='category_questions' ),
    path('submit-answer/<int:category_id>/<int:question_id>/<str:level>' , views.submit_answer , name = "submit_answer"),
    path('user-profile/' ,views.user_profile , name ='user_profile' )
    # path('result/', views.submit_answer , name = 'submit_answer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)