#!/usr/bin/python

#Austin Andres and Edwin Zerwekh
#Capstone
#This script combines our code and our devices, such that we only have to run one line from the command line to execute our program

import time,re,datetime,sys,argparse,os,csv
from random import randint


if __name__ == '__main__':
    checker = True
    print("System is restarting...")
    #Restarts the Ubertooth devices to clear memory 
    os.system("ubertooth-util -U0 -Sr")
    os.system("ubertooth-util -U1 -Sr")
    os.system("ubertooth-util -U2 -Sr")
    script_num = randint(0,10000) #Just generates a random number to tack on to our output file names
    text_num = str(script_num) #Text file all ubertooth devices will write to
    csv_num = str(script_num) #Log file
    #PCAP file names
    pcap0= str(script_num)
    pcap1 = str(script_num + 1)
    pcap2 = str(script_num + 2)
    '''
    Using the open source software that comes with the Ubertooth and combining it with our code.
    The command calls each Ubertooth (-U0, -U1, -U2) tells it to listen on a specific Adevertising Channel (37, 38, 39)
    Outputs to our named PCAP files (each Ubertooth gets its own PCAP)
    Finally, we use a sed command to parse the data of all of the PCAP files into a common text file.
    '''
    one = str("ubertooth-btle -U0 -A 37 -fI -r ELK-SCRIPT"+ pcap0 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    two =str("ubertooth-btle -U1 -A 38 -fI -r ELK-SCRIPT"+ pcap1 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    three = str("ubertooth-btle -U2 -A 39 -fI -r ELK-SCRIPT"+ pcap2 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    main_p = "python Main_ELK.py live ELK-SCRIPT"+text_num+".txt ELK-SCRIPT"+csv_num+"-out.csv" #See Main_ELK.py
    print("System is Starting...\n")
    #Printing out and ensuring the Ubertooth firmware is what we excpect
    os.system("ubertooth-util -U0 -v")
    os.system("ubertooth-util -U1 -v")
    os.system("ubertooth-util -U2 -v")
    #TARGETING
    #Replace this Bluetooth MAC Address with the targeted device address
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U0")
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U1")
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U2")
    #This line will let us know what the output files will be called
    print("Output Files: ELK-SCRIPT" + pcap0 +","+ pcap1 + ","+pcap2+"\n")
    print("Executing...\n")
    #Parsing the commands together to run the program. (Ctrl-C to end)
    os.system(one +" | " + two + " | " + three + " | " + main_p )
    

