from setuptools import setup, find_packages

setup(
    name='GP_Plus_functions',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'torch',
        'gpytorch',
        'matplotlib',  # Assuming you use matplotlib for plotting
        'sobol_seq',  # Include this if it's a separate package you're using for sobol sequence generation
        'tabulate',  # Include if you're using tabulate for generating tables in your package
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
