# todo_list/todo_app/views.py
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,

)

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



from .models import ToDoItem, ToDoList

class CustomLoginView(LoginView):
	template_name='todo_app/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy("index")

class RegisterPage(FormView):
	template_name = 'todo_app/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True	
	success_url = reverse_lazy('index')

	def form_valid(self,form):
		user = form.save()
		if user is not None:
			login(self.request,user)
		return super(RegisterPage,self).form_valid(form)

	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage,self).get(*args,**kwargs) 	


class ListListView(LoginRequiredMixin,ListView):
	model = ToDoList
	template_name = "todo_app/index.html"
	context_object_name = 'user_tasks'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_tasks'] = context['user_tasks'].filter(user=self.request.user)

		return context


class ItemListView(LoginRequiredMixin,ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(LoginRequiredMixin,CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

    def form_valid(self,form):
    	form.instance.user = self.request.user
    	return super(ListCreate,self).form_valid(form)



class ItemCreate(LoginRequiredMixin,CreateView):
    model = ToDoItem
    fields = ['todo_list','title','description','due_date','complete']  

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['todo_list'].queryset = form.fields['todo_list'].queryset.filter(user=self.request.user)

        return form




    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemCreate(LoginRequiredMixin,CreateView):
    model = ToDoItem
    fields = ['todo_list','title','description','due_date','complete']  

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['todo_list'].queryset = form.fields['todo_list'].queryset.filter(user=self.request.user)

        return form




    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(LoginRequiredMixin,UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
        "complete",
    ]

    def get_form(self, form_class=None):
    	form = super().get_form(form_class=None)
    	form.fields['todo_list'].queryset = form.fields['todo_list'].queryset.filter(user=self.request.user)
    	return form

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(LoginRequiredMixin,DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(LoginRequiredMixin,DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context        


