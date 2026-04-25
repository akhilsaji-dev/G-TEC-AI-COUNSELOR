from django.shortcuts import render
from .services.ai_engine import get_ai_response
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def chat_view(request):
    result = None

    if request.method == "POST":
        user_input = request.POST.get("message")
        # result = get_ai_response(user_input)
         # 👇 AI response (plain text)
        ai_text = get_ai_response(user_input)

        # 👇 Convert to styled HTML
        result = format_response(ai_text)

    return render(request, "chat.html", {"response": result})

def format_response(text):
    text = text.replace("**", "").replace("*","")  # Remove carriage returns

    lines = text.split("\n")
    html = ""
    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Heading
        if line.startswith("###"):
            if in_list:
                html += "</ul>"
                in_list = False
            html += f"<h3 style='color:#00eaff'>{line.replace('###','',)}</h3>"

        # Bullet points
        elif line.startswith("-"):
            if not in_list:
                html += "<ul>"
                in_list = True
            html += f"<li>{line.replace('-','')}</li>"

        # Normal text
        else:
            if in_list:
                html += "</ul>"
                in_list = False
            html += f"<p>{line}</p>"

    if in_list:
        html += "</ul>"

    return f"<div style='color:white'>{html}</div>"



@login_required(login_url='/login/')
def counselor_view(request):
    return render(request, 'counselor.html')

# HOME
def home(request):
    return render(request, 'core/home.html')

# ABOUT
def about(request):
    return render(request, 'core/about.html')

# FAQ
def faq(request):
    return render(request, 'core/faq.html')

# REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # create user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "core/register.html")
# LOGIN


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")  # IMPORTANT
        else:
            return render(request, "core/login.html", {"error": "Invalid credentials"})

    return render(request, "core/login.html")

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

