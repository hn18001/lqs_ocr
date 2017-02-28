import sys
import os
import time
sys.path.append('/usr/lib/python2.7/dist-packages/')


sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from lqs_ocr import result_server
from lqs_ocr.ttypes import *

from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

sys.path.append("./ocr")
import ocr

import util

def save_img(images):
    path = "../result/"

    img_list = []
    for image in images:
        full_path = os.path.join(path, os.path.basename(image.img_name))
        img_name = image.img_name     # The img_name in server machine
        result = {}
        result["full_path"] = full_path
        result["img_name"] = img_name
        img_list.append(result)

        print "full path:", full_path
        f = open(full_path, 'w')
        f.write(image.img)
        f.close()

        util.rotate_img(full_path)
        util.add_border(full_path)
    return img_list

def main():
    addr = "112.74.23.141"
    port = 6000
    print("Linking to: %s:%s" %(addr, port))
    transport = TSocket.TSocket(addr, port)

    # Buffering is critical, Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    ocr_protocol = TMultiplexedProtocol(protocol, "ocr_server")
    result_protocol = TMultiplexedProtocol(protocol, "result_server")

    # Create a client to use the protocol encoder
    ocr_client = ocr_server.Client(ocr_protocol)
    result_client = result_server.Client(result_protocol)

    while(1):
        start = time.time()
        try:
            transport.open()

            images = ocr_client.line_ocr()

            img_list = save_img(images)

            ocr_results = []
            img_list.sort()
            for img in img_list:
                ocr_rlt = ocr.ocr(img["full_path"])
		print ocr_rlt

                rlt = ocr_result(img_name = img["img_name"], result = ocr_rlt)
                ocr_results.append(rlt)

            if len(img_list) != 0:
                result_client.write_ocr_result(ocr_results)

            transport.close()
            print("ocr's time:%f" %(time.time()-start))
        except Exception:
        #except thrift.TTransportException, tx:
            print("Failed to connect to %s:%d" %(addr, port))

        time.sleep(1)

if __name__ == "__main__":
    main()
