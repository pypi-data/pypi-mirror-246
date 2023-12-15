from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name = "iobm",
    version = "0.5.4",
    author = "Mohammed Junaid",
    author_email = "junaid1607@outlook.com",
    description = "A simple conditional adverserial neural network module.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/MJ-GITHUB-007/cGAN",
    project_urls = {
        "GitHub" : "https://github.com/MJ-GITHUB-007/cGAN",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'iobm-train = iobm.cgan_train:run_cGAN_training',
            'iobm-generate = iobm.cgan_generate:run_cGAN_generating'
        ],
    },
    python_requires = ">=3.6",
    install_requires=[
        'Pillow',
        'torch',
        'torchvision',
        'tqdm',
    ],
    license='MIT',
)