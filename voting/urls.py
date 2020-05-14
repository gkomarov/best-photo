from django.urls import path
from voting import views

app_name = 'voting'
urlpatterns = []

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('update', views.VoteUpdate.as_view(), name='update')
]
