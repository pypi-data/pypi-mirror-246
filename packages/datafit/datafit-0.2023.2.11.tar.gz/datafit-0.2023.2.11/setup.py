from setuptools import setup, find_packages

longDescription = """
## DataFit
DataFit is a python package developed for automating data preprocessing.

#### Note: ```These commits are manual, just for the ease-of-access of users.```
#### commit: ```Changes in descriptions```

#### Note ```This Package is under development and is open source.```

This package is developed by Syed Syab and Hamza Rustam for the purpose of Final Year Project at University of Swat.
our information is given below


About Project:

    DataFit is a python package developed for automating data preprocessing.
    
    Project initilization data: 01/OCT/2023
    
    Project Finilization Data: 01/Dec/2023 (Expected)
    

Team Member:

    ```Professor Naeem Ullah: **Supervisor**```
    
    Basic Information:
    
        [https://facebook.com/Naeem-Munna?mibextid=PzaGJu]
        
        [naeem@uswat.edu.pk]
        
    ================================
    
    ```Syed Syab: **Student** (Me) ```
    
    Basic information:
    
        [https://github.com/SyabAhmad]
        
        [lhttps://inkedin.com/SyedSyab]
        
        [syab.se@hotmail.com]
        
    ```Hamza Rustam: **Student**```
    
    Basic Information:
    
        [https://github.com/Hamza-Rustam]
        
        [linkedin.com/hamza-rustam-845a2b209]
        
        [hs4647213@gmail.com]
    
    

This Package is desinged in a user-friendly manner which means every one can use it.

The main functionality of the package is to just automate the data pre-processing step, and make it easy for machine learning engineers or data scientist.

Current Functionality of the package is:
```
    Function:
        displaying information
        Handling Null Value
        Delete Multiple Columns
        Handling Categorical Values
        Normalization
        Standardization
        Extract Numeric Values
        Tokenization
```

### To use the package
```commandline
pip install datafit
```
To use this package it's quit simple, just import it like pandas and then use it.
```python
from datafit import datafit as df
# to check information of the data
df.information(data)
```

To categorize the data
```python
from datafit import datafit as df

df.handleCategoricalValues(data,["column1","column2"])
```
if you want to not mention the columns name an do it for all columns then simply type **None** inplace of columns names.
```python
from datafit import datafit as df

df.handleCategoricalValues(data,None)
```

To Extract numerical values from the columns

```python
from datafit import datafit as df

df.extractValues(data,["columns1", "columns2"])
```


**Note Again:** This package is uder development. 
if it touches your heart do share it and follow me on **github** [https://github.com/SyabAhmad] and **linkedin** [lhttps://inkedin.com/SyedSyab] for mote intersting updates


"""


setup(
    name='datafit',
    version='0.2023.2.11',
    description='This is a Python package that automates the data preprocessing',
    long_description=longDescription,
    long_description_content_type='text/markdown',  # Specify the type of content as Markdown
    author='Naeem Ullah, Syed Syab, Hamza Rustam',
    #secondauthor = 'Hamza Rustam',
    #supervisor = 'Naeem Ullah',
    #author_email='syab.se@hotmail.com',
    #secondauthor_email = 'hs4647213@gmail.com',
    #supervisor_email = 'naeem@uswat.edu.pk',
    url='https://github.com/SyabAhmad/datafit',
    license='MIT',

    packages=find_packages(),
    install_requires=[
        'numpy>=1.0',
        'pandas>=1.0',
        'scikit-learn',

    ],

    # Entry points for command-line scripts if applicable
    entry_points={
        'console_scripts': [
            'my_script = __init__.py',
        ],
    },

    # Other optional metadata
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        # Add more classifiers as appropriate
    ],
)