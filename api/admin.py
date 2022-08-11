from django.contrib import admin

# Register your models here.

from .models import User, Task, Team, Room, Team_task


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Team_task)