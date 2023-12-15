from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'UAS Daspro.'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="gold33423320",
    version=VERSION,
    author="rizalfarhan",
    author_email="<rizalfarhannanda@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/rizalfarhan/gold33423320',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['UAs', 'COY'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)