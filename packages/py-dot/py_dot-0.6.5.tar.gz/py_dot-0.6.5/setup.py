import pathlib

import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

"""
>>> pip install twine

>>> py setup.py sdist bdist_wheel
... twine check dist/*
... twine upload dist/*

>>> py setup.py sdist bdist_wheel
... py -m twine check dist/*
... py -m twine upload dist/*
"""

setuptools.setup(
    name='py-dot',
    version='0.6.0',
    description='Python Base Development Library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/protyliss/py-dot',
    author='Protyliss',
    author_email='protyliss@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    packages=setuptools.find_packages(),
    include_package_data=True
    # install_requires=[]
    # entry_points={}
)
