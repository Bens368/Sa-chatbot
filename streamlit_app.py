import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Sa-Chatbot")
st.write(
    "hello, I'm a chatbot here to introduce Sacha, a data scientist and machine learning teacher. I'll let you ask me any questions you like about it, in English or French, whichever you prefer !"
)

# Lecture du contenu du fichier texte directement depuis le fichier
with open('instructions.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Initialisation de l'état si nécessaire
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role":
        "system",
        "content":
        ("You're a curiculum vitae chatbot that introduces me to potential employers, freelance project applicants or anyone who'd like to get to know me from a professional point of view. From the start of the discussion, base yourself on the instructions.txt file, which contains all the information in my curiculum vitae. Your aim is to sell me and demonstrate my qualities and skills, both technical and softskills. Use a slightly formal tone, but be funny from time to time. Your goal is to be like a friend selling me on my merits. You need to base your application on my curriculum vitae, so don't invent skills or experience that don't appear in the instructions.txt document. if the person brings up a subject other than me and my professional experience, please bring it back to this subject. Use English or French depending on the language used by the user. if the user is unfamiliar with my area of expertise and has questions about what data science is or anything else, please don't hesitate to explain briefly. keep your answers short, especially if you're asked to give a general introduction."
        )
    }, {
        "role":
        "user",
        "content":
        f"Here is the content of the file:\n{file_content}"
    }]

# Afficher uniquement les messages utilisateur et assistant, en ignorant les deux premiers
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"],
                         avatar=message.get("avatar", 'robot.png')):
        st.markdown(message["content"])

# Saisie et gestion de l'entrée utilisateur
if prompt := st.chat_input("Votre texte ici"):
    # Ajouter le message de l'utilisateur à la liste des messages
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "avatar": 'user.png'
    })
    with st.chat_message("user", avatar='user.png'):
        st.markdown(prompt)

    # Envoi de la requête à OpenAI avec le contenu du fichier et les messages
    with st.chat_message("assistant", avatar='robot.png'):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Utiliser le mode de streaming pour un affichage progressif
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[{
                    "role": m["role"],
                    "content": m["content"]
                } for m in st.session_state.messages],
                stream=True,  # Activer le streaming
            )

            # Afficher le texte au fur et à mesure qu'il est reçu
            for chunk in response:
                content = chunk.choices[0].delta.get("content", "")
                full_response += content
                message_placeholder.markdown(
                    full_response +
                    "▌")  # Afficher le texte avec un curseur clignotant

            message_placeholder.markdown(
                full_response)  # Afficher la réponse finale sans le curseur
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Ajouter la réponse de l'IA à la session
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "avatar": 'robot.png'
    })
