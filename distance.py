import serial
import time




ser = serial.Serial("/dev/ttyAMA0", 115200, bytesize=8, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
#print(ser)
#ser = serial.Serial("/dev/ttyAMA0", 115200)
def getTFminiData():
    bytes_read = 0
    data = None
    while True:
        #time.sleep(0.1)
        count = max(1, ser.in_waiting)
        
        if count < 8:
            print(count)
            if data is None:
                data = ser.read(count)
                
            else:
                data.append(ser.read(count))
            bytes_read += count

        else:
            recv = ser.read(9 - bytes_read)
            bytes_read = 0
            try:
                recv = data + recv
            except Exception as e:
                print(e)
                recv = recv
            
            data = None
            ser.reset_input_buffer()

            if recv[0] == 0x59 and recv[1] == 0x59:  # python3
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                #print('(', distance, ',', strength, ')')
                ser.reset_input_buffer()
                return distance


if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        getTFminiData()
    except KeyboardInterrupt:  # Ctrl+C
        if ser != None:
            ser.close()
            
