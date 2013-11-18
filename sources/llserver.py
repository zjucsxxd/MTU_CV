import numpy as np
import socket
import struct

class LLServerClient:
  def __init__(self, host, port):
	self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.s.connect((host, port))

  def read(self):
    header = struct.unpack('<IHHBHHI', self.s.recv(8 + 9))
    bodySize = header[0] - (8 + 9)
    cv_im = np.fromstring(self.s.recv(bodySize, socket.MSG_WAITALL), dtype = np.uint8)
    cv_im = np.reshape(cv_im, (header[5], header[4]))
    return (0, cv_im)
