from asyncio import sleep

from cv2 import VideoCapture, imencode

class Camera():
  def __init__(self, width = 800, height = 480, fps = 60, source = 0):
    self.fps = fps
    self.camera = VideoCapture(source)
    self.camera.set(3, width)
    self.camera.set(4, height)

  def __del__(self):
    self.camera.release()

  def frame(self):
    success, frame = self.camera.read()
    ret, image = imencode('.jpg', frame)
    return image.tobytes()

  async def frames(self):
    while True:
      yield self.frame()
      await sleep(1 / self.fps)

  async def stream(self, rsp):
    async for frame in self.frames():
      rsp.write(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
