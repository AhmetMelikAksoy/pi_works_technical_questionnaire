import pandas as pd

def read_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Read and preprocess data from a file.
    
    Args:
        file_path (str): Path to the input file.

    Returns:
        pd.DataFrame: Processed data in a pandas DataFrame.
    """
    #read input file with tab delimeter
    data = pd.read_csv(file_path, delimiter="\t")

    #convert PLAY_TS to datetime
    data["PLAY_TS_DATETIME"] = pd.to_datetime(data['PLAY_TS'], format="%d/%m/%Y %H:%M:%S", errors='coerce')

    #extract the date component and fill missing values where there are only date component rows
    data["PLAY_TS_DATE"] = data["PLAY_TS_DATETIME"].dt.date
    fill_na_values = pd.to_datetime(data[data['PLAY_TS_DATETIME'].isna()]["PLAY_TS"], format="%d/%m/%Y")
    data['PLAY_TS_DATE'].fillna(fill_na_values, inplace=True)

    return data

def number_of_distinct_songs_by_user(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the number of distinct songs played by each user on distinct dates.

    Args:
        data (pd.DataFrame): Input DataFrame containing play data.

    Returns:
        pd.DataFrame: A DataFrame with counts of distinct songs per user on distinct dates."""
    
    user_song_count = data.groupby(['CLIENT_ID', 'PLAY_TS_DATE'])['SONG_ID'].nunique().reset_index()
    return user_song_count

if __name__ == "__main__":
    file_path = "exhibitA-input.csv"
    data = read_and_preprocess_data(file_path)
    
    user_song_count = number_of_distinct_songs_by_user(data)

    #report the number of users who played 346 distinct songs
    num_users_with_346_songs = user_song_count[user_song_count["SONG_ID"] == 346].shape[0]
    print(f"Number of users who played 346 distinct songs: {num_users_with_346_songs}")

    #report the maximum number of distinct songs played by a user
    max_distinct_songs = user_song_count["SONG_ID"].max()
    print(f"Maximum number of distinct songs played by a user: {max_distinct_songs}")