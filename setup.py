from setuptools import setup, find_packages

setup(
       name='ai-pre-commit',
       version='1.0.1',
       packages=find_packages(),
       install_requires=[
           'requests',
       ],
       entry_points={
           'console_scripts': [
               'ai-pre-commit=ai_pre_commit.ai_code_reviewer:main',
           ],
       },
)