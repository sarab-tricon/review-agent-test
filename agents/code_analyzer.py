from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_NAME, TIMEOUT
from utils.helpers import format_code_review_prompt

client = Groq(api_key=GROQ_API_KEY)

def analyze_code(code_content):
    prompt = format_code_review_prompt(code_content, "analyzer")
    
    message = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1500,
        temperature=0.7,
        timeout=TIMEOUT
    )
    
    analysis_result = {
        "agent": "code_analyzer",
        "content": message.choices[0].message.content,
        "status": "completed"
    }
    
    return analysis_result