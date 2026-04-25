from django.shortcuts import render
from .services.ai_engine import get_ai_response


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

