from django.shortcuts import render, redirect
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .models import Task
# FormVie, a class based view for user registration

class CustomLogin_View(LoginView):
    template_name = 'base/login.html'
    fields ='__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class Logout_View(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('login')


# Create your views here.
# class based views
# this is not a function based model views

class Task_List(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'

    # user restriction of task
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__istartswith = search_input)
            context['search_input']=(search_input)

        return context


class Task_Detail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= 'task'
    template_name= 'base/task.html'

class Task_Create(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Task_Create, self).form_valid(form)

class Task_Update(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')


class Task_Delete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')


class Register_Page(FormView):
    template_name= 'base/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user= True
    success_url = reverse_lazy('tasks')
    
    # redirecting user once the form is completed
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(Register_Page, self ).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
          return redirect('tasks')
        return super(Register_Page, self).get(*args, **kwargs)


