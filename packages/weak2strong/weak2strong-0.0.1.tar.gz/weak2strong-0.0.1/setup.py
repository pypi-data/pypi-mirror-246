import setuptools

setuptools.setup(
    name = "weak2strong",
    packages=["weak2strong"],
    version = "0.0.1",
    author = "OpenAI",
    author_email = "generalization@openai.com",
    # load from requirements.txt
    # install_requires=[line.strip() for line in open("requirements.txt")],
    install_requires=[],
    description = "",
    python_requires = ">=3.9"
)
