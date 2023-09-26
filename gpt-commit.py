import subprocess
import openai
import os

def get_git_diff():
    """Get the difference between the git index and head."""
    result = subprocess.run(['git', '--no-pager', 'diff', '--cached'], capture_output=True, text=True)
    return result.stdout

def get_commit_message_from_chatgpt(diff_output):
    """Prompt ChatGPT for a commit message based on the git diff."""

    # Retrieve API key from environment variable
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set!")
        return

    openai.api_key = openai_api_key

    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Based on the following git diff:\n\n{diff_output}\n\nProvide a commit message describing the changes:",
      max_tokens=100
    )
    message = response.choices[0].text.strip()
    return message

def main():
    diff_output = get_git_diff()
    print(diff_output)
    if not diff_output:
        print("No changes detected. Exiting.")
        return

    commit_message = get_commit_message_from_chatgpt(diff_output)
    if commit_message:
        subprocess.run(['git', 'commit', '-m', commit_message])
        print(f"Committed with message: {commit_message}")

if __name__ == "__main__":
    main()

