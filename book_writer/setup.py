from setuptools import setup, find_packages

setup(
    name="book_writer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.32.0",
        "langchain==0.1.12",
        "google-generativeai==0.3.2",
        "python-dotenv==1.0.1",
        "pydantic==2.6.3"
    ],
    author="Eder Jani Martins",
    author_email="zetared@gmail.com",
    description="Assistente de escrita de livros com IA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/book_writer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 