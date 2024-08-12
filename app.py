import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from gtts import gTTS
import base64
import speech_recognition as sr
import yfinance as yf

# Load environment variables
load_dotenv()

def generate_ai_response(prompt, client):
    with open('/res/files/tune_data.txt', 'r') as file:
        tune_data = file.read()
    system_message = "You are a helpful AI assistant named as \"FinGPT\". Provide concise responses that are only related to Finance. You ONLY respond to the prompts that have topics realted to Finance. "+ tune_data
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    response = ""
    for message in client.chat_completion(
        messages=messages,
        max_tokens=120,
        stream=True
    ):
        response += message.choices[0].delta.content or ""
    
    return response

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# Function for Writing Multiple files
def write_multipleFiles(files,save_directory):
    for file in files:
        data = file.read()
        save_path = os.path.join(save_directory, file.name)
        
        # Write the data to a new file in the specified directory
        with open(save_path, 'wb') as output_file:
            output_file.write(data)
            
            
# Audio base64 Converter function
def audio_to_base64(audio_file):
        with open(audio_file, "rb") as file:
            audio_bytes = file.read()
        return base64.b64encode(audio_bytes).decode()

def play_audio(text,file_index, lang='en'):
    # Generate the audio file only once
    if f"response{file_index}" not in st.session_state:
        # Convert the text to speech
        tts = gTTS(text=text, lang='en')  
        # Setting the Path for audio file          
        audio = os.path.join(os.getcwd(), f"response{file_index}.mp3")
        # Save the audio file
        tts.save(audio)
        # Store the audio file in the session state
        st.session_state[f"response{file_index}"] = audio

    # Converting to Audio base64
    audio_file = st.session_state[f"response{file_index}"]
    audio_base64 = audio_to_base64(audio_file)

    # HTML string with the hidden audio player that autoplays
    audio_html = f"""
    <audio autoplay style="display:none;">
    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>"""
    st.markdown(audio_html, unsafe_allow_html=True)
    
    # Delete the file after playing 
    os.remove(audio)

# Define the function to recognize speech
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            user_input = r.recognize_google(audio)
            st.write("You said:", user_input)
            return user_input
        except sr.UnknownValueError:
            st.warning("Sorry, I didn't understand what you said.")
        except sr.RequestError:
            st.write("Sorry, there was an issue with the speech recognition service.")
        return None   


def main():
    st.set_page_config("FinGPT",page_icon="res\img\page_icon.png",)
    st.header('FinGPT AI Assistant',divider="rainbow",anchor=False)
    # slider_logo= "res\img\slider_logo.png"
    st.logo("res\img\slider_logo.png",icon_image="res\img\page_icon.png")

    # Sidebar for settings
    with st.sidebar:
        st.title('🤖💸 FinGPT')
        hf_api_token = os.getenv("hf_xxxxxxxxxxxxxxxxxxxxxxxxx")

    
        # Files data Collecting and Segregating
        uploaded_files = st.file_uploader("Upload a Score and Context file", type=["csv", "txt"],accept_multiple_files=True,help="User can Upload Context and Score File Here")
        if uploaded_files:
            write_multipleFiles(uploaded_files,"store_files")
            
        

        #Clear Chat History 
        st.button('Clear Chat History', on_click=clear_chat_history)

    # Initialize the InferenceClient
    client = InferenceClient(
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        token="hf_xxxxxxxxxxxxxxxxxxxxxxxxx" #API token
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        
    # Counter for unique audio files
    if "audio_counter" not in st.session_state:
        st.session_state.audio_counter = 0

    with st.container():

        col1,col2 = st.columns([8,1])

    
        # Display chat history
        for index, message in enumerate(st.session_state.messages):
            with st.container():
                with col1:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                
                with col2:
                    st.markdown("""
                    <style>
                        div[data-testid="col2"] * {
                            width: fit-content !important;
                            gap: 3;
                        }
                    </style>
                    """, unsafe_allow_html=True)
            
                    def play_():
                        play_audio(message["content"],st.session_state.audio_counter,lang="en")
                        st.session_state.audio_counter += 1  # Increment the counter for each play
                # with col6:    
                    st.button("🔉",key=f"play_{index}",help="Text to Speech",use_container_width=False,on_click=play_)

     
    
   
    
    # Speech to Text button
    if st.button("Speak your message🎤",help="Speech to Text"):
        user_input = recognize_speech()
    else:
        user_input = st.chat_input("Type your message here...")     

        
    # User input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        response = generate_ai_response(user_input, client)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
                
        

if __name__ == "__main__":
    main()