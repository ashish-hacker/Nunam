"""
Processes data(excel files) in chunks and converts them to csv file
"""

from __future__ import barry_as_FLUFL

__version__ = '0.1'
__author__ = 'Ashish Kumar Panigrahy'


# Import necessary modules
import pandas as pd
class Preprocess:
    def __init__(self,):
        self.name_list = []
        self.dfs = []

    def get_sheet_names(self, 
                        like_name, file):
        """Return the list of sheet names in file starting with our specified pattern

        Parameters:
        like_name - The starting pattern to search (string)
        file - filename of the excel file (string)

        Return:
        returns the list of sheet names
        """

        f = pd.ExcelFile(file)  # the excel file buffer
        for i in f.sheet_names:
            if i[:len(like_name)] == like_name:  # if the sheet name starts with the pattern
                self.name_list.append(i)  
    
        return self.name_list
    
    def get_dataframe(self, 
                      inFile, sheet):
        """reads the data in chunks and stores in a dataframe which gets returned

        Parameters:
        inFile - The Filename, excel file (string)
        sheet - The array containing sheet names to read (List)

        Return:
        returns the dataframe after reading from excel file
        """

        if len(sheet) == 0: # If the sheet is an empty list return None
            return None
        
        chunks = []  
        nr = 10 ** 5 # chunk size
        sr = 1  # It is initialized to 1 to skip the header part
        df_header = pd.read_excel(inFile, sheet_name=sheet[0], nrows=1)
        while True:
            chunk_df = pd.read_excel(inFile,                  # Read file in chunks
                                    sheet_name=sheet,
                                    nrows=nr,
                                    skiprows=sr,
                                    header=None)
            sr += nr
            if not len(chunk_df):  # If the data is exhausted or read fully break out of the loop
                break
            chunks.append(chunk_df)
            chunk_df = pd.concat(chunk_df)
            # Rename the columns to concatenate the chunks with the header.
            columns = {i: col for i, col in enumerate(df_header.columns.tolist())}
            chunk_df.rename(columns=columns, inplace=True)
            df = pd.concat([df_header, chunk_df])
        return df

    def create_dfs(self,
                   filenames, sheet_name_like):
        """Creates a list of dataframes , created from different excel files
        
        Parameters:
        filenames - List of filenames from which data will be extracted (List)
        sheet_name_like - The pattern to be searched for in the starting of sheet names (List)

        Returns:
        returns the list of dataframes
        """
        
        for i in filenames:
            name = self.get_sheet_name(sheet_name_like, i)
            df = self.get_dataframe(i, name)
            self.dfs.append(df)
        return self.dfs

    def create_csv(self, df_list, csv_filename):
        """Create csv file of by concatinating all dataframes
        Parameter:
        df_list - List of dataframes (List)
        csv_filename - The name of the csv file to be created (String)
        """
        
        # remove all None values from the list
        df_list = list(filter(lambda a: a != None, df_list))
        df = pd.concat(df_list)
        df.to_csv(csv_filename)
