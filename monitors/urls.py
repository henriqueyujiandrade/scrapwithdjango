from django.urls import path

from . import views

urlpatterns = [
    path("monitors/", views.MonitorView.as_view(), name="monitors-data"),
    path("monitors/<pk>/", views.MonitorDetailView.as_view(), name="monitors-detail-data"),
    path("monitors/scrap", views.MonitorScrappingView.as_view(), name="base-monitors"),
    # path("products/<pk>/", views.ProductDetailView.as_view(), name="detail-products"),   
]