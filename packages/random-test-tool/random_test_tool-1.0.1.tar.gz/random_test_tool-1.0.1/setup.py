from setuptools import setup, find_packages

setup(
    name='random_test_tool',
    version='1.0.1',
    author='Antoine Rigoureau',
    author_email='antoine.rigoureau@xmco.fr',
    description='A simple python tool used form validating pseudo random generators output.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xmco/random_test_tool/"
)