from setuptools import setup, find_packages
#packages lo que hace es ayuda a buscar subpaquete que estan creado en el proyecto
setup(name="PypiPackagexample",
      version="0.0.1",
      license = 'MIT',
      description="paquete de prueba para una clase de Udemy",
      author="Shushant Mohan Kumari",
      install_requires=['math','numpy'],
      packages=find_packages(),
      url='https://github.com/Shushant94/pypipackageexample.git'
    )         
    
    


