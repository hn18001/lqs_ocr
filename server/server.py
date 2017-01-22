import os
import sys
import shutil
import get_line_complex_lection
import cv2

sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from lqs_ocr import result_server
from lqs_ocr.ttypes import *

from thrift.TMultiplexedProcessor import TMultiplexedProcessor
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
    def __init__(self):
        self.log = {}

    def line_ocr(self):
        img_path = "../need_to_process_images/"      # The images that are needed to ocr are saved in the dir.
        if not os.path.exists(img_path):
            print("The path [%s] is not exist!" %img_path)
            return []
    	flag = True
	if flag == True:
		#src_path = results[0].img_name[:results[0].img_name.rfind('/')]
		get_line_complex_lection.get_row_lection(img_path)
        ocr_imgs = []


        for root, dir_names, file_names in os.walk(img_path):
            if len(file_names) != 0:
                print("start ocr...\n")
            for file_name in file_names:
                full_path = os.path.join(root, file_name)
                f = open(full_path, 'r')
                img = f.read()
                rlt_img = ocr_img(img = img, img_name = full_path, b_location = False)
                ocr_imgs.append(rlt_img)
                f.close()
                
	return ocr_imgs

class Handler1:
    def __init__(self):
        self.log = {}

    def write_ocr_result(self, results):
        f = open("/home/dzj_user/result.txt", 'w')
	for result in results:
		img_file_name = result.img_name[result.img_name.rfind('/')+1:]
		print result.result

                f.write(result.result + "\n")

		new_file_txt = new_path + '/%s.txt' % img_file_name;
		new_img_path = new_path + '/%s' % img_file_name;
		with open(new_file_txt, 'wb') as nfp:
			line = '%s\n' % result.result;
			nfp.write(line);
		shutil.move(result.img_name, new_img_path)
		
        f.close()
        print("\nocr is finished...")
	return True

def main():
	#handler = Handler()
	#processor = ocr_server.Processor(handler)
	handler = Handler()
	handler1 = Handler1()

	ocr_processor = ocr_server.Processor(handler)
	result_processor = result_server.Processor(handler1)
	processor = TMultiplexedProcessor()
	processor.registerProcessor("ocr_server", ocr_processor)
	processor.registerProcessor("result_server", result_processor)

	addr = "112.74.23.141" 
	port = 6000
	print("Server IP: %s, port: %d" %(addr, port))

	transport = TSocket.TServerSocket(addr, port=port)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()

	server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

	print "Starting the ocr server."
	server.serve()

if __name__ == "__main__":
	new_path = '../processed_images'        # Save the ocr result and copy the images to this dir.
	if not os.path.exists(new_path):
		os.mkdir(new_path)
	
	main()
