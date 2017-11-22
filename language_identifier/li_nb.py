from naive_bayes import *

if __name__ == "__main__":
    dr_path = "DLI32/"
    files = os.listdir(dr_path)

    for name in files:
        lan_id = int(name.split('.')[0])
        if lan_id%10 == 0:
           label = floor(lan_id/10) -1;
        else:
           label = floor(lan_id/10)

    