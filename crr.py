import time #time module  for sleep functionality 

def rec_messages(transmission_log, reception_log): # recieve CAN messages from trans log and store in receeption log
    with open(transmission_log, "r") as infile, open(reception_log, "a") as outfile: #open trans log to read and reception log to append
        infile.seek(0, 2) #keeps pointer to only read newest entry
        while True: #loop to keep receiever working
            line = infile.readline() #read next message from trans log
            if line: #if new message recieved
                outfile.write(line) #write to reception log
                print(f"ACK: {line.strip()}") #print to console
            time.sleep(0.1) # sleep duration

if __name__ == "__main__": 
    transmission_log = "sent.log" #trans log
    reception_log = "rec.log" #recieving log
    print(f"starting Reciever, logging to: {reception_log}") #boot message
    rec_messages(transmission_log, reception_log) #start
