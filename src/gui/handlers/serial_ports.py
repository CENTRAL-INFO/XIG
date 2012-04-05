import json
import webob
import sys, glob
try:
    import serial.tools.list_ports
except:
    pass

class SerialPortsHandler:
    
    def __init__(self):
        self.com_ports = set()
    
    def poll(self):
        new_ports = self.get_ports()
        if new_ports != self.com_ports:
            # ports changed
            self.com_ports = new_ports
            l = list(new_ports)
            return l.sort()
        return None
    
    def get_ports(self):
        # return list of serial ports
        com_ports = set()
        try:
          for port, desc, port_type in serial.tools.list_ports.comports():
              com_ports.add(port)
        except:
          pass
        if len(com_ports):
            return com_ports
        try:
            if sys.platform.startswith("darwin"):
		    return set(glob.glob('/dev/tty.*') + glob.glob('/dev/cu.*'))
	    return set(glob.glob('/dev/tty*') + glob.glob('/dev/cu*'))
        except:
            pass
        return com_ports
    
    def __call__(self, request):
        if request.method == 'GET':
            self.com_ports = self.get_ports()
            com_ports = list(self.com_ports)
            com_ports.sort()
            return webob.Response(json.dumps(com_ports), content_type='json')
        else:
            return webob.exc.HTTPMethodNotAllowed()
