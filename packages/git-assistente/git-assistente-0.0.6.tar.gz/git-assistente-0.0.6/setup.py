from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='git-assistente',
    version='0.0.6',
    license='MIT License',
    author='CarlosAllberto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='dasilvacarlosalberto344@gmail.com',
    keywords='git assistente',
    description='Um assistente do Git para subir projetos no GitHub',
    packages=find_packages(),
    package_data={'git_assistente': ['core/*.py', 'utils/*.py']},
    install_requires=['colorama', 'dankware'],
    entry_points={"console_scripts": ["assistente = git_assistente.__main__:main"]},)