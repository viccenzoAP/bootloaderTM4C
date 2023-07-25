import serial
import time
import binascii
import os
import math
import sys

conectado = serial
file_path = False
port = True

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'data/ota.bin')

def flash_full(file_path_param):
    if not file_path_param:
        print("Choose a compatible file")
    else:
        apagar_mem()
        time.sleep(0.05)
        while conectado.in_waiting:
            data_in = conectado.read(4)
            if data_in == b"\x01\xaa\x01\xa5":
                print("ack sucess!")
            if data_in == b"\x01\xa1\x01\xa5":
                print("Erase sucess!")
            if data_in == b"\x01\xa1\xf0\xa5":
                print("Erase failed!")
            print(data_in)
        flashing_request(file_path_param)
        time.sleep(0.05)
        while conectado.in_waiting:
            data_in = conectado.read(4)
            if data_in == b"\x01\xaa\x02\xa5":
                print("ack sucess!")
            if data_in == b"\x01\xa2\x01\xa5":
                print("Flashing request accepted!")
            if data_in == b"\x01\xa2\x00\xa5":
                print("Flashing request refused!")
            print(data_in)
        flash_data(file_path_param)
        time.sleep(0.05)
        while conectado.in_waiting:
            data_in = conectado.read(4)
            if data_in == b"\x01\xaa\x03\xa5":
                print("ack sucess!")
            if data_in == b"\x01\xa3\x01\xa5":
                print("Writing flash memory succeeded, send next chunk of data")
            if data_in == b"\x01\xa3\x00\xa5":
                print("Flashing refused!")
            if data_in == b"\x01\xa3\x02\xa5":
                print("Writing flash memory succeeded, application is now completely transferred")
            print(data_in)
        flash_end(file_path_param)
        time.sleep(0.05)
        while conectado.in_waiting:
            data_in = conectado.read(4)
            if data_in == b"\x01\xaa\x04\xa5":
                print("ack sucess!")
            if data_in == b"\x01\xa4\x01\xa5":
                print("Flash end accepted!")
            if data_in == b"\x01\xa4\x00\xa5":
                print("Flash end refused!")
            print(data_in)
        reset()


def reset():
    buffer = bytearray([0, 5, 0xA5])
    conectado.write(buffer)


def crc32_from_file(file_path_param):
    if not file_path_param:
        print("Choose a compatible file")
    else:
        f = open(file_path_param, 'rb').read()
        f = (binascii.crc32(f) & 0xFFFFFFFF)
        return "%08X" % f


def flash_end(file_path_param):
    if not file_path_param:
        print("Choose a compatible file")
    else:
        crc32 = int(crc32_from_file(file_path_param), 16)
        crc32_byte = crc32.to_bytes(4, byteorder='big')
        crc32_array = bytearray(crc32_byte)
        buffer = bytearray([4, 4])
        for i in range(len(crc32_array)):
            buffer.append(crc32_array[i])
        buffer.append(0xA5)
        conectado.write(buffer)


def flash_data(file_path_param):
    if not file_path_param:
        print("Choose a compatible file")
    else:
        f = open(file_path_param, 'rb')
        nbytes_div252 = math.floor(os.path.getsize(file_path_param) / 252)
        for i in range(nbytes_div252):
            buffer = bytearray([252, 3])
            data_array = bytearray(f.read(252))
            for d in range(len(data_array)):
                buffer.append(data_array[d])
            buffer.append(0xA5)
            conectado.write(buffer)
            print(buffer)
            time.sleep(0.05)
            while conectado.in_waiting:
                data_in_flash = conectado.read(4)
                if data_in_flash == b"\x01\xaa\x03\xa5":
                    print("ack sucess!")
                if data_in_flash == b"\x01\xa3\x01\xa5":
                    print("Writing flash memory succeeded, send next chunk of data")
                if data_in_flash == b"\x01\xa3\x00\xa5":
                    print("Flashing refused!")
                if data_in_flash == b"\x01\xa3\x02\xa5":
                    print("Writing flash memory succeeded, application is now completely transferred")
                print(data_in_flash)
        last_data_lenth = os.path.getsize(file_path_param) - nbytes_div252*252
        last_byte_array = bytearray(f.read(last_data_lenth))
        buffer = bytearray([last_data_lenth, 3])
        for i in range(len(last_byte_array)):
            buffer.append(last_byte_array[i])
        buffer.append(0xA5)
        conectado.write(buffer)
        time.sleep(0.05)
        while conectado.in_waiting:
            data_in_flash = conectado.read(4)
            if data_in_flash == b"\x01\xaa\x03\xa5":
                print("ack sucess!")
            if data_in_flash == b"\x01\xa3\x01\xa5":
                print("Writing flash memory succeeded, send next chunk of data")
            if data_in_flash == b"\x01\xa3\x00\xa5":
                print("Flashing refused!")
            if data_in_flash == b"\x01\xa3\x02\xa5":
                print("Writing flash memory succeeded, application is now completely transferred")
            print(data_in_flash)

def flashing_request(file_path_param):
    if not file_path_param:
        print("Choose a compatible file")
    else:
        payload_size = os.path.getsize(file_path_param)
        payload_size_bytes = payload_size.to_bytes(4, byteorder='big')
        payload_size_array = bytearray(payload_size_bytes)
        buffer = bytearray([4, 2])
        for i in range(len(payload_size_array)):
            buffer.append(payload_size_array[i])
        buffer.append(0xA5)
        conectado.write(buffer)


def apagar_mem():
    buffer = bytearray([0, 1, 0xA5])
    conectado.write(buffer)


def open_file(file_path_param):
    f = open(file_path_param, 'rb')
    hexadata = binascii.hexlify(f.read(1))
    while hexadata:
        hexadata = binascii.hexlify(f.read(1))
    f.close()


try:
    conectado = serial.Serial('/dev/ttyUSB0', 19200, timeout=0.5)
    print("Conectado com a porta", conectado.portstr)
except serial.SerialException:
    print("Porta USB não detecda!")
    port = False
    pass

while True:
    print("A - Delete memory")
    print("B - Select binary file")
    print("C - Flashing request")
    print("D - Flash")
    print("E - Flash end")
    print("F - Rest")
    print("G - FLASH FULL")
    print("H - Exit")
    comando = input("Input Action:")
    if comando == "A":
        if port:
            apagar_mem()
            time.sleep(0.05)
            while conectado.in_waiting:
                data_in = conectado.read(4)
                if data_in == b"\x01\xaa\x01\xa5":
                    print("ack sucess!")
                if data_in == b"\x01\xa1\x01\xa5":
                    print("Erase sucess!")
                if data_in == b"\x01\xa1\xf0\xa5":
                    print("Erase failed!")
                print(data_in)
        else:
            print("No serial connection")
    elif comando == "B":
        file_path = filename
    elif comando == "C":
        if port:
            flashing_request(file_path)
            time.sleep(0.05)
            while conectado.in_waiting:
                data_in = conectado.read(4)
                if data_in == b"\x01\xaa\x02\xa5":
                    print("ack sucess!")
                if data_in == b"\x01\xa2\x01\xa5":
                    print("Flashing request accepted!")
                if data_in == b"\x01\xa2\x00\xa5":
                    print("Flashing request refused!")
                print(data_in)
        else:
            print("No serial connection")
    elif comando == "D":
        if port:
            flash_data(file_path)
            time.sleep(0.05)
            while conectado.in_waiting:
                data_in = conectado.read(4)
                if data_in == b"\x01\xaa\x03\xa5":
                    print("ack sucess!")
                if data_in == b"\x01\xa3\x01\xa5":
                    print("Writing flash memory succeeded, send next chunk of data")
                if data_in == b"\x01\xa3\x00\xa5":
                    print("Flashing refused!")
                if data_in == b"\x01\xa3\x02\xa5":
                    print("Writing flash memory succeeded, application is now completely transferred")
                print(data_in)
        else:
            print("No serial connection")
    elif comando == "E":
        if port:
            flash_end(file_path)
            time.sleep(0.05)
            while conectado.in_waiting:
                data_in = conectado.read(4)
                if data_in == b"\x01\xaa\x04\xa5":
                    print("ack sucess!")
                if data_in == b"\x01\xa4\x01\xa5":
                    print("Flash end accepted!")
                if data_in == b"\x01\xa4\x00\xa5":
                    print("Flash end refused!")
                print(data_in)
        else:
            print("No serial connection")
    elif comando == "F":
        reset()
    elif comando == "G":
        flash_full(file_path)
    elif comando == "H":
        break
    else:
        print("Action not available")
if port:
    conectado.close()
    print("Conexão fechada")