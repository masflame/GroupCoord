from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('', views.login_view, name='login'),  # 👈 home route
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),  # Registration path
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('login/', LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login after logout

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
