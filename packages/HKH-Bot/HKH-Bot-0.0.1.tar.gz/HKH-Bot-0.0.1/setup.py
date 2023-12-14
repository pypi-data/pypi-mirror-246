from setuptools import setup, find_packages

setup(name="HKH-Bot",
	  version="0.0.1",
	  author="HKH",
	  description="Let's make chatbots !",
	  packages=find_packages(),
	  install_requires=["faiss-cpu==1.7.4", "langchain==0.0.244", "sentence-transformers==2.2.2", "gpt4all==2.0.2", "PyMuPDF==1.22.5"]
)