
# FinGPT AI Assistant

**FinGPT** is a Streamlit-based AI assistant designed to provide concise and relevant information related to finance, market trends, insurance, and more. It uses Hugging Face models for generating AI responses and integrates various functionalities, such as speech recognition, text-to-speech, and real-time stock information retrieval.

## Features

- **Finance-Specific AI Assistant**: FinGPT provides accurate and context-aware responses to finance-related queries.
- **Real-Time Stock Information**: Automatically fetches and displays up-to-date stock information when relevant tickers are mentioned in the user prompt.
- **Speech-to-Text**: Allows users to interact with the assistant via voice commands.
- **Text-to-Speech**: Converts the assistant's responses to speech for an enhanced user experience.
- **Contextual Data**: Utilizes uploaded text and CSV files to fine-tune responses.
- **Session Management**: Includes functionality to clear chat history and maintain session state across interactions.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HarshSangani21/FinGPT-Chatbot.git
   cd FinGPT-Chatbot
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.7+ installed. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your Hugging Face API token:
   ```plaintext
   hf_api_token=your_hugging_face_api_token
   ```

## Usage

1. **Run the Application**:
   Start the Streamlit application by running:
   ```bash
   streamlit run app.py
   ```

2. **Interacting with FinGPT**:
   - **Type Your Queries**: Use the chat input to type any finance-related questions.
   - **Voice Commands**: Click the "Speak your message" button to use speech recognition.
   - **Text-to-Speech**: Listen to the assistant's responses by clicking the 🔊 button next to the messages.
   - **Upload Files**: Upload CSV and TXT files to enhance the assistant's contextual understanding.
   - **Clear Chat History**: Reset the conversation using the "Clear Chat History" button in the sidebar.

## Project Structure

- **app.py**: The main file containing the Streamlit application logic.
- **store_files/**: Directory where uploaded files are stored for context and score data.
- **res/**: Contains resources such as images used in the application and sample files.
- **.env**: Environment variables including your Hugging Face API token.
- **requirements.txt**: Python dependencies required to run the project.

## Dependencies

- **Streamlit**: For building the interactive web interface.
- **Hugging Face Hub**: To connect with Hugging Face's model inference API.
- **gTTS**: Google Text-to-Speech for converting text responses to audio.
- **SpeechRecognition**: For capturing and recognizing voice commands.
- **yfinance**: For retrieving real-time stock information.
- **Pandas**: For handling and processing CSV data.
- **dotenv**: For loading environment variables from a `.env` file.
- **Base64**: For encoding audio files in Base64 format for web use.

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Hugging Face for providing powerful NLP models.
- Google Text-to-Speech API for enabling text-to-speech functionality.
- Streamlit for creating an easy-to-use interface for machine learning applications.
- DJS InfoMatrix for guiding throughout, in making the project.
