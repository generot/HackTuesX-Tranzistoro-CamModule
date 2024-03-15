import gc
import machine
import camera
import display

from microWebSrv import MicroWebSrv

class webcam():
    def __init__(self):
        self.framesize = camera.FRAME_SVGA

        self.routeHandlers = [
            ("/getFrame", "GET", self._httpSendFrame)
        ]

    def run(self, disp):
        try:
            camera.init(0, format=camera.JPEG, framesize=self.framesize, fb_location=camera.PSRAM)
        except:
            camera.deinit()
            
            try:
                camera.init(0, format=camera.JPEG, framesize=self.framesize, fb_location=camera.PSRAM)
            except:
                print("Camera initialization failure!")
                
                display.flush()
                
                disp.fill(0)
                display.println(disp, "FAILURE:")
                display.println(disp, "")
                display.println(disp, "Camera could not")
                display.println(disp, "be initialized.")
                disp.show()
                
                return False

        mws = MicroWebSrv(routeHandlers=self.routeHandlers)
        mws.Start(threaded=True)
        
        print("Server is running...")
        
        display.flush()
        gc.collect()

    def _httpSendFrame(self, httpClient, httpResponse):
        image = camera.capture()

        httpResponse.WriteResponse(code=200, headers=None,
                                    contentType="image/jpeg",
                                    contentCharset="UTF-8",
                                    content=image)


