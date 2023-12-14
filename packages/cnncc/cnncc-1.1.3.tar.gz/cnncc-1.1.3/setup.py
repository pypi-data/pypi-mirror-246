from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("INSTRUCTIONS.md") as f:
    description = f.read()

setup(
    name="cnncc",
    version="1.1.3",
    packages=find_packages(),
    description="A simple CNN for cell-cycle phase classification",
    author="F.Dumoncel, E.Billard, S. Boudouh",
    install_requires=required,
    package_data={
        "cnncc": [
            "models/resnet/*.pt",
            "models/resnet/*.pth",
            "models/nagao/*.pth",
            "models/nagao/*.pt",
            "models/logreg/*.joblib",
        ],
    },
    entry_points={"console_scripts": ["cnncc = cnncc:main"]},
    long_description=description,
    long_description_content_type="text/markdown",
)
