from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    #path('', views.DashboardView.as_view(), name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view),
    path('', views.index, name ='index'),
    path('index_p/', views.patient_index, name ='patient_index'),
    path('<int:id>/', views.add_patient, name ='add_patient'),
    path('patients/', views.patients, name ='patients'),
    path('add_patient/', views.add_patient, name ='add_patient'),
    path('search_patient/', views.search_patient, name ='search_patient'),
    path('patient/<int:id>/', views.patient, name ='patient'),
    path('patient_diets/', views.patient_diets, name='patient_diets'),
    path('visits/', views.visits, name ='visits'),
    path('new_visit/', views.new_visit, name ='new_visit'),
    path('products/', views.products, name ='products'),
    path('search_product/', views.search_product, name ='search_product'),
    path('product/<int:id>/', views.product_details, name ='product_details'),
    path('new_product/', views.new_product, name ='new_product'),
    path('diets/', views.diets, name ='diets'),
    path('diets_all/', views.diets_all, name ='diets_all'),
    path('diet/<int:id>/', views.diet, name ='diet'),
    path('new_diet/', views.new_diet, name ='new_diet'),
    path('diet_meals/', views.diet_meals, name ='diet_meals'),
    path('meals/', views.meals, name ='meals'),
    path('new_meal/', views.new_meal, name ='new_meal'),
    path('meal_products/', views.meal_products, name ='meal_products'),
    path('meal/<int:id>/', views.meal, name ='meal'),
    path('reports/', views.reports, name ='reports'),
    path('openfoodapi/', views.openfoodapi, name ='openfoodapi'),
]