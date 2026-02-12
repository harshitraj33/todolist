from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListListView.as_view(), name='list_list'),
    path('<int:pk>/', views.ListDetailView.as_view(), name='list_detail'),
    path('<int:pk>/delete/', views.ListDeleteView.as_view(), name='list_delete'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('item/<int:pk>/toggle/', views.ItemToggleView.as_view(), name='item_toggle'),
    path('<int:pk>/add_item/', views.AddItemView.as_view(), name='add_item'),
]
