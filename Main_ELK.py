import time,re,datetime,sys,argparse,os,csv
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error

def follow(live_log, input_or_live):

    if "input" in input_or_live:
        #live_log.seek(0,0)
        while True:
            line = live_log.readline()
            if not line:
                break
            yield line

    else:
        live_log.seek(0,2)
        while True:
                line = live_log.readline()
                if not line:
                        time.sleep(0.1)
                        continue
                yield line

if __name__ == '__main__':
    
    try:
        with connect(host="localhost",user="Zeus97",password="Capstone22!",database="elk_model") as connection:
            print(connection)
        connection = mysql.connector.connect(host="localhost",user="Zeus97",password="Capstone22!",database="elk_model")
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
           

    parser = argparse.ArgumentParser()
    parser.add_argument("input_or_live", type=str,
                    help=" -> input or live")
    parser.add_argument("file", type=str,
                        help=" -> file path")
    parser.add_argument("outputfile", type=str,
                        help=" -> output file path")
    args = parser.parse_args()

    input_or_live=args.input_or_live
    file=args.file
    output=args.outputfile

    if any(item in input_or_live for item in ['input', 'live']):
        print("Starting {} parser...".format(input_or_live))
    else:
        print("Need to either specify input or live...")
        exit()

    # Check if file exist, if not, create it.
    if not os.path.exists(file):
        open(file, 'w').close()

    print("Reading file: {}...".format(file))
    print("\n")
    #new = open("update.txt", "w")

    logfile = open(file,"r")
    loglines = follow(logfile, input_or_live)
    line_num = 0

    #d="*"
    #print("packet_number"+d+"date"+d+"freq"+d+"addr"+d+"delta_t"+d+"rssi"+d+"channel"+d+"pdu_type"+d+"AdvA"+d+"data_flags"+d+"InitA"+d+"ScanA"+d+"Manufacturer"+d+"TxPowerlvl"+d+"local_name"+d+"local_name_ml"+d+"AdvA_ml"+d+"InitA_ml"+d+"ScanA_ml")

    fout = open(output, "w")
    print(output)
    #anomaly = open("anomaly_"+output, "w")
    d="*"
    header = ("packet_number"+d+"date"+d+"freq"+d+"addr"+d+"delta_t"+d+"rssi"+d+"channel"+d+"pdu_type"+d+"AdvA"+d+"data_flags"+d+"InitA"+d+"ScanA"+d+"Manufacturer"+d+"TxPowerlvl"+d+"local_name"+d+"local_name_ml"+d+"AdvA_ml"+d+"InitA_ml"+d+"ScanA_ml")
    fout.write("{}\n".format(header))
    LOCAL_NAME =''
    RSSI = 0
    for line in loglines:
        line_num += 1
        sl = line.strip()
        sl_len = len(sl)
        

        BLE_CONNECTION = False
        BLE_COMMAND = False 
        

        DEBUG = 0 #0 = off, 1 = on, prints all variables with \n

        if DEBUG:
            print("Line Number - {}".format(line_num))

        # Setting blank values to all variables that will be used
        date = freq = addr = delta_t = rssi = channel = '' # First part
        pdu_type = AdvA = data_flags = InitA = ScanA = command_Length=command_CID=command_OPCODE=command_Handle=command_data = '' # PDU part
        Manufacturer = TxPowerlvl = local_name = '' # Last part
        local_name_ml = AdvA_ml = InitA_ml = ScanA_ml = '' # 2nd to last

        # Making sure packet has Mac-Address
        p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)
        found = re.findall(p, line)
        '''
        if not found:
            continue
        '''
        ########################
        ### Error handling start

        sl = sl.replace('*', '') #Using * as delimiter, getting rid of any false positivies.
        
        if "CRC:" not in sl: # Making sure packet has is completed with CRC ending..
            continue
        
        if "Early return due to" in sl: # Another error string
            continue

        if not sl.startswith('systime='): #If line doesn't start with systime=, move to the next.
            continue

        if "Error:" in sl: #Remove all malformed packets, 'Error: attempt to read past end of buffer...'
            continue

        if "UNKNOWN Data:" in sl: #Remove all malformed packets
            continue
        '''
        if (sl_len < 220): #Half written packets, no good anyways. grep -x '.\{1,200\}' -n
            continue
        '''
        ### Error handling end
        ######################

        '''
        #Dropping all data packets for now.
        matches = ["LL_FEATURE_REQ", "L2CAP", "LL Control PDU"]
        if any([substring in sl for substring in matches]):
            continue
        '''
        if 1 != 1:
            continue
        else:
            try:
                date = re.findall('systime=(.*?) freq=', sl)
                date = int(date[0])
                date = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S")
                if DEBUG:
                    print(date)
            except:
                data=''
            
            try:
                freq = re.findall('freq=(.*?) addr=',sl)
                freq = int(freq[0])
                if DEBUG:
                    print(freq)
            except:
                freq=''
            
            try:
                addr = re.findall('addr=(.*?) delta_t=',sl) #The AccessAddress property defines the 32-bit unique connection address between two devices. The default value is '8E89BED6'.
                addr = str(addr[0])
                if DEBUG:
                    print(addr)
            except:
                addr=''

            try:
                delta_t = re.findall('delta_t=(.*?) ms rssi=',sl)
                delta_t = str(delta_t[0])
                if DEBUG:
                    print(delta_t)
            except:
                delta_t=''
            
            try:
                rssi = re.findall('rssi=(.*?)\s',sl)
                rssi = str(rssi[0])
                rssi = rssi.split(" ")[:1][0]
                
                if DEBUG:
                    print(rssi)
            except:
                rssi=''
            
            try:
                channel = re.findall('Channel Index: (.*) Type:',sl)
                channel = str(channel[0])
                if DEBUG:
                    print(channel)
            except:
                channel=''
            

            # Checking for PDU types
            # http://j2abro.blogspot.com/2014/06/understanding-bluetooth-advertising.html
            # https://www.novelbits.io/bluetooth-low-energy-sniffer-tutorial-advertisements/

            if "LL Data PDU" in sl and "CRC:" in sl : #PDU Packets btwn master and slave
                #print("LL DATA")
                try:
                    #print(sl)
                    #LLID_type = re.findall('LLID: (.*?) 1' ,sl)
                    #print(LLID_type + " HERE \n")
                    #LLID_type = int(str(pdu_type[0]))
                    if "LLID: 1" in sl:
                        pdu_type = "Empty_PDU" # also known as acknowledges packet, if the peripheral device has « 0x1 » ( our case ) as value, he will reply to every connection event packet sent from the Central device at every connection interval. The type LLID 0x1 may signify whether it is an empty PDU or it is a continuation fragment of L2CAP packets.
                    elif "LLID: 2" in sl:
                        pdu_type = "Data_PDU" # the L2CAP plays the role of support of a higher level protocol multiplexing over the same physical link. With L2CAP we can assign to SMP ( Security Manager protocol ) and ATT ( Attribute protocol ) a fixed logical channel CID — 0x0006 for SMP and 0x0004 for ATT -.
                    elif "LLID: 3" in sl:
                        pdu_type = "LL_Control_PDU" #to control the link layer connection. The payload of the PDU consists of: 1. Opcode 2. Control data
                    if 1==1: #DEBUG:
                        x = 2
                    BLE_CONNECTION = True
                        #print(pdu_type)
                        

                except:
                    LLID_type=''

                if pdu_type == "Data_PDU":
                    try: 
                        BLE_COMMAND = True
                        split_sl=str((sl.split("Data: ", 1))[1])
                        split_crc = split_sl.split("CRC:",1)
                        command_data_list = str(split_crc[0]).strip(' ').split(" ")
                        command_Length = str(command_data_list[0]) + str( command_data_list[1])
                        command_CID = str(command_data_list[2]) + str( command_data_list[3])
                        command_OPCODE = str(command_data_list[4])
                        command_Handle = str(command_data_list[5]) + str( command_data_list[6]) 
                        #data_command = int(str(pdu_type[0]))
                        #print(command_data_list)
                        loop_num =len(command_data_list)
                        for i in range(0, (loop_num + 1)):
                            if loop_num < 10:
                                command_data += str(command_data_list[i])
                            else:
                                if i < 7:
                                    continue
                                else:
                                    command_data += str(command_data_list[i])
                            #print(command_data)
                        #print(sl)
                        #print(command_Length+command_CID+command_OPCODE+command_Handle+command_data)
                        #print(delta_t)
                    except: 
                        data_command="ERROR"



            if "ADV_IND" in sl: #Known as Advertising Indications (ADV_IND), where a peripheral device requests connection to any central device (i.e., not directed at a particular central device). Example:  A smart watch requesting connection to any central device.
                try:
                    pdu_type = re.findall('Type: (.*?) AdvA: ',sl)
                    
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''

                if "AdvData" in sl:
                    try:
                        AdvA = re.findall('AdvA: (.*?) AdvData: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

                else:
                    try:
                        AdvA = re.findall('AdvA: (.*?) Data: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

                if "Type 01 (Flags)" in sl: #Are included when an advertising packet is connectable. 
                # https://devzone.nordicsemi.com/f/nordic-q-a/29083/ble-advertising-data-flags-field-and-discovery
                    split_flags = sl.split("(Flags)")[1] #Getting second half after split for better coverage

                    if "Early return due" in split_flags: #Fixed error with Early warning.
                        try:
                            data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) Early',sl)
                            data_flags = str(data_flags[0])
                            if DEBUG:
                                print(data_flags)
                        except:
                            data_flags=''

                    if "Type 0a" in split_flags:
                        try:
                            data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) Type 0a',sl)
                            data_flags = str(data_flags[0])
                            if DEBUG:
                                print(data_flags)
                        except:
                            data_flags=''

                    if ("Type: " or "Reserved Data:") in split_flags:
                        try:
                            data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) (Type:|Reserved Data:)',sl)
                            data_flags = str(data_flags[0])
                            if DEBUG:
                                print(data_flags)
                        except:
                            data_flags=''

                    #elif "Data:" in split_flags:
                    #   data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) Data: ',sl)
                    #   data_flags = str(data_flags[0])
                    #   print(data_flags)

            if "ADV_DIRECT_IND" in sl: #Connectable directed advertising. Directed advertising is used when a device needs to quickly connect to another device. An initiating device immediately sends a connection request upon receiving this. This PDU has the following payload. Example: A smart watch requesting connection to a specific central device.
                try:
                    pdu_type = re.findall('Type: (.*?) AdvA: ',sl)
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''
                
                try:
                    AdvA = re.findall('AdvA: (.*?) InitA: ',sl)
                    AdvA = str(AdvA[0])
                    if DEBUG:
                        print(AdvA)
                except:
                    AdvA=''
                
                try:
                    InitA = re.findall('InitA: (.*?) Data: ',sl)
                    InitA = str(InitA[0])
                    if DEBUG:
                        print(InitA)
                except:
                    InitA=''
            
            # Just like ADV_IND, need to figure out main portion..
            if "ADV_NONCONN_IND" in sl: #Non connectable undirected advertising. Used by devices that want to broadcast and don't want to be connected to or scannable. This is the only option for a device that is only a transmitter. Example:  Beacons in museums defining proximity to specific exhibits.
                try:
                    pdu_type = re.findall('Type: (.*?) AdvA: ',sl)
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''

                if "AdvData" in sl:
                    try:
                        AdvA = re.findall('AdvA: (.*?) AdvData: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

                else:
                    try:
                        AdvA = re.findall('AdvA: (.*?) Data: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

            # Just like ADV_IND, need to figure out main portion..
            if "ADV_SCAN_IND" in sl: #Example:  A warehouse pallet beacon allowing a central device to request additional information about the pallet.

                try:
                    pdu_type = re.findall('Type: (.*?) AdvA: ',sl)
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''

                if "AdvData" in sl:
                    try:
                        AdvA = re.findall('AdvA: (.*?) AdvData: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

                else:
                    try:
                        AdvA = re.findall('AdvA: (.*?) Data: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

                if "Type 01 (Flags)" in sl: #Are included when an advertising packet is connectable. 
                # https://devzone.nordicsemi.com/f/nordic-q-a/29083/ble-advertising-data-flags-field-and-discovery

                    if "Early return due" in sl: #Fixed error with Early warning.
                        try:
                            data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) Early',sl)
                            data_flags = str(data_flags[0])
                            if DEBUG:
                                print(data_flags)
                        except:
                            data_flags=''
                    else:
                        try:
                            data_flags = re.findall('Flags\) \d\d\d\d\d\d\d\d (.*?) Type',sl)
                            data_flags = str(data_flags[0])
                            if DEBUG:
                                print(data_flags)
                        except:
                            data_flags=''

            # While not specifically an advertising PDU type, active scanning will involve the following additional
            if "SCAN_REQ" in sl: #Upon receiving and advertising packet and active scanner will issue this scan request packet
                try:
                    pdu_type = re.findall('Type: (.*?) ScanA: ',sl)
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''

                try:
                    AdvA = re.findall('AdvA: (.*?) Data: ',sl)
                    AdvA = str(AdvA[0])
                    if DEBUG:
                        print(AdvA)
                except:
                    AdvA=''

                try:
                    ScanA = re.findall('ScanA: (.*?) AdvA: ',sl)
                    ScanA = str(ScanA[0])
                    if DEBUG:
                        print(ScanA)
                except:
                    ScanA=''
                
            if "SCAN_RSP" in sl:  #Upon receiving a scan request (SCAN_REQ) packet and advertiser can respond with this.
                try:
                    pdu_type = re.findall('Type: (.*?) AdvA: ',sl)
                    pdu_type = str(pdu_type[0])
                    if DEBUG:
                        print(pdu_type)
                except:
                    pdu_type=''
            
                try:
                    AdvA = re.findall('AdvA: (.*?) ScanRspData: ',sl)
                    AdvA = str(AdvA[0])
                    if DEBUG:
                        print(AdvA)
                except:
                    AdvA=''

            if "CONNECT_REQ" in sl: 

                matches = ["Type:", "InitA:", "AdvA:", "AA:"]
                if any([substring in sl for substring in matches]):
                #The Central device, « the initiator », sends the packet Connect_Req to a device with the connectable and discoverable mode to establish a connection link. This packet contains all the required data needed for the future connection between the two devices.

                # Can still parse out many of the fields, if necessary.
                # http://rfmw.em.keysight.com/wireless/helpfiles/n7606/Content/Main/PDU_Payload_Setting_4.htm#CRC

                    try:
                        pdu_type = re.findall('Type: (.*?) InitA: ',sl)
                        pdu_type = str(pdu_type[0])
                        if DEBUG:
                            print(pdu_type)
                    except:
                        pdu_type=''
                
                    try:
                        InitA = re.findall('InitA: (.*?) AdvA: ',sl)
                        InitA = str(InitA[0])
                        if DEBUG:
                            print(InitA)
                    except:
                        InitA=''

                    try:
                        AdvA = re.findall('AdvA: (.*?) AA: ',sl)
                        AdvA = str(AdvA[0])
                        if DEBUG:
                            print(AdvA)
                    except:
                        AdvA=''

            ### Finished with PDU stuff
            ###########################

            if "Manufacturer Specific Data" in sl: #Are included when an advertising packet is connectable. 
            # https://devzone.nordicsemi.com/f/nordic-q-a/29083/ble-advertising-data-flags-field-and-discovery

                if "(Manufacturer Specific Data) Wrong length" in sl:
                    pass

                else:
                    try:
                        Manufacturer = re.findall('Company: (.*?) Data:',sl)
                        Manufacturer = str(Manufacturer[0])
                        if DEBUG:
                            print(Manufacturer)
                    except:
                        Manufacturer=''

            if "Tx Power Level" in sl: #Tx Power Level 

                if "dBm" not in sl:
                    pass

                else:
                    try:
                        TxPowerlvl = re.findall('Tx Power Level\) (.*?) dBm',sl)
                        TxPowerlvl = str(TxPowerlvl[0])
                        if DEBUG:
                            print(TxPowerlvl)
                    except:
                        TxPowerlvl=''


            if ("Complete Local Name") in sl: #Are included when an advertising packet is connectable.
                try:
                    local_name = re.findall('\(Complete Local Name\) (.*?) Data: ',sl)
                    local_name = str(local_name[0])
                    if DEBUG:
                        print(local_name)

                    pattern = '.*Type \S\S '
                    result = re.match(pattern, local_name)
                    if result:
                      local_name = (result[0].split("Type")[0]) 
                    LOCAL_NAME = local_name
                except:
                    local_name=''

            if "Type" in data_flags: # Cleaning up some more Type misplacements.
                try:
                    pattern = '.*Type \S\S '
                    result = re.match(pattern, data_flags)
                    if result:
                      data_flags = (result[0].split("Type")[0]) 
                except:
                    data_flags=''

        if BLE_CONNECTION:

            # Joining everything up in one CSV line before plotting..    
            first_part = date,freq,addr,delta_t,rssi,channel #every packet will have this
            pdu_part =   pdu_type, command_data
            d = "*" #delimiter
            #x =  str(line_num)+"*"+str(date)+"*"+str(freq)+"*"+addr.strip()+"*"+delta_t.strip()+"*"+rssi.strip()+"*"+pdu_type+"*"+str(command_data).strip()
            all = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(line_num,d,date,d,freq,d,addr.strip(),d,delta_t.strip(),d,rssi.strip(),d,pdu_type,d,command_Length,d,command_CID,d,command_OPCODE,d,command_Handle,d,command_data)
            #print(command_data.strip())
            #print(type(command_data))
            #print(command_data)
            #fout.write(x)
            if command_data == "": #Malformed Packet
                continue
            #anomaly_form = "{}{}{}{}{}{}{}{}{}".format(command_Length,d,command_CID,d,command_OPCODE,d,command_Handle,d,command_data)
            
            if float(delta_t.strip()) > 500:
                #print(delta_t.strip())
                print("Anomaly Detected: Delta T: " + delta_t.strip() +" ms")
                print("Logging Anomaly...\n")
                fout.write("{}\n".format(all))

            if BLE_COMMAND:
                
                #new.write('("'+command_Length+'", "'+command_CID+'", "'+command_OPCODE+'", "'+command_Handle+'", "'+command_data+'"),')
                #print('("'+command_Length+'", "'+command_CID+'", "'+command_OPCODE+'", "'+command_Handle+'", "'+command_data+'"),\n')
                opcode_anomaly = False
                command_data_anomly = False
                valid_command = False
                #anomaly.write("{}\n".format(anomaly_form))
                select_movies_query = "SELECT * FROM model_BLE_connection"
                opcode_list =[]
                command_data_list = []
                with connection.cursor() as cursor:
                    cursor.execute(select_movies_query)
                    for row in cursor.fetchall():
                        if row[1] == command_Length and row[2] == command_CID and row[3] == command_OPCODE and row[4] == command_Handle and row[5] == command_data:
                            valid_command = True
                            break
                        else:
                            opcode_list.append(row[3])
                            command_data_list.append(row[5])
                if valid_command:
                    continue
                if command_OPCODE not in opcode_list:
                    opcode_anomaly = True
                    print("Anomaly Detected: unknown opcode: " + command_OPCODE)
                if command_data not in command_data_list:
                    command_data_anomly = True
                    print("Anomaly Detected: unknown command: " + command_data)
                if command_data_anomly or opcode_anomaly:
                    print("Logging Anomaly...\n")
                    fout.write("{}\n".format(all))
                else:
                    print("Anomaly Detected: unknown sequence: " + all)
                    print("Logging Anomaly...\n")
                    fout.write("{}\n".format(all))


                        #if opcode == row[3]:

                        #print(row)
            #check = time.time()
            #print(check)
            continue


        # Joining everything up in one CSV line before plotting..    
        first_part = date,freq,addr,delta_t,rssi,channel #every packet will have this
        pdu_part =   pdu_type,AdvA,data_flags,InitA,ScanA #Some packets will have either data_flags,InitA,ScanA
        last_part =  Manufacturer,TxPowerlvl,local_name,local_name_ml,AdvA_ml,InitA_ml,ScanA_ml

        d = "*" #delimiter
        all = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(line_num,d,date,d,freq,d,addr.strip(),d,delta_t.strip(),d,rssi.strip(),d,channel.strip(),d,pdu_type.strip(),d,AdvA.strip(),d,data_flags.strip(),d,InitA.strip(),d,ScanA.strip(),d,Manufacturer.strip(),d,TxPowerlvl.strip(),d,local_name.strip(),d,local_name_ml.strip(),d,AdvA_ml.strip(),d,InitA_ml.strip(),d,ScanA_ml.strip()) 
        #fout.write("{}\n".format(all))
        #print(local_name.strip()+"   "+local_name_ml.strip())
        try: 
            if float(delta_t.strip()) <100 and pdu_type == "ADV_IND": #Spoofing attack
                print("Anomaly Detected: Delta T, too fast: " + delta_t.strip() +" ms")
                print("Logging Anomaly...\n")
                fout.write("{}\n".format(all))
            elif pdu_type == "CONNECT_REQ":
                print("Connection Established. Device Name: " + LOCAL_NAME.strip())
                print(all)
                print("Logging this event...\n")
                fout.write("{}\n".format(all))
            elif RSSI == 0:
                RSSI = float(rssi.strip())
                continue 
            elif local_name.strip() != "ELK-BLEDOM":
                RSSI =0
                continue
            elif abs(float(rssi.strip()) - float(RSSI))  > 25 : #14
                print("Anomaly Detected: RSSI Changed Drastically, Device moved or Possible Spoofing attack")
                print(RSSI)
                print(rssi)
                print("Logging Anomaly...\n")
                print(all)
                fout.write("{}\n".format(all))
            
            #print("\n"+str(RSSI) )
            RSSI = float(rssi.strip())
            #print(float(rssi.strip()))
            
        except:
            continue
       
        '''
        try:
            if pdu_type == "SCAN_RSP":
                
                print(all)
              
        except:
            continue
        '''
        #check = time.time()
        #print(check)
        if DEBUG:
            print("\n")
if input_or_live == "input":
   print("Finished!")
   print("Output Written to: {}".format(output))

