# AI Code Review Pre-commit Hook

A pre-commit hook that uses Ollama's CodeLlama model to perform automated code reviews on your staged changes.

## Features

- Analyzes code changes for:
  - Potential bugs and issues
  - Security concerns
  - Performance implications
  - Code style and best practices
  - Typos and grammar issues
- Provides detailed feedback with line numbers and suggested fixes
- Supports multiple file types (.py, .js, .ts, .jsx, .tsx, .cpp, .c, .java)
- Option to proceed or abort commit if issues are found

## Prerequisites

- Python 3.x
- Git
- [Ollama](https://ollama.ai/) running locally with the CodeLlama model

## Installation

There are two ways to set up the pre-commit hook:

### 1. Using setup_hook.py (Recommended)

This method automatically installs the hook in your git repository:

1. Clone this repository:

   ```bash
   git clone https://github.com/noxhsxrk/ai-pre-commit
   ```

2. Run the setup script:
   ```bash
   python setup_hook.py
   ```

### 2. Manual Installation with Shell Script

1. Create a shell script (e.g., `ai-precommit.sh`) with the following content:

   ```bash
   #!/bin/bash
   source ~/ai_code_reviewer/venv/bin/activate
   python3 ~/ai_code_reviewer/ai_code_reviewer.py
   ```

2. Make the script executable:

   ```bash
   chmod +x ai-precommit.sh
   ```

3. Add the script path to your pre-commit hook:

   ```bash
   echo '#!/bin/sh\n./ai-precommit.sh' > .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

4. Copy `pre-commit.py` to your repository's `.git/hooks` directory
5. Rename it to `pre-commit`
6. Make it executable:

   ```bash
   chmod +x .git/hooks/pre-commit
   ```

## Usage

After installation, the hook will automatically run when you attempt to commit changes. You'll see output like:

```
=== AI Code Review Results ===

=== Review for xxxxx ===

It looks like you have made some changes to an existing codebase, and I would be happy to help you identify any potential bugs or issues with your changes. Here are my suggestions for each of the five points you mentioned:

1. Potential bugs or issues:

2. Code style and best practices:

3. Security concerns:

4. Performance implications:

5. Typos and grammar issues:

```
