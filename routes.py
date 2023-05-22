from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

from os import getcwd
from codification import Codification

router = APIRouter()

@router.get("/")
def main():
    content = """
        <body style="font-size: 1.8rem">
        <div>
        <h2> FAST API</h2>
        <hr />
        La api esta funcionando correctamente
        </div>
        </body>
    """
    return HTMLResponse(content=content)

@router.post("/uploadData")
async def upload_data(key: str, file: UploadFile):

    content = await file.read()
    str_message = str(content, 'utf-8')
    if len(str_message) >= len(key):
        codification = Codification()
        
        if codification.encript_message(str_message,key):
            return FileResponse(getcwd()+"/encripted.des",media_type="text/plain",filename="encripted.des")
        else:
            raise HTTPException(status_code=500, detail="Ha ocurrido un error durante la codificación")
    else:
        raise HTTPException(status_code=501, detail="El tamaño de la clave es superior al mensaje enviado")

@router.post("/downloadMessage")
async def desencript_message(key: str, file: UploadFile):
    
    content = await file.read()
    str_message = str(content, 'utf-8')
    if len(str_message) >= len(key):
        codification = Codification()
        
        if codification.desencript_message(str_message,key):
            return FileResponse(getcwd()+"/desencripted_message.txt",media_type="text/plain",filename="desencripted_message.txt")
        else:
            raise HTTPException(status_code=500, detail="Ha ocurrido un error durante la decodificación")
    else:
        raise HTTPException(status_code=501, detail="El tamaño de la clave es superior al mensaje enviado")