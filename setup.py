from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name='MSR Asset Management',
    version='1.0.0',
    description='data mining of machine learning asset management dependents',
    author='Jimmy Zhao',
    author_email='z.zhao@queensu.ca',
    packages=find_packages(),
    install_requires=['PyGithub', 'python-gitlab', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3'
        'Operating System :: OS Independent'
    ]
)