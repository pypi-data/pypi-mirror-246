from setuptools import setup, find_packages

setup(
    name="NetwrokScanning",  
    version="0.1",
    author="Abdirisaq",  
    author_email="abdirisaqmoa@outlook.com",
    license='MIT',  
    description="A Python package for network scanning and analysis working in the backend ",  
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZeusDevEng/NetworkScanning", 
    packages=find_packages(),
    install_requires=[
        "scapy>=2.5.0",

   ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Specify compatible Python versions
)
