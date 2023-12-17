from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as reader:
    description = reader.read()

setup(
    name="jodev_emailpy",
    version="0.1.1",
    description="A python library for recieving email directly in your application using emailjs",
    url="https://github.com/joelwry/jodev_emailpy",
    author="joelwry",
    author_email="joelwryjolomi@gemail.com",
    packages=find_packages(),
    install_requires=["requests"],  # Change 'requires' to 'install_requires'
    license="MIT",
    long_description=description,
    long_description_content_type="text/markdown",  # Specify the content type as Markdown
    keywords=['emailjs', 'email', 'email sender', 'email reciever']
)
