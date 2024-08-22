import json #handles json data
import time #sleep functions and time tracking
import os #interaction with file system
#constants
poll_interval = 0.1 #time interval between checks 
frequency_threshold = 0.2 #maximum allowed time between messages
plausible_data_range = range(0, 256) #plausable data range

def analyse_messages(reception_log, anomaly_log): #analyses frequency and plausability messages
    last_message_time = None #stores last message time
    file_position = 0 #tracks position of the file
    
    while True: # loop for continous operation
        if os.path.exists(reception_log): #check reception log exists
            with open(reception_log, "r") as infile, open (anomaly_log, "a") as outfile: # open reception to read and anomaly to append
                infile.seek(file_position) # move pointer to last read
                lines = infile.readlines() #read all lines from the file since last checked

                if lines: #if there are new messages recieved
                    for line in lines: #process each newley read line
                        line = line.strip() #remove and surrounding space
                        if line: #if line isnt empty
                            message = json.loads(line) #parse 
                            current_time = time.time() #record time

                            if last_message_time is not None: #if not the first message
                                time_diff = current_time - last_message_time #calculate the differennce in time
                                if time_diff < frequency_threshold: #difference flag
                                    anomaly = { #log
                                        "Type:":" Frequency Anomaly",
                                        "message:": message,
                                        "Time:": current_time
                                    }
                                    outfile.write(json.dumps(anomaly) + "\n") #write to log
                                    print(f"Intrusion attempt detected: {anomaly}") #write to console
  
                            if any(byte not in plausible_data_range for byte in message["DATA:"]): #check for any data byte discrepencies
                                anomaly = { #log
                                    "Type:": "Plausability Anomaly",
                                    "message:": message,
                                    "timestamp:":current_time
                                }
                                outfile.write(json.dumps(anomaly) + "\n") #write to log
                                print(f"Intrusion Attempt detected: {anomaly}") #write to console

                            last_message_time = current_time # update last message time
                file_position = infile.tell() #update file position
        time.sleep(poll_interval) #time interval

if __name__ == "__main__":
    reception_log = "rec.log" #rec log
    anomaly_log = "anomaly_log" #anomaly log
    print(f"Starting CANGaurd, logging to: {anomaly_log}...") #boot message
    analyse_messages(reception_log, anomaly_log) #start
 

