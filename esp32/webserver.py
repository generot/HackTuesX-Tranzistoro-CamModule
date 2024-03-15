import gc
import machine
import camera
import display
import json

from microWebSrv import MicroWebSrv

class webcam():
    def __init__(self, config):
        self.framesize = camera.FRAME_SVGA
        self.config = config
        self.config_dict = json.load(self.config)

        self.routeHandlers = [
            ("/getFrame", "GET", self._httpSendFrame),
            ("/assignId", "GET", self._httpAssignID)
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
                
                #return False

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
    
    def _httpAssignID(self, httpClient, httpResponse):
        query_params = httpClient.GetRequestQueryParams()
        
        print(self.config_dict)
        
        if "assigned_id" not in self.config_dict:
            self.config_dict["assigned_id"] = query_params["assigned_id"]
            self.config.seek(0)
            json.dump(self.config_dict, self.config)
            self.config.close()
        
        httpResponse.WriteResponse(code=200,
                                   headers=None,
                                   contentType="application/text",
                                   contentCharset="UTF-8",
                                   content=self.config_dict["assigned_id"])