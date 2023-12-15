'''
    Tools to read data from ANES election survey results.

    There are two types of files: 
    1) a single timeseries file that contains demographics etc over time
    2) a file for each survey year that contains open ends (the format differs by year)

    Although the format of the open-ends file differs by year, it always contains the 
    open-ends in some structured format, as well as a "Case ID" key that indicates 
    which participant the row maps to. 

    For the timeseries data, a utility function is provided to read the data as a
    Pandas DataFrame.

    For each year of open-ended data, a utility function is provided to read
    the specific format from that year and map column labels onto standard
    labels for each open-ended question. This function also converts the "Case ID"
    (or similar) column into a key that can be mapped to the timeseries data.

    Finally, a utility function is provided to add the open-ended data from specified
    years/files to the overall timeseries file.
'''

import pandas as pd
import os

def read_all_data(
    data_dir="downloaded_data",
    timeseries_filename="anes_timeseries_cdf_csv_20220916.csv",
    open_ends_2020_filename="2020.xlsx",
    open_ends_2016_filename="2016.xlsx",
    overall_2016_filename="anes_timeseries_2016_rawdata.txt",
    open_ends_2012_filename="2012.xlsx",
    open_ends_2008_filename="2008.xls",
   ):  
    """
    Read and combine all necessary from a given directory. This reads the timeseries data file,
    reads the open-ended data file for each year, and combines them before returning a DataFrame.
    
    There are a large number of filename input parameters to this function - the defaults have
    all been set to the download names from download_data.py, so they do not need to be overriden
    unless using different filenames.

    Parameters
    ----------
    output_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    timeseries_filename : str (optional, default="anes_timeseries_cdf_csv_20220916.csv")
      An optional filename to read timeseries data from

    open_ends_2020_filename : str (optional, default="2020.xlsx")
      An optional filename to read 2020 open-ended data from

    open_ends_2016_filename : str (optional, default="2016.xlsx")
      An optional filename to read 2016 open-ended data from

    overall_2016_filename : str (optional, default="anes_timeseries_2016_rawdata.txt")
        An optional filename to read 2016 overall data, in order to create a
        mapping to the keys used in the open-ended data

    open_ends_2012_filename : str (optional, default="2012.xlsx")
      An optional filename to read 2012 open-ended data from

    open_ends_2008_filename : str (optional, default="2008.xls")
      An optional filename to read 2008 open-ended data from

 
    Returns
    -------
    pandas.DataFrame
      A combined DataFrame of all timeseries data, with open-ended data appended in columns
      (wherever present). This DataFrame is indexed by a unique identifier that combines
      year and case ID (a participant identifier). This DataFrame has each column from the original
      timeseries dataset, as well as the following open-ended columns: 
      'Like About Democratic Candidate', 
      'Dislike About Democratic Candidate', 
      'Like About Republican Candidate', 
      'Dislike About Republican Candidate', 
      'Like About Democratic Party', 
      'Dislike About Democratic Party', 
      'Like About Republican Party', 
      'Dislike About Republican Party'


    Examples
    --------
    >>> ts_df = read_all_data()
    """

    # Reads the overall timeseries file
    ts = read_timeseries_data(data_dir=data_dir, filename=timeseries_filename)

    # Reads each of the open_ends files by year
    open_ends_by_year = []
    open_ends_by_year.append(read_2020_open_ends(data_dir=data_dir, filename=open_ends_2020_filename))
    open_ends_by_year.append(read_2016_open_ends(data_dir=data_dir, filename=open_ends_2016_filename, overall_2016_filename=overall_2016_filename))
    open_ends_by_year.append(read_2012_open_ends(data_dir=data_dir, filename=open_ends_2012_filename))
    open_ends_by_year.append(read_2008_open_ends(data_dir=data_dir, filename=open_ends_2008_filename))


    # Concats the open-ended data from each year together
    open_ends = pd.concat(open_ends_by_year)        

    # Joins the time series and open-ended data
    ts = ts.join(open_ends)

    return ts

def read_timeseries_data(data_dir="downloaded_data", filename="anes_timeseries_cdf_csv_20220916.csv"):
    """
    Reads the timeseries data file from the given data_dir. This loads the CSV as a 
    Pandas DataFrame, and creates an index from year and case ID (participant ID).

    Parameters
    ----------
    data_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filename : str (optional, default="anes_timeseries_cdf_csv_20220916.csv")
      The CSV file to read data from
    
    Returns
    -------
    pandas.DataFrame
      A DataFrame containing the timeseries data, with an index created by combining
      year and Case ID.

    Examples
    --------
    >>> ts = read_timeseries_data()
    """
    
    input_filename = os.path.join(data_dir, filename)
    df = pd.read_csv(input_filename, low_memory=False)

    # VCF0004 is year
    # VCF0006 is case ID (participant ID)
    # To create the index, we will combine the two columns VCF0004	VCF0006
    df["index"] = df["VCF0004"].astype(str) + df["VCF0006"].apply(lambda x: "%0.4d" % x)
    df = df.set_index("index")
    
    return df

def read_2020_open_ends(data_dir="downloaded_data", filename="2020.xlsx"):
    """
    Reads the 2020 open-ended data file. In this file, each open-ended response
    is stored in a different tab. This function calls the read_open_ends_by_tab
    function with the correct set of tabs for 2020 data.

    Parameters
    ----------
    data_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filename : str (optional, default="2020.xlsx")
      The Excel file to read data from
    
    Returns
    -------
    pandas.DataFrame
      A DataFrame containing the open-ended data, with an index created by combining
      year and Case ID.

    Examples
    --------
    >>> df = read_2020_open_ends()
    """    

    # Reads the entire Excel file as a dictionary of DFs, keyed by tab name
    input_filename = os.path.join(data_dir, filename) 
    df_by_tab = pd.read_excel(input_filename, engine="openpyxl", sheet_name=None)
    cleaned_df_by_tab = {}

    # We are interested in extracting data for the following tabs in tabs_and_labels
    tabs_and_labels = [
        ("V201107", "Like About Democratic Candidate"),
        ("V201109", "Dislike About Democratic Candidate"),
        ("V201111", "Like About Republican Candidate"),
        ("V201113", "Dislike About Republican Candidate"),
        ("V201159", "Like About Democratic Party"),
        ("V201161", "Dislike About Democratic Party"),
        ("V201163", "Like About Republican Party"),
        ("V201165", "Dislike About Republican Party"),
    ]
    
    # For each tab of interest, extract the open-ended responses
    for tab, label in tabs_and_labels:
        df = df_by_tab[tab]

        # Prepends "2020" to the case ID (respondent identifier) and sets it to be the index
        # Modifies the index_column, which is assumed to be the first column
        assert len(df.columns) == 2
        index_column = df.columns[0]
        df[index_column] = "2020" + df[index_column].astype(str)
        df = df.set_index(index_column)

        # Rename the other (remaining) column to be the label
        assert len(df.columns) == 1, df.columns
        previous_column_label = df.columns[0]
        df = df.rename(columns={previous_column_label: label})

        cleaned_df_by_tab[label] = df

    # Combine the cleaned_df from each tab
    combined_open_ends = pd.concat(cleaned_df_by_tab.values(), axis=1)
    
    return combined_open_ends

def read_2016_open_ends(data_dir="downloaded_data", filename="2016.xlsx", overall_2016_filename="anes_timeseries_2016_rawdata.txt"):
    """
    Reads the 2016 open-ended data file. In this file, each open-ended response
    is stored in a different tab. This function calls the read_open_ends_by_tab
    function with the correct set of tabs for 2016 data. Because the 2016 open-ended
    data is keyed by a different key (V160001_orig, the original ID) rather than
    the usual year + case ID key, we also remap the index from V160001_orig to V160001.
    In order to do this, we read V160001_orig and V160001 from the original (non-open-ended)
    2016 data file.

    Parameters
    ----------
    data_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filename : str (optional, default="2016.xlsx")
      The Excel file to read data from
    
    Returns
    -------
    pandas.DataFrame
      A DataFrame containing the open-ended data, with an index created by combining
      year and Case ID.

    Examples
    --------
    >>> df = read_2016_open_ends()
    """
    

    # Reads the entire Excel file as a dictionary of DFs, keyed by tab name
    input_filename = os.path.join(data_dir, filename) 
    df_by_tab = pd.read_excel(input_filename, engine="openpyxl", sheet_name=None)
    cleaned_df_by_tab = {}

    # We are interested in extracting data for the following tabs in tabs_and_labels
    tabs_and_labels = [
        ("V161069", "Like About Democratic Candidate"),
        ("V161072", "Dislike About Democratic Candidate"),
        ("V161075", "Like About Republican Candidate"),
        ("V161078", "Dislike About Republican Candidate"),
        ("V161098", "Like About Democratic Party"),
        ("V161101", "Dislike About Democratic Party"),
        ("V161104", "Like About Republican Party"),
        ("V161106", "Dislike About Republican Party"),
    ]
    
    # For each tab of interest, extract the open-ended responses
    for tab, label in tabs_and_labels:
        df = df_by_tab[tab]

        # Sets the first column to be the index        
        assert len(df.columns) == 2
        index_column = df.columns[0]
        df[index_column] = df[index_column].astype(str)
        df = df.set_index(index_column)

        # Rename the other (remaining) column to be the label
        assert len(df.columns) == 1, df.columns
        previous_column_label = df.columns[0]
        df = df.rename(columns={previous_column_label: label})

        cleaned_df_by_tab[label] = df

    # Combine the cleaned_df from each tab
    combined_open_ends = pd.concat(cleaned_df_by_tab.values(), axis=1)
    
    # For 2016 data, everything is indexed by column V160001, but we need to remap to
    # V160001_orig from the original dataset
    # For convenience sake this mapping is hardcoded in here, because it should not be 
    # necessary to download this additional 2016 original dataset file just to parse 
    # the open-ended responses. However, here is sample code to construct it if need be:
    
    import csv
    full_input_filename = os.path.join(data_dir, overall_2016_filename)   
    with open(full_input_filename) as inputfile:
        reader = csv.reader(inputfile, delimiter="|")
        header = next(reader)
        new_id = header.index("V160001")
        original_id = header.index("V160001_orig")
        mapping = {}
        for row in reader:
            assert len(row) == len(header)
            mapping[row[original_id]] = "2016%0.4d" % int(row[new_id].strip())        

    # Maps from the current DF index to this new index
    combined_open_ends.index = [mapping.get(str(x), str(x)) for x in combined_open_ends.index]

    return combined_open_ends


def read_2012_open_ends(data_dir="downloaded_data", filename="2012.xlsx"):
    """
    Reads the 2012 open-ended data file. In this file, each open-ended response
    is stored in a different column in a single tab.

    Parameters
    ----------
    data_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filename : str (optional, default="2012.xlsx")
      The Excel file to read data from
    
    Returns
    -------
    pandas.DataFrame
      A DataFrame containing the open-ended data, with an index created by combining
      year and Case ID.

    Examples
    --------
    >>> df = read_2012_open_ends()
    """
    
    # Reads the Pre2012 tab of the Excel file
    input_filename = os.path.join(data_dir, filename)    
    df = pd.read_excel(input_filename, sheet_name="Pre2012")

    # Creates an index column by joining the year and case ID (always the first column)
    index_column = df.columns[0]
    df[index_column] = "2012" + df[index_column].apply(lambda x: "%0.4d" % int(x) if type(x) == int else x)
    df = df.set_index(index_column)

    # Selects only the relevant columns    
    columns_and_labels = [
        ("candlik_likewhatdpc", "Like About Democratic Candidate"),
        ("candlik_dislwhatdpc", "Dislike About Democratic Candidate"),
        ("candlik_likewhatrpc", "Like About Republican Candidate"),
        ("candlik_dislwhatrpc", "Dislike About Republican Candidate"),
        ("ptylik_lwhatdp", "Like About Democratic Party"),
        ("ptylik_dwhatdp", "Dislike About Democratic Party"),
        ("ptylik_lwhatrp", "Like About Republican Party"),
        ("ptylik_dwhatrp", "Dislike About Republican Party"),
    ]
    df = df[[column for column, label in columns_and_labels]]

    # Remaps columns to the relevant labels
    df = df.rename(columns={column: label for column, label in columns_and_labels})

    return df
    
    
def read_2008_open_ends(data_dir="downloaded_data", filename="2008.xls"):    
    """
    Reads the 2008 open-ended data file. In this file, each open-ended response
    is stored in a different column in a single tab. 

    Parameters
    ----------
    data_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filename : str (optional, default="2008.xlsx")
      The Excel file to read data from
    
    Returns
    -------
    pandas.DataFrame
      A DataFrame containing the open-ended data, with an index created by combining
      year and Case ID.

    Examples
    --------
    >>> df = read_2008_open_ends()
    """    
        
    # Reads the AllOpen tab of the Excel file
    input_filename = os.path.join(data_dir, filename)    
    df = pd.read_excel(input_filename, sheet_name="AllOpen")

    # Creates an index column by joining the year and case ID (always the first column)
    index_column = df.columns[0]
    df[index_column] = "2008" + df[index_column].apply(lambda x: "%0.4d" % int(x) if type(x) == int else x)
    df = df.set_index(index_column)

    # Selects only the relevant columns  
    columns_and_labels=[
        ("A8b.  DemPC_like", "Like About Democratic Candidate"),
        ("A8d.  DemPC_dislike", "Dislike About Democratic Candidate"),
        ("A9b.  RepPC_like", "Like About Republican Candidate"),
        ("A9d.  RepPC_dislike", "Dislike About Republican Candidate"),
        ("C1b.  DemParty_like", "Like About Democratic Party"),
        ("C1d.  DemParty_dislike", "Dislike About Democratic Party"),
        ("C2b.  RepParty_like", "Like About Republican Party"),
        ("C2d.  RepParty_dislike", "Dislike About Republican Party"),
    ]
    df = df[[column for column, label in columns_and_labels]]

    # Remaps columns to the relevant labels
    df = df.rename(columns={column: label for column, label in columns_and_labels})

    return df
