from django.urls import path

from . import views

app_name = "leads"
urlpatterns = [
    path("", views.LeadListView.as_view(), name="list"),
    path("create/", views.LeadCreateView.as_view(), name="create"),
    path("assign-agent/<int:pk>", views.AssignAgentView.as_view(), name="assign_agent"),
    path("assign-category/<int:pk>", views.LeadCategoryUpdateView.as_view(), name="assign_category"),
    path("detail/<int:pk>", views.LeadDetailView.as_view(), name="detail"),
    path("update/<int:pk>", views.LeadUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.LeadDeleteView.as_view(), name="delete"),
    path("category", views.CategoryListView.as_view(), name="category"),
    path("category/create", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>", views.CategoryDetailView.as_view(), name="category_detail"),
    path("category/update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("category/delete/<int:pk>", views.CategoryDeleteView.as_view(), name="category_delete"),
]