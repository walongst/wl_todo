from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
	Title = models.CharField(max_length=200)
	Description = models.TextField(null=True,blank=True)
	complete = models.BooleanField(default=False)
	create = models.DateTimeField(auto_now_add=True)

	def __str__(self): 
		return self.Title

	class Meta:
		ordering = ['complete']	


class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default="")
    todo_list = models.ForeignKey(Task, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]