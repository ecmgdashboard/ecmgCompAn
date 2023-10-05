import pandas as pd


def remove_duplicates(file_name):
    df = pd.read_csv(file_name)
    initial_shape = df.shape
    # the `subset=None` means that every column is used
    # to determine if two rows are different; to change that specify
    # the columns as an array
    # the duplicate rows are gone
    if file_name == "Individual Analyst Stock Pitches - Sheet1.csv":
        df.drop_duplicates(subset=None, inplace=True)
    elif file_name == "Comp An Analyst Pitch Holdings - Sheet1.csv":
        subset_cols = df.columns[2:]  # Disregard the first two columns
        df.drop_duplicates(subset=subset_cols, inplace=True)
    else:
        print("manipulating wrong files")

    final_shape = df.shape

    if initial_shape == final_shape:
        print("duplicate not found")
    else:
        print("duplicate found")
    # newer_file = file_name
    df.to_csv(file_name, index=False)


remove_duplicates("Individual Analyst Stock Pitches - Sheet1.csv")
print()
remove_duplicates("Comp An Analyst Pitch Holdings - Sheet1.csv")
print()
# remove_duplicates("newFile.csv")



