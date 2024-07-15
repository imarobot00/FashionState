
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
    path('shop/',views.shop,name="shop"),
    path('retailer_login/', views.retailer_login, name='retailer_login'),
    path('retailer_dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
    path('shop/<int:id>/',views.product_detail, name='product_detail'),
    path('profile/',views.profile,name='profile'),
    path('cart/',views.cart,name='cart'),
    path('homepage/', views.homepage, name='homepage'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

