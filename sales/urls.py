
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    #path("",views.insert_person,name="insert"),
    path("start", views.start ,name="start"),
    path('submit_login/', views.submit_login, name='submit_login'),
    path('signup/',views.signup,name='signup'),
    path('submit_signup/', views.submit_signup, name='submit_signup'),
    path('shop/',views.shop,name="shop")
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

