import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Data Maturity Detective")
st.write(
    "Welcome to the Data Maturity Detective! Ready to assess your company's maturity in data management? I'm going to ask you a series of questions to understand your practices and capabilities. Simply answer each question, and at the end, I'll provide you with a detailed diagnosis along with advice to improve your data maturity. To begin, type 'Ready' or ask me your first question."
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
        ("You're a curiculum vitae chatbot that introduces me to potential employers, freelance project applicants or anyone who'd like to get to know me from a professional point of view. From the start of the discussion, base yourself on the instructions.txt file, which contains all the information in my curiculum vitae. Your aim is to sell me and demonstrate my qualities and skills, both technical and softskills. Use a slightly formal tone, but be funny from time to time. Your goal is to be like a friend selling me on my merits. You need to base your application on my curriculum vitae, so don't invent skills or experience that don't appear in the instructions.txt document.
    ")
    }, {
        "role":
        "user",
        "content":
        f"Here is the content of the file:\n{file_content}"
    }]

# Afficher uniquement les messages utilisateur et assistant, en ignorant les deux premiers
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"],
                         avatar=message.get("avatar", 'CM_image.png')):
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
    with st.chat_message("assistant", avatar='CM_image.png'):
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
        "avatar": 'CM_image.png'
    })
