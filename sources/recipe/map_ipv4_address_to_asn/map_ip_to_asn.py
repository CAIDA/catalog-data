"""
Author: Esteban Carisimo
Institution: Northwestern University
Email: esteban.carisimo@northwestern.edu

This script is part of the IP to ASN Mapper tool, leveraging CAIDA's pyipmeta library and
CAIDA's data repository of daily RouteViews prefix-to-AS snapshots for mapping IP addresses
to their corresponding Autonomous System Numbers (ASNs).
"""

from datetime import datetime

import _pyipmeta 
import pandas as pd
import requests
from bs4 import BeautifulSoup

def find_routeviews_snapshot_url(date: datetime) -> str:
    """
    Retrieves the URL for a RouteViews prefix-to-AS snapshot from CAIDA's data repository for a specified date.
    
    Parameters
    ----------
    date : datetime
        The date of the RouteViews prefix-to-AS snapshot to be downloaded.
    
    Returns
    -------
    url : str
        The URL to the RouteViews prefix-to-AS snapshot.
    """
    
    # Construct the base URL for the specific year and month
    base_url = f"http://data.caida.org/datasets/routing/routeviews-prefix2as/{date.year}/{date.month:02d}/"
    
    # Attempt to retrieve the webpage
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
    except requests.RequestException as e:
        raise SystemExit(f"Error fetching data: {e}")
    
    # Parse the webpage to find links
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    # Find the first file that matches the date format in its name
    for link in links:
        if date.strftime('%Y%m%d') in link.text:
            file_name = link.text
            return f"{base_url}{file_name}"
    
    # Return an an empty string as an error
    return ""

class IPToASN:
    """
    A class to map IP addresses to ASN (Autonomous System Number) using the RouteViews pfx2as snapshots.
    """

    def __init__(self, date: datetime):
        """
        Initializes the IPToASN mapper with data from a specific date.

        Parameters
        ----------
        date : datetime
            The date for which to fetch and use the RouteViews prefix-to-AS snapshot.
        """
        self.ip_meta = _pyipmeta.IpMeta()
        provider = self.ip_meta.get_provider_by_name("pfx2as")
        url_routeviews_snapshot = find_routeviews_snapshot_url(date)
        
        if url_routeviews_snapshot:  # Check directly if string is not empty
            self.ip_meta.enable_provider(provider, f"-f {url_routeviews_snapshot}")
            self.ip_to_asn = {}
        else:
            raise SystemExit("No snapshot found for the specified date.")

    def get_ip_to_asn(self, ip: str) -> int:
        """
        Retrieves the ASN for a given IP address. Caches the result to avoid repeated lookups.

        Parameters
        ----------
        ip : str
            The IP address for which to find the corresponding ASN.

        Returns
        -------
        int
            The ASN associated with the given IP address, or 0 if no ASN is found.
        """
        if ip not in self.ip_to_asn:
            lookup_result = self.ip_meta.lookup(ip)
            if lookup_result:
                (result,) = lookup_result
                self.ip_to_asn[ip] = result.get('asns')[-1] if result.get('asns') else 0
            else:
                self.ip_to_asn[ip] = 0

        return self.ip_to_asn[ip]

def main():
    # Create a DataFrame with IP addresses
    df = pd.DataFrame(["157.92.49.99", "8.8.8.8", "0.0.0.0"], columns=["ip"])

    # Load IP addresses from a CSV file
    # df = pd.read_csv('path_to_your_file.csv')

    # Load IP addresses from a JSON file
    # df = pd.read_json('path_to_your_file.json')

    # Load IP addresses from a Parquet file
    # df = pd.read_parquet('path_to_your_file.parquet')
    
    # Convert tuple to datetime object for the date
    date = datetime(2020, 3, 4)
    
    # Initialize the IP to ASN mapping class with the given date
    ip_to_asn_mapper = IPToASN(date)
    
    # Map each IP to its ASN and add as a new column in the DataFrame
    df["asn"] = df["ip"].apply(ip_to_asn_mapper.get_ip_to_asn)
    
    # Print the resulting DataFrame
    print(df)

if __name__ == "__main__":
    main()
