#!/usr/bin/env python3
import os
import stat
from pathlib import Path

def setup_pre_commit_hook():
  # Get the git hooks directory
  git_dir = Path(os.popen('git rev-parse --git-dir').read().strip())
  hooks_dir = git_dir / 'hooks'
  pre_commit_path = hooks_dir / 'pre-commit'

  # Create the pre-commit hook file
  with open(pre_commit_path, 'w') as f:
      f.write('''#!/bin/sh
python3 .git/hooks/ai_code_reviewer.py
''')

  # Make the hook executable
  os.chmod(pre_commit_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

  # Copy the AI code reviewer script
  reviewer_path = hooks_dir / 'ai_code_reviewer.py'
  
  # Get the content of the first script
  current_dir = Path(__file__).parent
  with open(current_dir / 'ai_code_reviewer.py', 'r') as f:
      reviewer_content = f.read()

  # Write the content to the hooks directory
  with open(reviewer_path, 'w') as f:
      f.write(reviewer_content)

  print("Pre-commit hook installed successfully!")

if __name__ == "__main__":
  setup_pre_commit_hook()