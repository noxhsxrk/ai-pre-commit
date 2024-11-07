#!/usr/bin/env python3
import sys
import subprocess
import requests
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(
  level=logging.DEBUG,
  filename='ai_code_reviewer.log',
  filemode='a',
  format='%(asctime)s - %(levelname)s - %(message)s'
)

class AICodeReviewer:
  def __init__(self, ollama_url: str = "http://localhost:11434"):
      self.ollama_url = ollama_url
      self.model = "codellama"  # You can change this to any model you have in Ollama

  def get_staged_files(self) -> List[str]:
      """Get list of staged files for commit"""
      try:
          result = subprocess.run(
              ["git", "diff", "--cached", "--name-only"],
              capture_output=True,
              text=True,
              check=True
          )
          staged_files = result.stdout.strip().split('\n')
          logging.debug(f"Staged files: {staged_files}")
          return staged_files
      except subprocess.CalledProcessError as e:
          logging.error(f"Error getting staged files: {e}")
          return []

  def get_file_diff(self, file_path: str) -> str:
      """Get the diff for a specific file with minimal context to include line numbers"""
      try:
          # -U0 provides zero lines of context, making it easier to map changes to specific lines
          result = subprocess.run(
              ["git", "diff", "--cached", "-U0", file_path],
              capture_output=True,
              text=True,
              check=True
          )
          diff = result.stdout
          logging.debug(f"Diff for {file_path}:\n{diff}")
          return diff
      except subprocess.CalledProcessError as e:
          logging.error(f"Error getting diff for {file_path}: {e}")
          return ""

  def analyze_code(self, diff_content: str) -> str:
      """Send code to Ollama for analysis with detailed feedback request"""
      prompt = f"""
      Please review the following code changes and provide detailed feedback on:

      1. **Potential bugs or issues**
      3. **Security concerns**
      4. **Performance implications**
      5. **Typos and grammar issues**

      For each point above, please:
      - **Identify the specific line number(s) or code snippet(s) where the issue occurs.**
      - **Provide a clear description of the issue.**
      - **Suggest a concrete fix or improvement.**

      Here are the changes:
      {diff_content}

      Please format your feedback in the following manner:

      ### Potential bugs or issues:
      - **Line X:** Description of the issue.
        - **Suggested Fix:** [Your suggestion here]

      ### Code style and best practices:
      - **Line Y:** Description of the issue.
        - **Suggested Fix:** [Your suggestion here]

      ### Security concerns:
      - **Line Z:** Description of the issue.
        - **Suggested Fix:** [Your suggestion here]

      ### Performance implications:
      - **Line W:** Description of the issue.
        - **Suggested Fix:** [Your suggestion here]

      ### Typos and grammar issues:
      - **Line V:** Description of the issue.
        - **Suggested Fix:** [Your suggestion here]
      """

      payload = {
          "model": self.model,
          "prompt": prompt,
          "stream": False
      }

      try:
          logging.debug(f"Sending prompt to Ollama:\n{prompt}")
          response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
          response.raise_for_status()
          ai_response = response.json().get('response', '')
          logging.debug(f"Received response from Ollama:\n{ai_response}")
          return ai_response
      except requests.exceptions.RequestException as e:
          logging.error(f"Error connecting to Ollama: {e}")
          return f"Error connecting to Ollama: {str(e)}"

  def review_changes(self) -> Tuple[bool, str]:
      """Review all staged changes and compile feedback"""
      staged_files = self.get_staged_files()
      if not staged_files or staged_files[0] == '':
          return True, "No files staged for commit."

      all_feedback = []
      has_issues = False

      for file_path in staged_files:
          # Only process supported file types
          if not file_path.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.cpp', '.c', '.java')):
              logging.debug(f"Skipping unsupported file type: {file_path}")
              continue

          diff_content = self.get_file_diff(file_path)
          if not diff_content:
              logging.debug(f"No diff content for {file_path}, skipping.")
              continue

          feedback = self.analyze_code(diff_content)
          if "error" in feedback.lower():
              has_issues = True

          all_feedback.append(f"\n=== Review for {file_path} ===\n{feedback}")

      return not has_issues, "\n".join(all_feedback)

def main():
  reviewer = AICodeReviewer()
  success, feedback = reviewer.review_changes()

  print("\n=== AI Code Review Results ===")
  print(feedback)

  if not success:
      try:
          response = input("\nReview found potential issues. Do you want to proceed with the commit? (y/N) ").strip().lower()
          if response != 'y':
              print("Aborting commit.")
              sys.exit(1)
      except EOFError:
          print("No input available. Aborting commit.")
          sys.exit(1)

if __name__ == "__main__":
  main()