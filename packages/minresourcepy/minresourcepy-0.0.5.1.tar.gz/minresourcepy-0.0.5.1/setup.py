from setuptools import setup 
  
setup( 
    name='minresourcepy', 
    version='0.0.5.1',
    description='Tools for Resource Geologists', 
    url = 'https://github.com/renanlo/MinResourcepy',
    author='Renan Lopes', 
    author_email='renanglopes@gmail.com', 
    license='MIT License',
    install_requires=[ 
        'numpy>=1.24.3',
        'pandas>=2.0.3',
        'transforms3d>=0.4.1',
        'plotly>=5.9.0',
        'matplotlib>=3.7.2'],
) 