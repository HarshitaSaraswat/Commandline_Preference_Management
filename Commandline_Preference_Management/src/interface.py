import FreeCAD


class CommandLineInterface:
    def __init__(self, *args):
        self.args = args

    def run(self):
        print("runnningg with args=", self.args)
    
    def test_run(self):
        print("77777777777777777777777777777777777777777777777777--------------------------------------------")
        x=FreeCAD.ParamGet("User parameter:BaseApp/Preferences/OpenGL")
        print(x)
        
        print(x.GetContents())

    def text_exception(self):
        raise Exception("jhfjhasvfmdvfdsav")
