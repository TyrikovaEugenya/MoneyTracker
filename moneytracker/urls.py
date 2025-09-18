from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dds.views import TransactionViewSet
from dds import views as trans_views
from catalogues.views import (
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    CategoryListAPIView,
    SubcategoryListAPIView
)
from catalogues import views as cat_views

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', trans_views.transaction_list, name='transaction_list'),
    path('create/', trans_views.transaction_create, name='transaction_create'),
    path('edit/<int:pk>/', trans_views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', trans_views.transaction_delete, name='transaction_delete'),
    path('api/', include(router.urls)),
    path('api/categories/', CategoryListAPIView.as_view(), name='api_categories'),
    path('api/subcategories/', SubcategoryListAPIView.as_view(), name='api_subcategories'),
    path('catalogue/', cat_views.catalogue_manage, name='catalogue_manage'),
    path('catalogue/status/delete/<int:pk>/', cat_views.delete_status, name='delete_status'),
    path('catalogue/type/delete/<int:pk>/', cat_views.delete_type, name='delete_type'),
    path('catalogue/category/delete/<int:pk>/', cat_views.delete_category, name='delete_category'),
    path('catalogue/subcategory/delete/<int:pk>/', cat_views.delete_subcategory, name='delete_subcategory'),
]
