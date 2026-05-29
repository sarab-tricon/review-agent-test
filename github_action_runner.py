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

    return {"pr_number": pr_number, "github_token": github_token}


def get_changed_files(pr_details):
    pr_number = pr_details["pr_number"]
    github_token = pr_details["github_token"]

    repo = os.getenv("GITHUB_REPOSITORY")

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
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
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()  # string return
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
        "Accept": "application/vnd.github.v3+json",
    }

    data = json.dumps({"body": comment_text}).encode("utf-8")
    request = Request(url, data=data, headers=headers, method="POST")

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
            "final_review": {},
        }

        result = workflow.invoke(initial_state)

        return {
            "file": file_path,
            "analyzer": result["analyzer_result"].get("content", ""),
            "optimizer": result["optimizer_result"].get("content", ""),
            "security": result["security_result"].get("content", ""),
            "documentation": result["documentation_result"].get("content", ""),
        }
    except Exception as e:
        print(f"Error reviewing file {file_path}: {e}")
        return None


def format_review_comment(reviews):
    comment = "## 🤖 Code Review Results\n\n"

    has_any_issues = False

    for review in reviews:
        if review:
            file_name = review["file"]
            file_has_issues = False
            file_comment = f"### 📄 `{file_name}`\n"

            # Check for CRITICAL ISSUES (only if analyzer found any)
            analyzer_text = review["analyzer"].lower()
            if any(x in analyzer_text for x in ["line", "bug", "error", "crash"]):
                critical_lines = []
                for line in review["analyzer"].split("\n"):
                    line = line.strip()
                    if not line or len(line) < 5:
                        continue
                    if any(x in line.lower() for x in ["line", "bug", "error"]):
                        if not any(
                            x in line.lower() for x in ["okay", "let's", "first"]
                        ):
                            clean = line.lstrip("-•").strip()
                            if clean and clean not in critical_lines:
                                critical_lines.append(clean)

                if critical_lines:
                    file_comment += "**🔴 Critical Issues:**\n"
                    for issue in critical_lines[:3]:
                        file_comment += f"- {issue}\n"
                    file_comment += "\n"
                    file_has_issues = True

            # Check for SECURITY ISSUES (only if security agent found any)
            security_text = review["security"].lower()
            if any(
                x in security_text
                for x in ["line", "vulnerability", "security", "risk"]
            ):
                security_lines = []
                for line in review["security"].split("\n"):
                    line = line.strip()
                    if not line or len(line) < 5:
                        continue
                    if any(
                        x in line.lower()
                        for x in ["line", "vulnerability", "security", "risk"]
                    ):
                        if not any(
                            x in line.lower() for x in ["okay", "let's", "first"]
                        ):
                            clean = line.lstrip("-•").strip()
                            if clean and clean not in security_lines:
                                security_lines.append(clean)

                if security_lines:
                    file_comment += "**🔒 Security Concerns:**\n"
                    for issue in security_lines[:3]:
                        file_comment += f"- {issue}\n"
                    file_comment += "\n"
                    file_has_issues = True

            # Check for OPTIMIZATIONS (only if optimizer found any)
            optimizer_text = review["optimizer"].lower()
            if any(
                x in optimizer_text
                for x in ["line", "optimization", "improve", "refactor", "performance"]
            ):
                optimization_lines = []
                for line in review["optimizer"].split("\n"):
                    line = line.strip()
                    if not line or len(line) < 5:
                        continue
                    if any(
                        x in line.lower()
                        for x in ["line", "optimization", "improve", "refactor"]
                    ):
                        if not any(
                            x in line.lower() for x in ["okay", "let's", "first"]
                        ):
                            clean = line.lstrip("-•").strip()
                            if clean and clean not in optimization_lines:
                                optimization_lines.append(clean)

                if optimization_lines:
                    file_comment += "**⚡ Optimizations:**\n"
                    for opt in optimization_lines[:3]:
                        file_comment += f"- {opt}\n"
                    file_comment += "\n"
                    file_has_issues = True

            # Check for DOCUMENTATION ISSUES (only if documentation agent found any)
            doc_text = review["documentation"].lower()
            if any(
                x in doc_text
                for x in ["line", "docstring", "documentation", "comment", "unclear"]
            ):
                doc_lines = []
                for line in review["documentation"].split("\n"):
                    line = line.strip()
                    if not line or len(line) < 5:
                        continue
                    if any(
                        x in line.lower()
                        for x in [
                            "line",
                            "docstring",
                            "documentation",
                            "comment",
                            "unclear",
                        ]
                    ):
                        if not any(
                            x in line.lower()
                            for x in ["okay", "let's", "first", "adequate"]
                        ):
                            clean = line.lstrip("-•").strip()
                            if clean and clean not in doc_lines:
                                doc_lines.append(clean)

                if doc_lines:
                    file_comment += "**📚 Documentation:**\n"
                    for doc in doc_lines[:3]:
                        file_comment += f"- {doc}\n"
                    file_comment += "\n"
                    file_has_issues = True

            # Only add file comment if it has issues
            if file_has_issues:
                comment += file_comment
                has_any_issues = True

    if not has_any_issues:
        comment += "✅ **No issues found!** Code looks good.\n\n"

    comment += "---\n*Automated review by Code Review Agent*"

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
        skip_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pdf",
            ".zip",
            ".exe",
            ".bin",
            ".lock",
            ".pkl",
            ".pyc",
            ".o",
            ".so",
            ".dll",
            ".app",
            ".dmg",
        }

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in skip_extensions:
            print(f"Skipping binary/image file: {file_path}")
            continue

        # Skip common config/data files that aren't code
        skip_patterns = [
            "node_modules/",
            "venv/",
            ".git/",
            "__pycache__/",
            "package-lock.json",
            "yarn.lock",
            ".env",
        ]

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
