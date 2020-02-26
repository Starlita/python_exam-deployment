from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.createUser),
    path('login', views.loginUser), 
    path('logout', views.logout),
    path('thoughts', views.showThoughts),
    path('add', views.addThought), 
    path('onethought/<int:thought_id>', views.show_one_thought),
    path('delete/<int:thought_id>', views.deleteThought),
    path('make/<int:thought_id>', views.makeLike),
    path('unlike/<int:thought_id>', views.unlike),
    #path('<path:path>', views.sendHome)
]