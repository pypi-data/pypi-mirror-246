from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Tracescopio - um capturador simples de tracebacks'
LONG_DESCRIPTION = 'Tracescopio - Captura tracebacks de projetos Django. Use um middleware ou um decorator para otbter os traces e envia-los a um servidor'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="tracescopio", 
        version=VERSION,
        author="Tercio A Oliveira",
        author_email="t3rcio@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",            
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License (GPL)"
        ]
)