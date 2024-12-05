from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ClassifyDocumentView, delete_account, extract_text_or_table, user_profile, AboutView, DashboardView,  CustomPasswordChangeDoneView, CustomPasswordChangeView, extract_text_done, readmore_view, readmoreview, display_result

urlpatterns = [
    path('', views.base, name='base'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('about/', AboutView.as_view() , name='about'),
    path('readmore_classify/', readmore_view.as_view() , name='readmore_classify'),
    path('readmore_extract/', readmoreview.as_view() , name='readmore_extract'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('classify_document/', ClassifyDocumentView.as_view(), name='classify_document'),
    path('classify_document/done/', views.display_result, name='classify_document_done'),
    path('extract_text/', views.extract_text_or_table, name='extract_text'),
    path('extract_text/done/', extract_text_done, name='extract_text_done'),
    path('delete_account/', delete_account, name='delete_account'),
]