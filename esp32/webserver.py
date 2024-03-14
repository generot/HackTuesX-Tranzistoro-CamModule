import gc
import machine
import camera

from microWebSrv import MicroWebSrv

class webcam():
    def __init__(self):
        self.saturation = 0
        self.quality = 10
        self.brightness = 0
        self.contrast = 0
        self.vflip = 0
        self.hflip = 0
        self.framesize = camera.FRAME_XGA

        self.routeHandlers = [
            ("/getFrame", "GET", self._httpSendFrame)
        ]

    def run(self):
        print("Server is running...")

        res = camera.init(0, format=camera.JPEG, framesize=self.framesize, fb_location=camera.PSRAM)
        
        if not res:
            camera.deinit()
            
            res = camera.init(0, format=camera.JPEG, framesize=self.framesize, fb_location=camera.PSRAM)
            
            if not res:
                #Display this error to the user somehow.
                print("Camera initialization failure!")
                
                return False

        mws = MicroWebSrv(routeHandlers=self.routeHandlers, webPath="www/")
        mws.Start(threaded=True)
        gc.collect()


    def _httpSendFrame(self, httpClient, httpResponse):
        image = camera.capture()

        httpResponse.WriteResponse(code=200, headers=None,
                                    contentType="image/jpeg",
                                    contentCharset="UTF-8",
                                    content=image)


