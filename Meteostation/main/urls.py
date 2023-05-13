from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('table', views.table, name='table'),
    path('data', views.data, name='data'),
    path('data/', views.data, name='data'),
    # path('data/<slug:name>', views.TableView.as_view(), name='data-table')
    path('data/raw/<str:name>', views.table, name='data-table-raw'),
    path('data/<str:interpolation>/<str:name>', views.table, name='data-table-interpolated')
]
