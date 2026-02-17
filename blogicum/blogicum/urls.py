from django.contrib import admin
from django.urls import include, path

from users import views as userviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls')),
    path('auth/registration/', userviews.RegistrationView.as_view(),
         name='registration'),
]

handler403 = 'pages.views.csrf_failure'

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_error'
