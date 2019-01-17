import cv2
import io
import socket
import struct
import time
import pickle
import zlib


if __name__ == "__main__":
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.43.211', 8485))
            connection = client_socket.makefile('wb')
            break
        except:
            continue

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += client_socket.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('client',frame)
        if(cv2.waitKey(1) != -1):
            client_socket.send("ok".encode())
            cv2.destroyAllWindows()
            client_socket.close()
            break 