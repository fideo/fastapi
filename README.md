# FASTAPI

## Pasos a seguir para levantar este proyecto de fastapi

1. Generar un entorno virtual. python -m venv venv
2. Ingresar al entorno virtual. source venv/bin/activate (depende del sistema operativo en el que se ejecute)
3. Ejecutar los componentes requeridos para la aplicación. pip install -r requirements.txt 
4. Luego intentamos levantar uvicorn (servidor web) que nos permitirá ver nuestra aplicación en un navegador web. uvicorn src.main:app --reload --port 8000
