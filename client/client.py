import sys
import os
import time

sys.path.append("./gen-py")
from lqs_ocr import ocr_server
from lqs_ocr.ttypes import *

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

    # Create a client to use the protocol encoder
    client = ocr_server.Client(protocol)

    # Connect!
    transport.open()

    while(1):
        start = time.time()
        # Call the interface to scene OCR.
        results = client.line_ocr()

        for result in results:
            print result.img_name

        print("ocr's time:%f" %(time.time()-start))

        time.sleep(2)

if __name__ == "__main__":
    main()
