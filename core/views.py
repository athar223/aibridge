import json

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm, PromptGeneratorForm, RecommenderForm
from .models import PromptHistory, Recommendation, UserProfile
from .services import generate_prompt, get_ai_recommendations
from .utils import LEARNING_RESOURCES


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def dashboard(request):
    total_users = UserProfile.objects.count()
    total_recommendations = Recommendation.objects.count()
    total_prompts = PromptHistory.objects.count()

    user_type_counts = []
    for value, label in UserProfile.UserType.choices:
        count = UserProfile.objects.filter(user_type=value).count()
        if count:
            user_type_counts.append({"label": label, "value": value, "count": count})

    recent_recommendations = Recommendation.objects.select_related("user")[:5]
    recent_prompts = PromptHistory.objects.all()[:5]

    context = {
        "total_users": total_users,
        "total_recommendations": total_recommendations,
        "total_prompts": total_prompts,
        "user_type_counts": user_type_counts,
        "user_type_labels_json": json.dumps([c["label"] for c in user_type_counts]),
        "user_type_values_json": json.dumps([c["count"] for c in user_type_counts]),
        "recent_recommendations": recent_recommendations,
        "recent_prompts": recent_prompts,
    }
    return render(request, "dashboard.html", context)


def recommender(request):
    result = None
    form = RecommenderForm()

    if request.method == "POST":
        form = RecommenderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            user_type = form.cleaned_data["user_type"]
            goal = form.cleaned_data["goal"]

            result = get_ai_recommendations(name, user_type, goal)

            user_profile, _ = UserProfile.objects.get_or_create(
                name=name, user_type=user_type, defaults={"email": ""}
            )
            Recommendation.objects.create(
                user=user_profile,
                goal=goal,
                ai_response=json.dumps(result),
            )

    context = {"form": form, "result": result}
    return render(request, "recommender.html", context)


def prompt_generator(request):
    result = None
    form = PromptGeneratorForm()

    if request.method == "POST":
        form = PromptGeneratorForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            result = generate_prompt(task)
            PromptHistory.objects.create(task=task, generated_prompt=json.dumps(result))

    context = {"form": form, "result": result}
    return render(request, "prompt_generator.html", context)


def resources(request):
    context = {"resource_categories": LEARNING_RESOURCES}
    return render(request, "resources.html", context)


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                "Thanks for reaching out! Our team will get back to you within 1-2 business days.",
            )
            return redirect("core:contact")

    context = {"form": form}
    return render(request, "contact.html", context)
