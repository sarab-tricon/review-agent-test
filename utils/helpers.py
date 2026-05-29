def format_code_review_prompt(code_content, agent_type):
    if agent_type == "analyzer":
        return f"""Analyze code for bugs. RESPOND ONLY WITH BULLET POINTS.

Code:
{code_content}

ONLY output format:
- Line X: [Bug description]
- Line Y: [Bug description]

Example:
- Line 35: Division by zero when list is empty
- Line 22: KeyError if 'age' key missing

If no bugs: "No bugs found"
NO OTHER TEXT. NO EXPLANATIONS. ONLY BULLETS. """

    elif agent_type == "optimizer":
        return f"""Suggest optimizations. RESPOND ONLY WITH BULLET POINTS.

Code:
{code_content}

ONLY output format:
- Line X: [Optimization]
- Line Y: [Optimization]

Example:
- Line 32: Use sum() instead of loop for efficiency
- Line 28: Combine duplicate loops

If no optimizations: "No optimizations needed"
NO OTHER TEXT. NO EXPLANATIONS. ONLY BULLETS."""

    elif agent_type == "security":
        return f"""Find security vulnerabilities. RESPOND ONLY WITH BULLET POINTS.

Code:
{code_content}

ONLY output format:
- Line X: [Vulnerability description]
- Line Y: [Vulnerability description]

Example:
- Line 10: Hardcoded password visible in code
- Line 54: SQL injection risk in query construction

If none: "No security issues found"
NO OTHER TEXT. NO EXPLANATIONS. ONLY BULLETS."""

    elif agent_type == "documentation":
        return f"""Check documentation quality. RESPOND ONLY WITH BULLET POINTS.

Code:
{code_content}

ONLY output format:
- Line X: [Documentation issue]
- Line Y: [Documentation issue]

Example:
- Line 15: Missing docstring for function
- Line 8: Unclear variable name 'x'

If none: "Documentation is adequate"
NO OTHER TEXT. NO EXPLANATIONS. ONLY BULLETS."""


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
