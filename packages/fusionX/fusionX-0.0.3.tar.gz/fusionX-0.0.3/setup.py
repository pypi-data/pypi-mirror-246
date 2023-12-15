

from setuptools import setup, find_packages


install_deps = ['numpy>=1.20.0', 'opencv-python>= 4.8.1.78', 'pickle5>=0.0.12']
VERSION = 'V0.0.3'
DESCRIPTION = 'fusionX'

# Setting up
setup(
    name="fusionX",
    version=VERSION,
    author="Bar Ben David, Suman Khan",
    author_email="<FusionX_pipeline@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="""
    This is a detailed description of your package.

    :Author: Bar Ben David , Suman Khan
    :Email: FusionX_pipeline@hotmail.com
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

