import json #import json for parsing
import time # import time for timekeeping
import random # import random for random number functionality

SOF = 0 # start of frame ('0' for dominant bit)
EOF = [1, 1, 1, 1, 1, 1, 1] # end of frame
int = 0.1 # time interval between messages
anom_freq = 1/30 # probability of a frequency anomaly being injected
anom_plaus = 1/30 # probability of a plausability anomaly

def create_can_message():
    message_id = random.randint(1, 100) # generate a frame ID 
    data_field =[random.randint(0, 255) for _ in range (8)] #create a list of random bytes to act as data
    crc_check = random.randint(0, 255) # generate a cyclic redundancy check value
    ack_bit = random.choice([0, 1]) # acknowledgement bit
    freq = random.randint(0, 100) # transmission rate

    if random.random() < anom_plaus: # introduction of a plausability anomaly
       data_field[random.randint(0, 7)] = random.randint(256, 300) #sets random data byte to exceed plausible value
 
    message = { # CAN frame
            "SOF:": SOF,
            "ID": message_id,
            "DATA:": data_field,
            "CRC:": crc_check,
            "ACK:": ack_bit,
            "FREQ(Ms):": freq,
            "EOF:": EOF
    }
   
    return message # return generated CAN message

def transmit(log_file):  #transmission
    while True: #loop to for constant transmission
        message = create_can_message() # generate a new message

        with open(log_file, "a") as f: #open log file to append
            f.write(json.dumps(message) + "\n") # write the generated message to file as json string
        print(f"SYN: {message}") # print message to console

        if random.random() < anom_freq: # random sleep duration 
            anomaly_duration = random.uniform(0.3, 0.7) #delay
            time.sleep(anomaly_duration) # determined sleep duratiin
        else:
            time.sleep(int) #constant sleep outside of anomaly injection

if __name__ == "__main__":
     log_file = "sent.log" # log destination
     print(f"starting Transmission: logged to: {log_file}") #boot message
     transmit(log_file) #start
