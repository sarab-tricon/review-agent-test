def format_code_review_prompt(code_content, agent_type):
    if agent_type == "analyzer":
        return f"""Analyze this code for bugs and logical errors.
        RESPOND WITH ONLY A BULLETED LIST. NO EXPLANATIONS.
Code:
{code_content}

Provide:
1. List of bugs found
2. Severity (critical/medium/low)
3. Line numbers where issues occur
4. Short explanation of each bug

If no bugs: "No bugs found"""

    elif agent_type == "optimizer":
        return f"""Suggest optimizations for this code.
Code:
{code_content}

Optimizations (if any):
- [Optimization]
- [Optimization]

If no optimizations: "No optimizations needed"""

    elif agent_type == "security":
        return f"""Check this code for security vulnerabilities.
Code:
{code_content}

Provide:
1. Security vulnerabilities found
2. Risk level (critical/high/medium/low)
3. Affected lines
4. How to fix each vulnerability in short

If none: "No security issues found"""

    elif agent_type == "documentation":
        return f"""Check code documentation quality.

        RESPOND WITH ONLY A BULLETED LIST. NO EXPLANATIONS.
Code:
{code_content}

Provide:
1. Missing documentation areas
2. Unclear variable/function names
3. Missing docstrings/comments

If none: "Documentation is adequate"""


def parse_agent_response(response_text):
    return {"content": response_text, "timestamp": None, "agent_type": None}


def combine_reviews(reviews_list):
    combined = {
        "bugs": [],
        "optimizations": [],
        "security_issues": [],
        "documentation_issues": [],
        "summary": "",
    }

    for review in reviews_list:
        if review:
            combined["summary"] += review.get("content", "") + "\n\n"

    return combined
