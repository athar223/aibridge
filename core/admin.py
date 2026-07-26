from django.contrib import admin

from .models import PromptHistory, Recommendation, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user_type", "created_at")
    list_filter = ("user_type", "created_at")
    search_fields = ("name", "email")
    ordering = ("-created_at",)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "goal_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("goal", "user__name")
    ordering = ("-created_at",)

    @admin.display(description="Goal")
    def goal_preview(self, obj):
        return (obj.goal[:75] + "…") if len(obj.goal) > 75 else obj.goal


@admin.register(PromptHistory)
class PromptHistoryAdmin(admin.ModelAdmin):
    list_display = ("task", "created_at")
    search_fields = ("task",)
    ordering = ("-created_at",)
