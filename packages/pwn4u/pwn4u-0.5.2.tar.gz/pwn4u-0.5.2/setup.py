from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()# Todas las lineas de README.md se guardan en esta variable llamada long_description 

# Configuración del paquete
setup(
    name = "pwn4u",
    version = "0.5.2",
    packages = find_packages(),# Esto busca todos los paquetes (actualmente solo está el paquete hack4u) que se encuentren en el directorio actual y los añade a la lista de paquetes
    install_requires = [],# Lista de dependencias
    author = "Cristian Hernández",# Nombre del autor
    description = "Una biblioteca para consultar cursos de hack4u",# Descripción del paquete
    long_description = long_description,# Descripción larga del paquete 
    long_description_content_type = "text/markdown",# Tipo de contniido de la descripción larga es markdown. Es logico porque el archivo README.md es un archivo markdown
    url = "https://hack4u.io",# URL del paquete 
)

