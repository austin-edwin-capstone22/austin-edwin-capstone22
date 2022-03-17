# Capstone: Pattern-of-life Analysis and Deviations for Bluetooth and Bluetooth Low Energy Devices.</br>
This repository will hold our code, paper, demonstration, and additional information about our USNA Capstone. 
</br> 
# Here is the Demo Video:</br>

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/yTJTlL0mBgo/0.jpg)](https://www.youtube.com/watch?v=yTJTlL0mBgo) </br>


# Functionality:
## Ubertooth One:
We begin with **three Ubertooth One devices**. An Ubertooth One is an open source 2.4 GHz wireless development platform suitable for Bluetooth experimentation. The Ubertooth One devices are running on Firmware Version 2020-12-R1 (API:1.07) (Open Source). The Ubertooth One gives us the ability to intercept bluetooth and bluetooth low energy packets of any device that has bluetooth capabilities. Once the packets are intercepted, the open source Ubertooth Software turns the data into a PCAP file that can be read and examined through Wireshark.
## Machine Running The Code:
The three Ubertooth One devices are then connected via USB to a computer, running **Ubuntu 20.04.3 LTS**. It is on this machine that we host the code and database that runs the Ubertooth One devices. 
## Database:
We created a simple database utilizing MySQL. In our case, this database houses the pattern of life of an ELK Smart LED Light. We ran our program to output the specific attributes of what the ELK packets should contain when it is operating as intended. This required us to collect thousands of packets, issuing the device every possible command and then insert the data into our database.
## Main_ELK.py:
This is the largest program. The input to this program is a text file that can be in the form of live input or retroactively of an already created text file. As mentioned before, this program is tailored for the ELK Led Light, but it can easily be modified for any device. Essentially what this program does is it takes in all the data provided by packet from a BLE device, then it breaks it down into its specific components (The details of how it is broken into its specific components is within the code of our Github). After a packet is parsed into its specific components we can do one of two things with it.
1. First, we can do what we mentioned before, we can write to the database and update its pattern of life. 
2. Second, we can monitor a device and ensure it is operating as intended. A powered on BLE device is always in one of two states. 
- 1. One, it is in advertising mode, in which case, it is looking for a master device to connect to. In this case the pattern of life at this time is relatively simple. It sends out advertising packets rapidly on a consistent basis. Our program monitors the device based on two attributes provided by the packets. 
- - 1. One, we monitor how many advertising packets are being sent on a particular interval of time. We have this hard coded into our program, essentially if the device starts exceeding the amount of packets it sends, relative to its established pattern of life, in advertising mode we can postulate that another device is attempting to advertise as is and could be a potential sign that a man in the middle attack is being carried our, so we log this activity. 
- - 2. Second, we monitor its RSSI level. This gets updated every packet, so if the delta RSSI is too large, it is another clear indication that another device is advertising as the device we are monitoring. Thus a possible Man in the Middle attack is occuring, so we log this activity.
- 2. The other state a BLE device could be in is in an established connection with a master device. Our program logs everytime a master device connects to our slave device for attribution purposes. Once again here we monitor the amount of packets being sent between the master and the slave, along with the RSSI to ensure a man in the middle attack does not occur and log it if it deviates. At this point we also monitor the BLE commands being sent from the master device to slave device. Everytime a master device sends our device a command we cross reference it with our database that contains the pattern of life. If the command deviates from the pattern of life, we log this activity. </br>
#### Finally, this program outputs a log file in the form of a CSV file containing all of the significant events I mentioned before.
## script_ELK.py: 
Essentially what this program does is it combines our software, our code and our system devices together into one centralized program. So what it does is it restarts all the Ubertooth One devices, making sure we start from scratch and clear the cache. Then it creates a random output file name for all of the files, (three PCAPs, one text, and one CSV). This is just in case the Ubertooth One restarts, we don't want to overwrite any files and we want to start collecting data again quickly. Then we use the Ubertooth One’s software to start the collection, however we modified the software a little bit. We have each Ubertooth listen on one advertising channel (37, 38, or 39) and then it creates the PCAP file and then we use a SED command to output that PCAP file into the form of a text file. Now all three Ubertooth devices are going to output to the same text file, which our Main program will use as input.
## Our code is simple to run:
Simply type in 'python script_elk.py’. The terminal screen will be updated live so we can see what is occurring with our targeted device. We have it set such that it only gives us output when a master device connects to our targeted device and when an anomaly occurs. However, we can easily modify the code to give us output about any particular piece of data, if for example, this code is reused and is intended to monitor a specific attribute of a BLE device, we can do that as well. At the conclusion of our program we can open the CSV file it creates and see what packets popped as items of interest. Then we can utilize Wireshark and open the PCAP file to dive deeper into why a packet was logged into the CSV file.



