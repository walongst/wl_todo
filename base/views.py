from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login

from . models import Task,ToDoItem


# Create your views here.

class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields='__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('tasks')

class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True	
	success_url = reverse_lazy('tasks')

	def form_valid(self,form):
		user = form.save()
		if user is not None:
			login(self.request,user)
		return super(RegisterPage,self).form_valid(form)

	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage,self).get(*args,**kwargs) 




class TaskList(LoginRequiredMixin,ListView):
	model = Task
	context_object_name = 'user_tasks'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_tasks'] = context['user_tasks'].filter(user=self.request.user)
		context['count'] = context['user_tasks'].filter(complete=False).count()
		search_input = self.request.GET.get('search-area') or ''
		if search_input:
			context['user_tasks']=context['user_tasks'].filter(
				Title__icontains=search_input)

		context['search_input']	= search_input
		return context

class TaskListList(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "base/item_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
	model = Task
	context_object_name = 'task'
	template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
	model = Task
	fields = ['Title','Description','complete']
	success_url = reverse_lazy('tasks')

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super(TaskCreate,self).form_valid(form)



class TaskUpdate(LoginRequiredMixin, UpdateView):
	model = Task
	fields = ['Title','Description','complete']
	success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
	model = Task
	context_object_name = 'user_tasks'
	success_url = reverse_lazy('tasks')



