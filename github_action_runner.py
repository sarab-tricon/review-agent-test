import os
import json
import subprocess
from urllib.request import Request, urlopen
from workflows.review_workflow import create_review_workflow

def get_pr_details():
    pr_number = os.getenv("PR_NUMBER")
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not pr_number or not github_token:
        print("Error: PR_NUMBER or GITHUB_TOKEN not set")
        return None
    
    return {
        "pr_number": pr_number,
        "github_token": github_token
    }

def get_changed_files(pr_details):
    pr_number = pr_details["pr_number"]
    github_token = pr_details["github_token"]
    
    repo = os.getenv("GITHUB_REPOSITORY")
    
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    request = Request(url, headers=headers)
    
    try:
        with urlopen(request) as response:
            files = json.loads(response.read().decode())
            return files
    except Exception as e:
        print(f"Error fetching changed files: {e}")
        return []

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read() #string return
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def post_pr_comment(pr_details, comment_text):
    pr_number = pr_details["pr_number"]
    github_token = pr_details["github_token"]
    
    repo = os.getenv("GITHUB_REPOSITORY")
    
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = json.dumps({"body": comment_text}).encode('utf-8')
    request = Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urlopen(request) as response:
            print(f"Posted comment successfully")
            return True
    except Exception as e:
        print(f"Error posting comment: {e}")
        return False

def review_single_file(file_path, file_content):
    try:
        workflow = create_review_workflow()
        
        initial_state = {
            "code_content": file_content,
            "analyzer_result": {},
            "optimizer_result": {},
            "security_result": {},
            "documentation_result": {},
            "final_review": {}
        }
        
        result = workflow.invoke(initial_state)
        
        return {
            "file": file_path,
            "analyzer": result["analyzer_result"].get("content", ""),
            "optimizer": result["optimizer_result"].get("content", ""),
            "security": result["security_result"].get("content", ""),
            "documentation": result["documentation_result"].get("content", "")
        }
    except Exception as e:
        print(f"Error reviewing file {file_path}: {e}")
        return None

def format_review_comment(reviews):
    comment = "# 🤖 Code Review Agent Analysis\n\n"
    
    for review in reviews:
        if review:
            comment += f"## File: `{review['file']}`\n\n"
            
            comment += "### 🐛 Bug Analysis\n"
            comment += f"{review['analyzer']}\n\n"
            
            comment += "### ⚡ Optimization Suggestions\n"
            comment += f"{review['optimizer']}\n\n"
            
            comment += "### 🔒 Security Analysis\n"
            comment += f"{review['security']}\n\n"
            
            comment += "### 📚 Documentation Review\n"
            comment += f"{review['documentation']}\n\n"
            
            comment += "---\n\n"
    
    comment += "*Review completed by Code Review Agent*"
    
    return comment

def main():
    print("Starting Code Review Agent...")
    
    pr_details = get_pr_details()
    if not pr_details:
        return
    
    print(f"PR Number: {pr_details['pr_number']}")
    
    changed_files = get_changed_files(pr_details)
    if not changed_files:
        print("No changed files found or error fetching files")
        return
    
    print(f"Found {len(changed_files)} changed files")
    
    reviews = []
    
    for file_info in changed_files:
        file_path = file_info.get("filename")
    
        # Skip binary files, images, and non-code files
        skip_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', 
                      '.exe', '.bin', '.lock', '.pkl', '.pyc', '.o',
                      '.so', '.dll', '.app', '.dmg'}
    
        file_ext = os.path.splitext(file_path)[1].lower()
    
        if file_ext in skip_extensions:
            print(f"Skipping binary/image file: {file_path}")
            continue
    
        # Skip common config/data files that aren't code
        skip_patterns = ['node_modules/', 'venv/', '.git/', '__pycache__/', 
                     'package-lock.json', 'yarn.lock', '.env']
    
        if any(pattern in file_path for pattern in skip_patterns):
            print(f"Skipping dependency/config file: {file_path}")
            continue
        
        print(f"Reviewing file: {file_path}")
        
        file_content = read_file_content(file_path)
        if not file_content:
            continue
        
        review = review_single_file(file_path, file_content)
        if review:
            reviews.append(review)
    
    if reviews:
        comment = format_review_comment(reviews)
        post_pr_comment(pr_details, comment)
        print("Review comment posted to PR")
    else:
        print("No Python files to review or all reviews failed")

if __name__ == "__main__":
    main()