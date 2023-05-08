from fastapi import APIRouter, UploadFile
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
            return FileResponse(getcwd()+"/encripted.des",media_type="application/octet-stream",filename="encripted.des")
        else:
            return JSONResponse(content={
            "status": False,
            "message": "Ha ocurrido un error durante la codificación"
        }, status_code=500)
    else:
        return JSONResponse(content={
            "status": False,
            "message": "El mensaje es inferior en longitud a la clave"
        }, status_code=500)

@router.post("/downloadMessage")
async def desencript_message(file: UploadFile):
    content = await file.read()
    str_message = str(content, 'utf-8')
    codification = Codification()
    
    if codification.desencript_message(str_message):
        return FileResponse(getcwd()+"/desencripted_message.txt",media_type="application/octet-stream",filename="desencripted_message.txt")
    else:
        return JSONResponse(content={
        "status": False,
        "message": "Ha ocurrido un error durante la decodificación"
    }, status_code=500)