'''
    Tools to download all necessary data from ANES.

    This includes downloading/unzipping an overall timeseries file,
    as well as open-ended files by year.
'''

import urllib.request
import zipfile
import os

def download_all(
    filenames_and_urls = [
        ("timeseries.zip", "https://electionstudies.org/anes_timeseries_cdf_csv_20220916/"),
        ("2020.xlsx", "https://electionstudies.org/anes_timeseries_2020_redactedopenends_excel_20211118/"),
        ("2016.xlsx", "https://electionstudies.org/wp-content/uploads/2016/02/anes_timeseries_2016_redacted_openends.xlsx"),
        ("2016_full.zip", "https://electionstudies.org/anes_timeseries_2016/"),
        ("2012.xlsx", "https://electionstudies.org/anes_timeseries_2012_openends/"),
        ("2008.xls", "https://electionstudies.org/wp-content/uploads/2008/03/anes_timeseries_2008_openends_redacted_Dec2012Revision.xls"),
    ],
    output_dir="downloaded_data"
):
    """
    Downloads all necessary data to an output data directory. This uses urllib.request
    to download a list of specified links to their specified filenames. This function downloads the 
    overall timeseries file, as well as 1984-2020 open-ended files.
    
    Parameters
    ----------
    output_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)

    filenames_and_urls : list (optional)
      A list of (filename, url) tuples to download
    
    Returns
    -------
    None
      

    Examples
    --------
    >>> # This will download all files to the default downloaded_data directory
    >>> download_all()
    >>> # This will download all files to a download directory instead
    >>> download_all(output_dir="download")
    """

    # This is a list of URLs to download from ANES along with their associated filename
    

    # If we don't have our output_dir folder yet, create it
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Download each specified URL to the specified filename
    for filename, url in filenames_and_urls:
        download(filename, url, output_dir=output_dir)
        
def download(filename, url, output_dir="downloaded_data"):
    """
    Downloads a single URL to a given filename. If the filename ends in
    *.zip, it is unzipped with the contents placed in the same
    output_dir.
    
    Parameters
    ----------
    filename : str
      The name of the file to write to. If the filename
      ends in *.zip, it will be unzipped with the contents
      placed in the same output_dir

    url : str
      The URL to download the file from
    
    output_dir : str (optional, default="downloaded_data")
      An optional output directory to write the downloaded files to
      (defaults to downloaded_data)
    
    Returns
    -------
    None
      

    Examples
    --------
    >>> # This will download and unzip the timeseries data
    >>> download("timeseries.zip", "https://electionstudies.org/anes_timeseries_cdf_csv_20220916/")
    >>> # This will download the 2020 open-ended data
    >>> download("2020.xlsx", "https://electionstudies.org/anes_timeseries_2020_redactedopenends_excel_20211118/")
    """
    
    print("Downloading", filename)
    
    # Assemble a request with the necessary headers to avoid detection    
    # From https://stackoverflow.com/questions/38489386/how-to-fix-403-forbidden-errors-when-calling-apis-using-python-requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    request = urllib.request.Request(url, None, headers)

    # Read the response data from our request
    response = urllib.request.urlopen(request)
    data = response.read()

    # Write the data to a local file
    download_path = os.path.join(output_dir, filename)
    with open(download_path, "wb") as outputfile:
        outputfile.write(data)

    # If the output file is a .zip archive, unpack it to the output_dir directory        
    if filename.lower().endswith(".zip"):
        # From https://stackoverflow.com/questions/3451111/unzipping-files-in-python
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)