from setuptools import setup, find_packages

setup(
    name='hashsystem',
    version='1.0',
    author='Rajat Mishra',
    author_email='rajatsmishra@aol.com',
    description='hashsystem helps developers generate hash passwords and generate token and decode token,that can be used in jwt ,apitokens,any kind of encription and decription process.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)