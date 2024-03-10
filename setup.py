from setuptools import setup, find_packages

setup(
    name='tinydes',  
    version='0.1.0', 
    author='Asad',  
    author_email='asadali047@gmail.com'
    description='A tiny discrete event simulation library',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://github.com/Asad1287/tinydes', 
    packages=find_packages(), 
    include_package_data=True, 
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
    classifiers=[
        
        'Development Status :: 4 - Beta',  
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10', 
        
    ],
    python_requires='>=3.6',  
    entry_points={
       
        'console_scripts': [
            'tinydes-cli=tinydes.cli:main',  
        ],
    },
)


