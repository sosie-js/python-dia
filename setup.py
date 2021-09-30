from setuptools import setup, find_packages# List of requirements

with open("README.md", 'r') as fh:
    long_description = fh.read()

#demjson ?
requirements = [ "setuptools", "jsonpickle"," logging"]  # This could be retrieved from requirements.txt# Package (minimal) configuration

setup(
    name="pythondia",
    version="0.7.1",
    description="Python dia helpers to generate diagrams in dia from python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sosie",
    # author_email="sosie@sos-productions.com",
    keywords="dia python diagram helper",
    url="http://github.com/sosie-js/python-dia",
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements,
    python_requires='>=3.6',
)

