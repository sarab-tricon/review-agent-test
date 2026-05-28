from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_NAME, TIMEOUT
from utils.helpers import format_code_review_prompt

client = Groq(api_key=GROQ_API_KEY)

def optimize_code(code_content):
    prompt = format_code_review_prompt(code_content, "optimizer")
    
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
    
    optimization_result = {
        "agent": "optimizer",
        "content": message.choices[0].message.content,
        "status": "completed"
    }
    
    return optimization_result