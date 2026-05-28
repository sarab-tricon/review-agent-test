def format_code_review_prompt(code_content, agent_type):
    if agent_type == "analyzer":
        return f"""Analyze this code for bugs and logical errors.
Code:
{code_content}

Provide:
1. List of bugs found
2. Severity (critical/medium/low)
3. Line numbers where issues occur
4. Brief explanation of each bug"""
    
    elif agent_type == "optimizer":
        return f"""Suggest optimizations for this code.
Code:
{code_content}

Provide:
1. Performance improvements
2. Code readability improvements
3. Before/after examples
4. Estimated performance gain"""
    
    elif agent_type == "security":
        return f"""Check this code for security vulnerabilities.
Code:
{code_content}

Provide:
1. Security vulnerabilities found
2. Risk level (critical/high/medium/low)
3. Affected lines
4. How to fix each vulnerability"""
    
    elif agent_type == "documentation":
        return f"""Check code documentation quality.
Code:
{code_content}

Provide:
1. Missing documentation areas
2. Unclear variable/function names
3. Suggested comments
4. Missing docstrings"""


def parse_agent_response(response_text):
    return {
        "content": response_text,
        "timestamp": None,
        "agent_type": None
    }


def combine_reviews(reviews_list):
    combined = {
        "bugs": [],
        "optimizations": [],
        "security_issues": [],
        "documentation_issues": [],
        "summary": ""
    }
    
    for review in reviews_list:
        if review:
            combined["summary"] += review.get("content", "") + "\n\n"
    
    return combined