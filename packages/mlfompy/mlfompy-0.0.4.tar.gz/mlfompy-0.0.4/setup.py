from pathlib import Path
import setuptools
import re


def find_version():
    try:
        version_str = Path('VERSION').read_text().replace('\n','').strip()
        version_match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)",version_str, re.M)
        if version_match:
            return version_match.group(1)
    except:
        pass
    print("Unable to find version string.")
    return "0.0.0"


def get_long_description():
    long_description=''
    with open(Path(Path(__file__).parent,'README.md'), 'r') as fh:
        long_description=fh.read()
    return long_description

setuptools.setup(
    name='mlfompy',
    version=find_version(),
    description='MLFoMPy is an effective tool that extracts the main figures of merit (FoM) of a semiconductors IV curve',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='',
    author_email='',
    url='https://gitlab.citius.usc.es/modev/mlfompy',
    setup_requires=['setuptools','numpy'],
    install_requires=['pytest','scipy','matplotlib','numpy','pyocclient','yachalk','seaborn'],
    extras_require={
        'ML': ['torch','pytorch-lightning','torcheval','torchmetrics','scikit-learn'],
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
    ],
)

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools