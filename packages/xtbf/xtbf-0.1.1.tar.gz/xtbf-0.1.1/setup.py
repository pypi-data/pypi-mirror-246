from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='xtbf',
    version='0.1.1',    
    description='A minimal, functional interface to the semiempirical extended tight-binding (xtb) program',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/Bayer-Group/xtbf',
    author='Jan Wollschläger',
    author_email='janmwoll@gmail.com',
    license='BSD 3-clause',
    packages=['xtbf'],
    install_requires=[
        'joblib', 'tqdm','numpy', 'pandas',
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
    ],
)