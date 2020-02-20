#!/usr/bin/python3

import getopt, sys, os, shutil
from termcolor import cprint
import csv
import random
import itertools

def usage():

    print ('Create a list of aleatory numbers from csv files')
    print ('')
    print ('Usage:')
    print ('\t-i DIR|--input=FILE.csv  path to the file with the csv indicating how many numbers per line')
    print ('\t-o DIR|--output=DIR      path to the directory where to put the CSVs (default is same as FILE)')
    print ('\t-s NUM|--size=NUM        size of the random number generated (default 5 characters)')
    print ('\t-f|--force               overwrite destination directory if exists')
    print ('\t-v|--verbose             be verbose')
    sys.exit(' ')

def main():

    # input arguments
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hi:o:vfl:", ["help","input=","output=","verbose","force","size="])
    except getopt.GetoptError as err:
        cprint (str(err), 'red')
        usage()
    verbose = False
    force = False
    size = 5
    table = {}
    output = None
    try:
        for o, a in opts:
            print(o)
            if o in ("-h", "--help"):
                usage()
            if o in ("-f", "--force"):
                force = True
            if o in ("-v", "--verbose"):
                verbose = True
            if o in ("-i", "--input"):
                with open(a, 'r') as file:
                    for row in csv.reader(file):
                        if row[1]:
                            table[row[0] or '_empty_'] = int(row[1])
                if not output:
                    output = os.path.splitext(os.path.basename(a))[0]
            if o in ("-o", "--output"):
                output = a
            if o in ("-s", "--size"):
                size = int(a)

        if not table:
            cprint('[ERROR] Input file must be a CSV with a name an a number', 'red')
            usage()

        if os.path.isdir(output):
            if force:
                cprint('[WARNING] Folder [%s] already exists, it will be removed'%output, 'yellow')
                shutil.rmtree(output)
            else:
                cprint('[ERROR] Folder [%s] already exists, please remove it or use -f'%output, 'red')
        os.mkdir(output)
        total = 0
        for num in table.values():
            total += num
        numbers = random.sample(range(10**size, 2*10**size), total)
        print('Generated %d random numbers'%len(numbers))

        mode = '{:0' + str(size) + 'd}'
        pos = 0
        for key,num in table.items():
            if verbose:
                print("Found [{0}] with [{1}]".format(key,num))
            with open(output + '/' + key + '.csv', "w") as file:
                w = csv.DictWriter(file, ['CODE'])
                if verbose:
                    print("Iterating from {0} to {1}".format(pos, pos + num))
                for code in itertools.islice(numbers, pos, pos + num):
                    w.writerow({'CODE': mode.format(code)})
            pos += num

        print('You may want to create pdfs with this command:')
        print('for i in %s/*; do soffice --convert-to pdf "$i" --headless; done'%output)

    except Exception as err:
        cprint(str(err), 'red')
        usage()


#-------------------------------
if __name__ == "__main__":
    main()

