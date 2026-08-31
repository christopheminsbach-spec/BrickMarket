from django.shortcuts import render
from ollama import chat


def bot_view(request):

    conversation = request.session.get(
        "conversation",
        []
    )

    visible_messages = [
        m for m in conversation
        if m["role"] != "system"
    ]

    return render(
        request,
        "bot/conversation.html",
        {
            "conversation": visible_messages
        }
    )


def bot_action(request):

    conversation = request.session.get(
        "conversation",
        []
    )


    if not conversation:

        conversation = [
            {
                "role": "system",
                "content": (
                    "Tu es Brick, assistant de la boutique Brickmarket. "
                    "Tu aides uniquement pour les LEGO. "
                    "Réponds de manière concise et amicale. "
                    "Si la question ne concerne pas LEGO, refuse poliment."
                ),
            }
        ]


    user_request = request.POST.get("message")


    if user_request:

        conversation.append(
            {
                "role": "user",
                "content": user_request
            }
        )


        response = chat(
            model="gemma3:1b",
            messages=conversation
        )


        assistant_message = (
            response["message"]["content"]
            if isinstance(response, dict)
            else response.message.content
        )


        conversation.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )


    request.session["conversation"] = conversation

    request.session.modified = True


    visible_messages = [
        m for m in conversation
        if m["role"] != "system"
    ]


    return render(
        request,
        "bot/conversation.html",
        {
            "conversation": visible_messages
        }
    )