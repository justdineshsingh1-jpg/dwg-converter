
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
            subprocess.run(["/lib64/ld-linux-x86-64.so.2", "/usr/local/bin/dxf2dwg", dxf_path, "-y", "-o", dwg_path], check=True, capture_output=True, text=True)
            
            with open(dwg_path, "rb") as f:
                dwg_data = f.read()
                
            return Response(
                content=dwg_data, 
                media_type="application/acad", 
                headers={"Content-Disposition": "attachment; filename=Survey_Detailed_Poles.dwg"}
            )
        except subprocess.CalledProcessError as e:
            return Response(content=f"Subprocess Error: {e.stderr}\nStdout: {e.stdout}", status_code=500)
        except Exception as e:
            return Response(content=f"Conversion Error: {str(e)}", status_code=500)
@app.get('/test')
async def test_cmd():
    import subprocess
    try:
        result = subprocess.run(['dxf2dwg', '--version'], capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {'error': str(e)}
@app.get('/find')
async def find_cmd():
    import subprocess
    try:
        result = subprocess.run(['ls', '-l', '/usr/local/bin/dxf2dwg'], capture_output=True, text=True)
        return {'out': result.stdout, 'err': result.stderr}
    except Exception as e:
        return {'error': str(e)}
@app.get('/ldd')
async def ldd_cmd():
    import subprocess
    try:
        result = subprocess.run(['ldd', '/usr/local/bin/dxf2dwg'], capture_output=True, text=True)
        return {'out': result.stdout, 'err': result.stderr}
    except Exception as e:
        return {'error': str(e)}

@app.get('/test_ld')
async def test_ld():
    import subprocess
    try:
        result = subprocess.run(['/lib64/ld-linux-x86-64.so.2', '/usr/local/bin/dxf2dwg', '--version'], capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {'error': str(e)}
