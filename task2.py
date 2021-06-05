import pandas as pd

def downsample(df, 
                sampling_rate = 0.016666666666666666):
    """downsampling of given dataframe to 1 sample/minute."""

    
    i = 2 # skip the header and keep the first row, we skip from 2nd line
    skip = int(1/sampling_rate) # No. of rows to be skipped
    while(i < len(df)):
        df = df.drop(df.index[i:i+skip+1])
        i += 1
    return df

def create_downsampled_csv(filename):
    """Create downsampled csv file."""
    df = pd.read_csv(filename)
    df = downsample(df)
    new_filename = filename[:-4] + "Downsampled.csv"
    df.to_csv(new_filename, index = False)

def main():
    create_downsampled_csv("detail.csv")
    create_downsampled_csv("detailVol.csv")
    create_downsampled_csv("detailTemp.csv")


if __name__ == "__main__":
    main()