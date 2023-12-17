from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='django-po-translation-message',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    version='0.1.0',
    author='Abdulaziz Baqaleb',
    author_email='ab.ah.bq@gmail.com',
    description='Get translated value from django.po file without requesting the language',
    packages=find_packages(),
    url= "https://github.com/i3z101/django-po-translation-message",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True
)