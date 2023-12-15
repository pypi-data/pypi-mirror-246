from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'gold'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="gold33423310",
    version=VERSION,
    author="hanifaslamm",
    author_email="<aslamhanif141@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/syahrulcaem/gold33423310',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['gold','33423310'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)