import os
import sys

sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from lqs_ocr.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def get_local_ip(ifname):
    import socket
    import fcntl
    import struct
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.gethostbyname(socket.gethostname())

    return ip

class Handler:
    def line_ocr():
        img_path = "../need_to_process_images/"
        ocr_imgs = []
        for root, dir_names, file_names in os.walk(img_path):
            for file_name in file_names:
                full_path = os.path.join(root, file_name)
                f = open(full_path, full_path)
                img = f.read()
                rlt_img = ocr_img(img = img, img_name = full_name, b_location = False) 
                ocr_imgs.append(rlt_img)
                f.close()
        return ocr_imgs

def main():
	handler = Handler()
	processor = ocr_server.Processor(handler)

	addr = get_local_ip("etho")
	port = 6000
	print("Server IP: %s, port: %d" %(addr, port))

	transport = TSocket.TServerSocket(addr, port=port)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()

	server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

	print "Starting the ocr server."
	server.serve()

if __name__ == "__main__":
	main()
