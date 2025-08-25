from dotenv import load_dotenv
from tkinter.messagebox import showinfo, showerror
from const import SYSTEM_PROMPT
import threading
import requests
import os

load_dotenv()


class QuestionFetcher:
    # too many mistakes/ wrong amount of questions / dumb answers, sometimes returns invalid JSON...
    llama_8b: str = 'llama-3.1-8b-instant'
    llama_70b: str = 'llama-3.3-70b-versatile'
    # OpenAI models provides better quiz questions than llamas so far...
    openai_preview_model_120b: str = 'openai/gpt-oss-120b'
    openai_preview_model_20b: str = 'openai/gpt-oss-20b'

    groq_completions_url: str = r'https://api.groq.com/openai/v1/chat/completions'
    groq_api_key: str = os.environ.get('GROQ_API_KEY')

    def __init__(self, topic: str, num_of_questions: int = 5, callback=None):
        self.topic = topic
        self.num_of_questions = num_of_questions
        self.callback = callback
        self.history: list = [
            SYSTEM_PROMPT,
            {"role": "user",
            "content": f"Generate me a quiz, on a {self.topic} topic, "
                       f"with {self.num_of_questions} questions"}]

        self.get_ai_response()

    def get_ai_response(self):
        headers: dict = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {QuestionFetcher.groq_api_key}"}

        payload: dict = {
            "model": QuestionFetcher.openai_preview_model_120b,
            # sends the last quiz topic + system prompt.
            "messages": self.history,
            "temperature": 0.6,
            "response_format": {"type": "json_object"}}

        def call_api():
            try:
                response = requests.post(QuestionFetcher.groq_completions_url, headers=headers, json=payload)
                response.raise_for_status()
                # print(response.status_code)
                data = response.json()
                message = data['choices'][0]['message']['content']
            except Exception as e:
                # TODO add some real exceptions, http errors 400, 401, 404 or whatever
                # TODO check if the data is malformed (not a valid JSON), retry the request with a short delay
                message = e
                showerror(title='Exception in call_api():', message=f'{e}')
            if self.callback:
                self.callback(message)

        # calling it in a thread so it doesn't freeze the UI
        threading.Thread(target=call_api).start()



