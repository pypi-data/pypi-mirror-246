import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='area-calculator-dci1234',
    version='0.0.3',
    author='Maksym Kharchenko',
    decription='Calculate areas of geometrical figures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    keywords=['python', 'calculator', 'math',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
)