

def decode(self, data="00200059120120005b8b0220005ce30320005b97"):  # = CH0: ~ 0.218 mV
    channel, zero, one, two, three = data[0:2], int(data[3:10], 16), int(data[13:20], 16), int(data[23:30], 16), int(data[33:40], 16)

    result = (2.5 * (float(zero+one+two+three) / 4) * 1000) / 2**28

    channeloffset = {"00": 0, "04": 1, "08": 2}
    return(channeloffset[channel], result)

print(decode(None, "042003d95e052003d7d4062003d82e072003d94e"))
print(decode(None))  # uses example data
