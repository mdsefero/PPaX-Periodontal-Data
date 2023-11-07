def preamble():
    return ("""
This script matches by sample ID to an exclusion list to separate data from a datafile of interest

Usage: PPaX_Exclusion_finder.py -f [data file] -e [exclusion list]
Input files formatted to CSV UTF-8

Last Updated: 11 Feb 2022
Maxim Seferovic, seferovi@bcm.edu
""")

import argparse, os.path, collections
from datetime import datetime


def timestamp(action, object):
    print(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S') : <22}"
        f"{action : <18}"
        f"{object}"
        )


def save(outdata, extension):
    savename = file[0].rsplit('.', 1)[0] + extension + file[0].rsplit('.', 1)[-1]
    iteration = 0
    overwrite = '.'
    while True:
        if os.path.isfile(savename):
            savename = savename.rsplit('.', 1)[0] + f"{overwrite}" + file[0].rsplit('.', 1)[-1]
            iteration += 1
            overwrite = f"({iteration})."
        else:
            break
    with open(savename, mode='wt', encoding='utf-8') as f:  
        f.write('\n'.join(outdata))
    timestamp("Saved", savename)


def opene():
    timestamp ('Reading ', exclude[0])
    excluded = []
    with open (exclude[0], 'r') as f:
        for line in f:
            newline = ''.join(line.split())
            id = newline.split(',')[0]
            excluded.append(newline)
    return excluded


def openf():
    timestamp ('Reading ', file[0])
    global firstline   ### Unhash for headers. 
    csv = collections.defaultdict(list)
    with open (file[0], 'r') as f:
        firstline = f.readline().strip() ### Unhash for headers. 
        for line in f:
            newline = ''.join(line.split())
            id = newline.split(',')[0]
            id = id.replace('_', '') #### To match exclusion list - manually check format
            csv[id].append(newline)
    return csv


def match(DB, excluded): 
    count = 0 
    outdata = [firstline]
    listremoved =  [firstline]
    for i in excluded:
        data = DB.get(i)
        if data == None: 
            print (f"Could not find {i} in the data of interest") 
        else: 
            listremoved.append(DB[i][0])
            del DB[i] 
            count +=1 
    for k,v in DB.items():
        outdata.append(v[0])
    timestamp ('Removed ', count) 
    save(outdata, '_filtered.')
    save(listremoved, '_removed.')


def main ():        
    excluded = opene()
    metadata = openf()  
    match (metadata, excluded)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=print(preamble()))
    parser.add_argument('-f',  '--file', nargs = 1, required=True, type=str, dest='in_file')
    parser.add_argument('-e',  '--exclude', nargs = 1, required=True, type=str, dest='in_exclude')
    args = parser.parse_args()
    file = args.in_file
    exclude = args.in_exclude
    main()