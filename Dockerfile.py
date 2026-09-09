from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import os

app = FastAPI()

# Allow your Google Apps Script / Web frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_dxf(request: Request):
    # Receive the raw DXF text from the frontend
    dxf_content = await request.body()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dxf_path = os.path.join(tmpdir, "input.dxf")
        dwg_path = os.path.join(tmpdir, "output.dwg")
        
        with open(dxf_path, "wb") as f:
            f.write(dxf_content)
            
        try:
            # Execute LibreDWG's conversion tool
            subprocess.run(["dxf2dwg", dxf_path, "-y", "-o", dwg_path], check=True)
            
            with open(dwg_path, "rb") as f:
                dwg_data = f.read()
                
            return Response(
                content=dwg_data, 
                media_type="application/acad", 
                headers={"Content-Disposition": "attachment; filename=Survey_Detailed_Poles.dwg"}
            )
        except Exception as e:
            return Response(content=f"Conversion Error: {str(e)}", status_code=500)