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
        df = pd.read_excel(inFile, sheet_name=sheet[0])
        for i in range(1, len(sheet)):
            temp = pd.read_excel(inFile, sheet_name=sheet[i])
            df = pd.concat([df, temp])
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
            name = self.get_sheet_names(sheet_name_like, i)
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
        lists = []
        for i in df_list:
          if i is not None:
            lists.append(i)
        df = pd.concat(lists)
        df.to_csv(csv_filename)




def main():
    p = Preprocess()
    data_files = ["data.xlsx", "data_1.xlsx"]

    ### Task 1 : Create CSV files

    # Combine all the data in sheets named like "Detail_67_" only, among the two data files provided, and save into 'detail.csv'
    dfs = p.create_dfs(data_files, "Detail_67_")
    p.create_csv(dfs, "detail.csv")

    # Combine all the data in sheets named like "DetailVol_67_" only, among the two data files provided, and save into 'detailVol.csv'
    dfs1 = p.create_dfs(data_files, "DetailVol_67_")
    p.create_csv(dfs1, "detailVol.csv")

    # Combine all the data in sheets named like "DetailTemp_67_" only, among the two data files provided, and save into 'detailTemp.csv' Provide attention to the column 'Record Index' which provided index values to avoid mismatching the rows while combining multiple files.
    dfs2 = p.create_dfs(data_files, "DetailTemp_67_")
    p.create_csv(dfs2, "detailTemp.csv")


if __name__ == "__main__":
    import cProfile
    cProfile.run('main()')


