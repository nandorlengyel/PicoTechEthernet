import binascii

# print(''.join(reversed("2003d95e"))) LSB -> MSB ?
# print("e59d3002") ??
channelcalfactor = 1

sensor = b'\x04 \x03\xD9^\x05 \x03\xD7\xD4\x06 \x03\xD8.\x07 \x03\xD9N'
# 042003d95e
# 052003d7d4
# 062003d82e
# 072003d94e

if len(sensor) == 20:  # assume len of 20 is valid data
    sensor = binascii.hexlify(sensor).decode()  # 042003d95e052003d7d4062003d82e072003d94e
    print(sensor)
    channel, zero, one, two, three = sensor[0:2], sensor[2:10], sensor[12:20], sensor[22:30], sensor[32:40]

    print(channel)  # 04
    print(zero)  # 2003d95e
    print(one)  # 2003d7d4
    print(two)  # 2003d82e
    print(three)  # 2003d94e

    zero = int(zero, 16)  # 537123166
    one = int(one, 16)  # 537122772
    two = int(two, 16)  # 537122862
    three = int(three, 16)  # 537123150

    print()
    print(zero)
    print(one)
    print(two)
    print(three)

    result = ((channelcalfactor * (three - two)) / (one - zero)) / 1000000.0
    print(result)
