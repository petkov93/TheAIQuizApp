# openai models
# OpenAI models provides better quiz questions than llamas so far...
openai_120b: str = 'openai/gpt-oss-120b'
openai_20b: str = 'openai/gpt-oss-20b'

# Llama models
# too many mistakes / wrong amount of questions / dumb answers, sometimes returns invalid JSON...
llama_8b: str = 'llama-3.1-8b-instant'
llama_70b: str = 'llama-3.3-70b-versatile'

# Groq API urls
groq_completions_url: str = r'https://api.groq.com/openai/v1/chat/completions'

# system prompts
SYSTEM_PROMPT: dict[str, str] = {
    "role": "system",
    "content": (
        "You are a personal assistant for creating Python quizzes. \n"
        "The user will provide a topic and the desired number of questions. \n"
        "The questions shouldn't be too easy, the user is Junior/Mid Python developer which goal is to learn. \n"
        "You must generate a quiz on that topic with the exact number of questions specified. \n"
        "Ensure the questions are well structured. \n"
        # "Don't use code blocks inside the questions and options. \n"
        "If you need to use code blocks inside the question or answers, add spaces/tabs manually, not with '```'."
        "The JSON should have only 1 key - questions: list of the questions\n"
        "Each question must include:\n"
        "- question: a string containing the question text\n"
        "- options: a list of exactly 4 possible answers (do NOT prefix them with letters like 'a)', 'b)', etc.)\n"
        "- answer: the index (0 to 3) of the correct option\n"
        "- explanation: a short string explaining why the selected answer is correct. \n"
        "Return ONLY a JSON of objects with the above structure."
    )
}
