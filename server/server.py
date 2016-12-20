import os
import sys

sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from ocr_server.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

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
		return ocr_imgs

def main():
	handler = Handler()
	processor = ocr_server.Processor(handler)

	addr = get_local_ip("etho")
	port = 6000
	print("Server IP: %s, port: %d" %(addr, port))

	transport = TSocket.TserverSocket(addr, port=port)
	tfactory = TTransport.TBufferedTRansportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()

	server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

	print "Starting the ocr server."
	server.serve()

if __name__ == "__main__":
	main()
