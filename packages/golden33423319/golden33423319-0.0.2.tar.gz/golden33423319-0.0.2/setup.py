from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'UAS'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="golden33423319",
    version=VERSION,
    author="Rafi Iqbal",
    author_email="<rafiiqbal2407@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/SeladaKeju/gold33423321',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['UAs', 'COY'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)