import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nkn-sdk',
    version='0.1.1',
    author='heron',
    author_email='peng.liu@nkn.org',
    description='NKN client and wallet SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nknorg/nkn-sdk-py3',
    packages=setuptools.find_packages(),
    install_requires=['pynacl', 'pycrypto', 'base58', 'requests', 'protobuf'],
    python_requires='>=3.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
