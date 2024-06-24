from django.urls import path
from .views import Task_List, Task_Detail, Task_Create, Task_Update, Task_Delete, CustomLogin_View, Register_Page, Logout_View
from .import views



urlpatterns=[
    path('login/', CustomLogin_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(next_page='login',http_method_names=['get', 'post', 'options']), name='logout'),
    path('register/', Register_Page.as_view(), name='register'),

    path('', Task_List.as_view(), name='tasks'),
    path('task/<int:pk>/', Task_Detail.as_view(), name='task'),
    path('task-create/', Task_Create.as_view(), name='task-create'),
    path('task-update/<int:pk>/', Task_Update.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', Task_Delete.as_view(), name='task-delete'),
]