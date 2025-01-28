import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import folium
from streamlit_folium import folium_static
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyD9tJVuvqin0E8ZXQTr8APiPkWqF9iGk5U")

class ItineraryMaker:
    def __init__(self):
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
    
    def generate_itinerary(self, destination, days, interests):
        """Generate travel itinerary using Gemini API"""
        prompt = f"""Create a detailed {days}-day travel itinerary for {destination}. 
        Include recommendations based on these interests: {interests}. 
        Provide specific locations, estimated time at each location, 
        and brief descriptions of activities."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def voice_input(self):
        """Capture voice input from user"""
        with sr.Microphone() as source:
            st.write("Listening... Speak your input")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, could not understand audio")
            return None
    
    def text_to_speech(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def create_destination_map(self, destination):
        """Create interactive map for destination"""
        # Use folium to create map (you'd need to add geocoding logic)
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium_static(m)

def main():
    st.title("🌍 AI Travel Itinerary Planner")
    
    # Sidebar for inputs
    st.sidebar.header("Trip Details")
    
    # Voice input option
    if st.sidebar.button("🎤 Voice Input"):
        maker = ItineraryMaker()
        voice_input = maker.voice_input()
        if voice_input:
            st.sidebar.write(f"Recognized: {voice_input}")
    
    # Manual input fields
    destination = st.sidebar.text_input("Destination")
    days = st.sidebar.slider("Trip Duration", 1, 14, 3)
    interests = st.sidebar.multiselect(
        "Interests", 
        ["Culture", "Food", "Nature", "History", "Adventure", "Shopping"]
    )
    
    # Generate Itinerary Button
    if st.sidebar.button("Generate Itinerary"):
        maker = ItineraryMaker()
        
        # Generate and display itinerary
        itinerary = maker.generate_itinerary(destination, days, interests)
        st.write("### Your Personalized Itinerary")
        st.write(itinerary)
        
        # Create destination map
        maker.create_destination_map(destination)
        
        # Voice output option
        if st.checkbox("Read Itinerary Aloud"):
            maker.text_to_speech(itinerary)

if __name__ == "__main__":
    main()

# Required dependencies (install via pip):
# streamlit
# google-generativeai
# SpeechRecognition
# pyttsx3
# folium
# streamlit-folium
