from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/info')
def get_info():
    return {'status': 'success'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')
