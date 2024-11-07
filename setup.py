
from setuptools import setup, find_packages

setup(
  name='ai-pre-commit',
  version='1.0.0',
  packages=find_packages(),
  install_requires=[
      'requests',
  ],
  entry_points={
      'console_scripts': [
          'ai-pre-commit=ai_code_reviewer:main',
      ],
  },
)