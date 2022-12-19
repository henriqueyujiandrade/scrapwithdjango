from django.urls import path

from . import views

urlpatterns = [
    path("monitors/", views.MonitorView.as_view(), name="base-monitors"),
    # path("products/<pk>/", views.ProductDetailView.as_view(), name="detail-products"),   
]