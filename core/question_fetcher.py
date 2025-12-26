import os
import threading
from tkinter.messagebox import showerror

import requests
from dotenv import load_dotenv

from data.quiz_fetcher_data import SYSTEM_PROMPT, openai_120b, groq_completions_url

load_dotenv()


class QuestionFetcher:
    def __init__(self, topic: str, num_of_questions: int = 5, callback=None):
        self.topic = topic
        self.num_of_questions = num_of_questions
        self.callback = callback

        self.model = openai_120b
        self.endpoint = groq_completions_url
        self.api_key: str = os.environ.get('GROQ_API_KEY')
        self.history: list = [
            SYSTEM_PROMPT,
            {"role": "user",
             "content": f"Generate me a quiz, on a {self.topic} topic, "
                        f"with {self.num_of_questions} questions"}]

        # TODO remove this method call, call the method in the manager
        self.get_ai_response()

    def get_ai_response(self):
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}

        payload: dict[str, str] = {
            "model": self.model,
            # sends the last quiz topic + system prompt.
            "messages": self.history,
            "temperature": 0.1,
            "response_format": {"type": "json_object"}}

        def call_api():
            try:
                response = requests.post(self.endpoint, headers=headers, json=payload)
                response.raise_for_status()
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
