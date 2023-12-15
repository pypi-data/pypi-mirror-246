from setuptools import setup, find_packages

setup(
    name='Quantagen',
    version='0.1.0',
    author='Christoffer Mattsson Langseth',
    author_email='christoffer@spatial.ist',
    description='A tool for Countagen users',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/christoffermattssonlangseth/quantagen',
    license='LICENSE',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'tifffile',
        'scikit-image',
        'matplotlib',
        # Add other dependencies as needed
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # Update these as per your compatibility
    ],
    python_requires='>=3.6',
)
