from sanic import Sanic, response
from sanic.log import logger

from camera import Camera

app = Sanic(__name__)

@app.middleware("response")
async def allow_origin(request, response):
  response.headers["Access-Control-Allow-Origin"] = "*"
  response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-Origin, Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Authorization"

@app.route('/')
async def index(request):
    return response.html('''hello''')

@app.route('/camera-stream/')
async def camera_stream(request):
    camera = Camera(320, 240, 10)
    # camera = Camera()
    return response.stream(camera.stream, content_type = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/steer', methods = ['POST'])
async def steer(request):
  logger.info(request.json)
  return response.json({'ok': True})

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 8000)
