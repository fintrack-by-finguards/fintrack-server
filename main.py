
import os
from sanic import Sanic
from sanic.response import text
from sanic_cors import CORS, cross_origin

from app.apis import api

app = Sanic("FinTrack")
CORS(app)
app.blueprint(api)

@app.get("/")
async def hello_world(request):
    return text("Customed Link")

if __name__ == "__main__":
    app.run(host="0.0.0.0", 
    port=8000,
    debug=True,
    access_log=False,
    auto_reload=True,
    )
