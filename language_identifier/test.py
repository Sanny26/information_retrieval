from identifier import *


def get_lang_label(profile, lprofiles):
    lang_label = -1
    min_dist = 99999

    for key, lprofile in lprofiles.items():
      dist = 0
      for i, val in enumerate(profile):
        if val in lprofile:
            dist+=abs(i-lprofile.index(val))
        else:
            dist+=len(lprofile)

        if dist < min_dist:
            min_dist = dist
            lang_label = key

    return lang_label

def test_DLI():

    accuracy = 0
    dr_path = "DLI32-2/"
    files = os.listdir(dr_path)

    for name in files:
        lan_id = int(name.split('.')[0])
        if lan_id%20 == 0:
           label = floor(lan_id/20) -1;
        else:
           label = floor(lan_id/20)

        profile = get_file_lprofile(dr_path+name)
        profile = [each[0] for each in profile.most_common(top_k_val)] 
        labelled = get_lang_label(profile, lprofiles)
        if label == labelled:
            accuracy += 1

    return float(accuracy)/len(files)
    

if __name__ =='__main__':

    lprofiles = pickle.load(open('lprofiles.txt', 'rb'))
    print( test_DLI() )    

    test_file = raw_input('Enter file path to be identified: ')

    profile = get_file_lprofile(test_file)
    profile = [each[0] for each in profile.most_common(top_k_val)]   

    lang_label = get_lang_label(profile, lprofiles)

    print( lang_label )

