from django.contrib import admin

# Register your models here.

from .models import Room, Task , User, Team, Team_task


admin.site.register(User)
admin.site.register(Team)
admin.site.register(Room)
admin.site.register(Task)
admin.site.register(Team_task)

