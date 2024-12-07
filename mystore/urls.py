from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    # path('login/', views.login_user, name='login'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<int:pk>/', views.category, name='category'),  # Category page
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('store_page/<int:store_id>/', views.store_page, name='store_page'),
    path('stores/', views.store_list, name='store_list'),
    path('posting-product/', views.posting_product, name='posting_product'),
    path('set_store_location/', views.set_store_location, name='set_store_location'),
    path('store_map/', views.store_map, name='store_map'),
    path('profile_under_review', views.profile_under_review, name='profile_under_review'),
    path('submit_cart/', views.submit_cart, name='submit_cart'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    # path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store-detail'),
    # path('store/manage/', views.ManageStoreView.as_view(), name='manage-store'),  # For sellers to manage their stores
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)