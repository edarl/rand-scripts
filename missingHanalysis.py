#!/usr/bin/python

# Purpose:    SCRIPT TO ANALYSE ATOM DIFFERENCE BETWEEN TWO PDB FILES
# Author:     Emma Darling
# Date:       08 AUG 2020

import sys
import pandas as pd

def parse_args():
    file1, file2, out = sys.argv[1:]
    return file1, file2, out

def save_df(df, file_out):   
    print("Saving dataframe to | ", file_out)
    df.to_csv(file_out, index=False)


def split_line(line):
    # Split the line based on pdb description(s)
    # split_line = [line[:6], line[6:11], line[12:16], line[17:20], line[21], line[22:26], line[30:38], line[38:46], line[46:54]]

    pdb_info ={
    'FIELDNAME' : line[:6],
    #'FIELDNUM'  : line[6:11],
    'ATOM'      : line[12:16],
    'ALTLOC'    : line[16],
    'RES_NAME'  : line[17:20],
    'CHAIN'     : line[21],
    'RESSEQ'    : line[22:26],
    'X' : line[30:38],
    'Y' : line[38:46],
    'Z' : line[46:54]
    }
    return pdb_info


def parse_pdb(file):
    # PDB parser, pdbs is a list of dicts
    
    with open(file, 'r') as f:
        c=1
        pdbs = []

        lines = f.readlines()
        for line in lines:
            if line[0:3] == 'END':
                break
            if line[0:3] == 'TER':
                #print("Skipping TER")
                continue

            pdb = {'ID' : c}
            pdb.update(split_line(line))
            #print(pdb)

            pdbs.append(pdb)
            c+=1

    return pdbs


def find_df_diff(df1, df2):
    # Takes as input two dataframes expectig cols of:
    #[ 'ID', 'FIELDNAME', 'ATOM', 'ALTLOC', 'RES_NAME', 'CHAIN', 'RESSEQ', '
    # X', 'Y', 'Z']
    # function compares the dfs based on the ATOM CHAIN RESSEQ fields

    # from https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences

    diff = pd.concat([df1,df2]).drop_duplicates(keep=False)

    return diff


def find_diff(df1, df2):
    # Atom difference
    c = ['FIELDNAME', 'ATOM', 'ALTLOC', 'RES_NAME', 'CHAIN', 'RESSEQ', 'X', 'Y', 'Z']
    diff = find_df_diff(df1[c], df2[c])

    return diff


def compare_pdbs(file1, file2):

    # parse files
    pdb1 = parse_pdb(file1)
    pdb2 = parse_pdb(file2)

    df1 = pd.DataFrame(pdb1)
    df2 = pd.DataFrame(pdb2)

    print("Atoms in file1:", df1.shape[0])
    print("Atoms in file2:", df2.shape[0])

    d = find_diff(df1, df2)
    
    return d

#d = compare_pdbs(file1, file2)
#save_df(d, 'diff.csv')
def test():
    file1="transfer/missing4/1EWQ_RING.pdb"
    file2="transfer/missing4/1EWQ_RING_resave.pdb"

def main():
    # parse input args
    file1, file2, out = parse_args()


    d = compare_pdbs(file1, file2)
    save_df(d, out)
    

if __name__ == "__main__":
    main()