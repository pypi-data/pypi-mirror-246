from setuptools import setup, find_packages

setup(
    name='Data533_superman_Jade',
    version='0.0.9',
    #packages=find_packages(),
    # packages=['Data533_superman_Jade', 'Data533_superman_Jade.customer', 'Data533_superman_Jade.administer'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'Data533_superman_Jade': ['Supermarket.db']},
    # py_modules=['Data533_superman_Jade.main']
    py_modules=['main']
)
