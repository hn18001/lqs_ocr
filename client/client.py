import sys
import os
import time

sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from lqs_ocr import result_server
from lqs_ocr.ttypes import *

from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def main():
    addr = "112.74.23.141"
    #addr = "10.169.95.133"
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

            ocr_results = []
            for image in images:
                print image.img_name
                rlt = ocr_result(img_name= image.img_name, result = "hello world")
                ocr_results.append(rlt)

            result_client.write_ocr_result(ocr_results)

            transport.close()
            print("ocr's time:%f" %(time.time()-start))
        except Exception:
        #except thrift.TTransportException, tx:
            print("Failed to connect to %s:%d", addr, port)

        time.sleep(2)

if __name__ == "__main__":
    main()
