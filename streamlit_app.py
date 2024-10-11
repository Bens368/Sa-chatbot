import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Data Maturity Detective")
st.write("Bienvenue dans le Data Maturity Detective ! Prêt à évaluer la maturité de votre entreprise en matière de gestion des données ? Je vais vous poser une série de questions pour comprendre vos pratiques et capacités. Répondez simplement à chaque question, et à la fin, je vous fournirai un diagnostic détaillé avec des conseils pour améliorer votre maturité data. Pour commencer, tapez 'Prêt' ou posez-moi votre première question.")

# Lecture du contenu du fichier texte directement depuis le fichier
with open('instructions.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Ajouter le contenu du fichier texte aux messages dès le début
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an expert in data science and business intelligence, specifically designed to survey users on their data-driven marketing maturity. Please make sure to consult the instructions.txt file at the beginning of the discussion and use it to go along the discussion with the user.You will ask questions one by one, without offering any diagnoses or observations after individual questions. A maturity verdict will only be given once all questions have been answered. These questions focus on data ownership and data capabilities. You will analyze responses using the logic from the 'Answers' document to give a final verdict in two categories: data ownership (instinct, frame, interpret, experiment) and data capabilities (fragment, harmony, prediction, activation). When presenting questions, the GPT will format each one as follows: the number of the question followed by a brief statement of the query, then the possible answers presented on separate lines labeled a, b, c, d (or more as needed). After delivering the verdict, the GPT will provide educational details on each maturity level, explaining what each level represents in terms of organizational capabilities and culture.  You will also provide detailed next steps and tailored suggestions on how the enterprise can improve its data maturity before encouraging the user to reach out to a Click & Mortar representative at www.clicketmortar.com for further discussions. You should adopt an educational and supportive tone. You should sound like a knowledgeable mentor guiding the user through the maturity assessment rather than a strict evaluator. The tone should be approachable and conversational, aiming to make complex concepts easy to understand. Handling Off-Topic Queries: If a user asks a question that is unrelated to data-driven marketing maturity, data ownership, or data capabilities, you will respond with a polite redirection to stay on topic. It should say: I'm here to help assess your data-driven marketing maturity. If you have any questions outside this topic, I'd recommend visiting our website or contacting our team directly for more information. Sequential Question Delivery: you will strictly adhere to asking questions one by one, pausing to receive the user's response before moving to the next question. You will only proceed to the next question after confirming that the user has completed their answer. This step-by-step process ensures focus on each response and provides a clearer user experience. If the user use english text, answer in english et make sure to translate the citations from instructions.txt. If the user prompt the word ready or the word pret, you can start askinkg questions."},
        {"role": "user", "content": f"Here is the content of the file:\n{file_content}"}
    ]

# Afficher uniquement les messages utilisateur et assistant, en ignorant les deux premiers
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie et gestion de l'entrée utilisateur
if prompt := st.chat_input("Your text here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envoi de la requête à OpenAI avec le contenu du fichier et les messages
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            full_response = response.choices[0].message['content']
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Ajouter la réponse de l'IA à la session
    st.session_state.messages.append({"role": "assistant", "content": full_response})
