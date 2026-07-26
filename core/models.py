from django.db import models


class UserProfile(models.Model):
    class UserType(models.TextChoices):
        STUDENT = "student", "Student"
        FREELANCER = "freelancer", "Freelancer"
        TEACHER = "teacher", "Teacher"
        PROFESSIONAL = "professional", "Professional"
        SMALL_BUSINESS = "small_business", "Small Business Owner"

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STUDENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"


class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recommendations")
    goal = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recommendation for {self.user.name}"


class PromptHistory(models.Model):
    task = models.CharField(max_length=255)
    generated_prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Prompt histories"

    def __str__(self):
        return self.task
