import setuptools

with open('README.md', 'r') as rm:
    long_description = rm.read()
    

setuptools.setup(
    name='reversed_name',
    version='0.0.1',
    author='SangDoo Nam',
    decription='reverses the characters in the name',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
    install_requires=[],
)