import sys


VERSION = "0.1.00"
# Example
# 1a ff 4c 00 02 15 b8 fe d8 63 9f 1c 44 7c 8f 82 df 0c 2e 06 7d ea ab 44 fc e5 c5


def s8(value):
    return -(value & 0x80) | (value & 0x7f)



def help():
    print("")
    print("Bluetooth LE Beacon Parser")
    print("Version: " + VERSION)

    print("Copyright (c) 2023 Thyrasec LLC")
    print("https://www.thyrasec.com")
    print("")
    print("Usage")
    print("parse-le-beacon <hex bytes>")
    print("")
    print("Example")
    print("parse-le-beacon.py 1a ff 4c 00 02 15 b8 fe d8 63 9f 1c 44 7c 8f 82 df 0c 2e 06 7d ea ab 44 fc e5 c5")
    print("")


def main():
    
    argument_len = len(sys.argv) - 1

    if(argument_len < 20):
        help()
        exit(0)

    data = sys.argv[1:]


    if(int(data[0], 16) != argument_len - 1):
        print("Wrong length. Expected " + str(int(data[0], 16)) + " bytes but only " + str(argument_len - 1) + " provided")
        exit(0)

    #print("Length: " + str(int(data[0], 16)))

    if(int(data[1], 16) != 0xFF):
        print("Expected Manufacturer Specific Data 0xFF")
        exit(0)

    print("Type: Manufacturer Specific Data")

    if(int(data[2], 16) != 0x4C or int(data[3], 16) != 0x00):
        print("Expected Apple ")
        exit(0)

    print("Manufacturer: Apple Inc.")

    if(int(data[4], 16) != 0x02):
        print("Wrong Subtype - not iBeacon")

    print("Subtype: iBeacon")

    if(int(data[5], 16) != argument_len - 6):
        print("Wrong Length " + str(int(data[5], 16)) + "  " + str(argument_len - 6))
        exit(0)

    uuid = data[6:6 + 16]

    print("UUID: " + ' '.join(uuid))
    
    major = data[6 + 17]
    minor = data[6 + 18]
    power = data[6 + 19]

    print("Major: " + str(major))
    print("Minor: " + str(minor))
    print("TX Power: " + str(s8(int(power, 16))) + " dBm")
    

if __name__ == "__main__":
    main()
