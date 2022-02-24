import os,time,re,datetime,sys
def main():
    while(1):
        text_file = str(sys.argv[1])
        with open(text_file, 'rb') as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-3, os.SEEK_END) #-2
                while f.read(1) != b'\n':
                    f.seek(-3, os.SEEK_CUR) #-2
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            try:
                sys_time_ubertooth = last_line.split("=")[1].split(" ")[0]
                check = time.time()
                #print(int(check))
                if (int(check) - int(sys_time_ubertooth)) > 60:
                    print(int(sys_time_ubertooth))
                    print(check)
                    print("Ubertooth Died... Restart!!!")
                    return
                    
                else:
                    continue
                print(sys_time_ubertooth)
            except:
                continue


if __name__ == '__main__':
    main()
    