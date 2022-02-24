import time,re,datetime,sys,argparse,os,csv
from random import randint



if __name__ == '__main__':
    checker = True
    print("System is restarting...")
    os.system("ubertooth-util -U0 -Sr")
    os.system("ubertooth-util -U1 -Sr")
    os.system("ubertooth-util -U2 -Sr")
    script_num = randint(0,10000)
    text_num = str(script_num)
    csv_num = str(script_num)
    pcap0= str(script_num)
    pcap1 = str(script_num + 1)
    pcap2 = str(script_num + 2)
    one = str("ubertooth-btle -U0 -A 37 -fI -r ELK-SCRIPT"+ pcap0 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    two =str("ubertooth-btle -U1 -A 38 -fI -r ELK-SCRIPT"+ pcap1 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    three = str("ubertooth-btle -U2 -A 39 -fI -r ELK-SCRIPT"+ pcap2 +".pcapng | " + "sed -e 's|["+ '"'+"'\\'']||g' | xargs | sed -e" + " 's/systime/"+"\\n"+"systime/g' >> ELK-SCRIPT"+ text_num+ ".txt")
    main_p = "python Main_ELK.py live ELK-SCRIPT"+text_num+".txt ELK-SCRIPT"+csv_num+"-out.csv"
    #print(one)
    print("System is Starting...\n")
    os.system("ubertooth-util -U0 -v")
    os.system("ubertooth-util -U1 -v")
    os.system("ubertooth-util -U2 -v")
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U0")
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U1")
    os.system("ubertooth-btle -t ff:ff:cc:09:56:2c -U2")
    print("Output Files: ELK-SCRIPT" + pcap0 +","+ pcap1 + ","+pcap2+"\n")
    print("Executing...\n")
    os.system(one +" | " + two + " | " + three + " | " + main_p )
    
   
    #if output: 

    '''os.system(two)
    os.system(three)

    os.system("python Main-1.py live ELK-SCRIPT.txt ELK-SCRIPT-out.csv")'''

    
    #print(one)

