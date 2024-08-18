import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from gtts import gTTS
import base64
import speech_recognition as sr
import yfinance as yf
import pandas as pd

# Load environment variables
load_dotenv()

def generate_ai_response(prompt, client):
    txt_path = os.path.join("store_files/tune_data.txt")
    if(os.path.exists(path=txt_path)):
        with open(txt_path, 'r') as file:
            tune_data = file.read()
    else:
        tune_data = ""
    csv_path = os.path.join("store_fies/bot_score.csv")
    if(os.path.exists(path=csv_path)):
        csv_data = pd.read_csv(csv_path)
    else:
        csv_data = pd.DataFrame()
    system_message = f"""You are a helpful AI assistant named as \"FinGPT\",that Provides concise responses that are only related to Finance, Market trends, insurance, etc. 
    You ONLY respond to the prompts that have topics realted to Finance. 
    You can Use the following information for giving better responses:

    Context Data:
    {tune_data}

    CSV Data consisting of Discount for the fitness score:
    {csv_data.to_string() if not csv_data.empty else "No CSV data"}

    """
    if "stock" in prompt.lower() or "$" in prompt:
        words = prompt.replace("$", "").split()
        potential_tickers = [word.upper() for word in words if word.isalpha() and len(word) <= 5]
        
        stock_info = ""
        for ticker in potential_tickers:
            stock_info += get_stock_info(ticker) + "\n"
        
        if stock_info:
            prompt += f"\n\nHere's the required information of the stock:\n{stock_info}"

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

def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        company_name = info.get('longName', 'Unknown Company')
        market_cap = info.get("marketCap", 0) / 1e9  # Convert to billions
        pe_ratio = info.get("trailingPE", "N/A")
        high_52w = info.get("fiftyTwoWeekHigh", "N/A")
        low_52w = info.get("fiftyTwoWeekLow", "N/A")
        return f"{company_name} (${ticker}) current price: ${current_price:.2f}, market cap: ${market_cap:.2f}B, P/E ratio: {pe_ratio:.2f}, 52-week high: ${high_52w:.2f}, 52-week low: ${low_52w:.2f}"
    except Exception as e:
        return f"Unable to fetch information for {ticker}. Error: {str(e)}"

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
        tts = gTTS(text=text, lang=lang)  
        # Setting the Path for audio file as Current working directory        
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
    st.logo("res\img\slider_logo.png",icon_image="res\img\page_icon.png")

    # Sidebar for settings
    with st.sidebar:
        st.title('🤖💸 FinGPT')
        hf_api_token = os.getenv("HF_API_TOKEN")

    
        # Files data Collecting and Segregating
        uploaded_files = st.file_uploader("Upload a Score and Context file", type=["csv", "txt"],accept_multiple_files=True,help="User can Upload Context and Score File Here")
        if uploaded_files:
            write_multipleFiles(uploaded_files,"store_files")
            
        

        #Clear Chat History 
        st.button('Clear Chat History', on_click=clear_chat_history)

    # Initialize the InferenceClient
    client = InferenceClient(
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        token=hf_api_token #API token to be inserted if not in .env
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today with Finance related queries?"}]
        
    # Counter for unique audio files
    if "audio_counter" not in st.session_state:
        st.session_state.audio_counter = 0

    

    # Display chat history
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        for index, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                col1, col2 = st.columns([8, 1])
                with col2:
                    # Text to Speech Button
                    def play_():
                        play_audio(message["content"],st.session_state.audio_counter,lang="en")
                        st.session_state.audio_counter += 1  # Increment the counter for each play
                    st.button("🔊",key=f"play_{index}",help="Text to Speech",use_container_width=False,on_click=play_)
                    
                        
    # Speech to Text button
    if st.button("Speak your message🎤",help="Speech to Text"):
        user_input = recognize_speech()
    else:
        user_input = st.chat_input("Type your quries related to finance, mutual funds...")     

        
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