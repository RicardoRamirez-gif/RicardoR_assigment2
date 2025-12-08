import openai
import os
# from dotenv import load_dotenv # Uncomment when needed

# Load API Key from environment variables (professional standard)
openai.api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_placeholder')

def summarize_text(text: str) -> str:
    """Uses OpenAI API to summarize text content."""
    # Ensure API key is set before proceeding
    if not openai.api_key or openai.api_key == 'your_openai_api_key_placeholder':
        print("❌ Warning: OPENAI_API_KEY not set. Skipping summarization.")
        return "Summary not available (API key missing)."
    
    try:
        # Send the extracted text to OpenAI's GPT model for summarization
        # NOTE: Using 'completions' API (text-davinci-003) is legacy. 
        # For a modern approach, consider using chat completions (gpt-3.5-turbo or gpt-4)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"❌ Error summarizing text with OpenAI: {e}")
        return f"Summary Error: {e}"

# You can add the sentiment analysis logic here later
# def get_sentiment(text): ...