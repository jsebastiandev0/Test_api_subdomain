LIVE DEMO:

1. API:     https://test-api.jsebastian.dev/docs
2. APP:     https://test-app.jsebastian.dev/


to run api: 


// how to do freeze for depencies...
// pip3 freeze > requirements.txt  # Python3

1.      .venv\Scripts\Activate.ps1
2.      fastapi dev main.py

// así sí corre por algo de los directorios.
3.      uvicorn main:app --reload      
        
# Desde el directorio backend/
comando para construir la imagen del backend:
docker build -t fastapi-crud .
docker run -d --name fastapi-api -p 8000:8000 --env-file .env fastapi-crud

# windows...
tener corriendo el contenedor de mongo, con el puerto y las variables del .env bien definidas

*******************************************************
# para el frontend 

1.      instalar dependecias:           pnpm install
2.      correr:                         pnpm dev
