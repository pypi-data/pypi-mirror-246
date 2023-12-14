

from setuptools import setup, find_packages


install_deps = ['numpy>=1.20.0']
VERSION = '0.0.4'
DESCRIPTION = 'fusionx20'

# Setting up
setup(
    name="fusionx20",
    version=VERSION,
    author="FusionX",
    author_email="<bar.bendavid@weiamann.ac.il>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="""
    This is a detailed description of your package.

    :Author: Barben 
    :Email: your.email@example.com
    """
,
 
    packages=find_packages(),
    install_requires=install_deps,
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

