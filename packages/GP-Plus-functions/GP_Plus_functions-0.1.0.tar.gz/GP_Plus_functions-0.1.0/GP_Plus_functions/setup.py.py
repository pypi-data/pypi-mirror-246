from setuptools import setup, find_packages

setup(
    name='GP_Plus_functions',  # This is the name of your package
    version='0.1.0',  # The initial release version
    author='Your Name',  # Your name or your organization/company name
    author_email='your.email@example.com',  # Your email address
    description='A short description of your package',  # A short description
    long_description=open('README.md').read(),  # A long description from your README file
    long_description_content_type='text/markdown',  # This is important if your README is in Markdown
    url='https://github.com/yourusername/your-repo',  # Link to your package's GitHub repo or website
    packages=find_packages(),  # Find all packages used
    install_requires=[
        # Any dependencies you have, e.g., 'numpy', 'torch', etc.
    ],
    classifiers=[
        # Classifiers help categorize your project and make it more discoverable
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the Python for your package
)

