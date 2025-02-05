import streamlit as st
import google.generativeai as genai
from textblob import TextBlob
import speech_recognition as sr  # Add this import

# Check if PyAudio is installed
try:
    import pyaudio
except ImportError:
    pyaudio = None
    st.write("PyAudio is not installed. Please install it using 'pip install pyaudio'.")

# Set your API key
api_key = "AIzaSyB3x47UoudsF1fHgEvhQXbGIwu5emyybfs"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Streamlit UI: Title, Welcome Message, and User Input
st.title("Healthcare Chatbot")
st.header("Welcome to HealBot")  # Ensure this line displays "Welcome to HealBot"
st.write("Ask a healthcare-related question, and I'll try to answer it.")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    if pyaudio is None:
        st.write("PyAudio is not installed. Please install it to use voice input.")
        return ""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
    return ""

# User Input
question = st.text_input("Enter your healthcare question:")
if st.button("Use Voice Input"):
    question = recognize_speech()

# Initialize response variable
response_text = ""

# Create a function to handle the chatbot response
def get_healthcare_response(question):
    try:
        # Create and start the chat
        model = genai.GenerativeModel("gemini-pro")  # Replace with correct model name
        chat = model.start_chat(history=[])

        # Send the user's question to the chat and get a response
        response = chat.send_message(question)
        
        # Extract the response text
        response_text = response.text

        # Analyze sentiment
        sentiment = TextBlob(question).sentiment
        if sentiment.polarity < 0:
            response_text += "\n\nIt seems like you're feeling down. Remember to take care of yourself and seek support if needed. Here's a tip to cheer you up: Take a short walk outside and enjoy nature."

        return response_text
    except Exception as e:
        return f"An error occurred: {e}"

# Main interaction section
option = st.selectbox(
    'Choose an option:',
    ('Ask a Question', 'Drug Advice', 'Mental Health Protection', 'Pill Reminders', 'Daily Tips', 'Progress Tracking', 'Schedule of Doctors', 'Emergency Contact')
)

if option == 'Ask a Question':
    if st.button("Ask"):
        if question:
            response_text = get_healthcare_response(question)
        else:
            response_text = "Please enter a question."
    st.write("Answer: ", response_text)

elif option == 'Drug Advice':
    drug_question = st.text_input("Enter your drug-related question:")
    if st.button("Use Voice Input for Drug Advice"):
        drug_question = recognize_speech()
    if st.button("Get Drug Advice"):
        if drug_question:
            drug_response = get_healthcare_response(drug_question)
            st.write("Drug Advice: ", drug_response)
        else:
            st.write("Please enter a drug-related question.")

elif option == 'Mental Health Protection':
    mental_health_question = st.text_input("Enter your mental health question:")
    if st.button("Use Voice Input for Mental Health"):
        mental_health_question = recognize_speech()
    if st.button("Get Mental Health Advice"):
        if mental_health_question:
            mental_health_response = get_healthcare_response(mental_health_question)
            st.write("Mental Health Advice: ", mental_health_response)
        else:
            st.write("Please enter a mental health question.")

elif option == 'Pill Reminders':
    pill_reminder = st.text_input("Enter your pill reminder details:")
    if st.button("Set Pill Reminder"):
        if pill_reminder:
            st.write("Pill Reminder set for: ", pill_reminder)
        else:
            st.write("Please enter pill reminder details.")

elif option == 'Daily Tips':
    if st.button("Get Daily Tip"):
        daily_tip = get_healthcare_response("Give me a daily health tip")
        st.write("Daily Tip: ", daily_tip)

elif option == 'Progress Tracking':
    progress_details = st.text_input("Enter your progress details:")
    if st.button("Track Progress"):
        if progress_details:
            st.write("Progress tracked: ", progress_details)
        else:
            st.write("Please enter your progress details.")

elif option == 'Schedule of Doctors':
    doctor_schedule = st.text_input("Enter the doctor's schedule details:")
    if st.button("Set Doctor Schedule"):
        if doctor_schedule:
            st.write("Doctor's schedule set: ", doctor_schedule)
        else:
            st.write("Please enter the doctor's schedule details.")

elif option == 'Emergency Contact':
    emergency_contact = st.text_input("Enter your emergency contact details:")
    if st.button("Set Emergency Contact"):
        if emergency_contact:
            st.write("Emergency contact set: ", emergency_contact)
        else:
            st.write("Please enter your emergency contact details.")
