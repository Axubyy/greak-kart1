from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreListView.as_view(), name='store'),
    path('<slug:category_slug>/', views.StoreListView.as_view(),
         name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(),
         name='product-detail')
]
