import pandas as pd
import sys
import more_itertools as mit

def parse_ip_assignees(csv_path):
    """
    Parses the IP address csv to ranges in which designations occupy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Designation"] = ip["Designation"].apply(lambda x: x.lower().replace("administered by", "").strip())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Designation"]), axis=1)
    .groupby(["Designation"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

def parse_ip_compressed(csv_path):
    """
    Parses the IP address csv to ranges IP addresses are either reserved, allocated, or legacy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Status [1]"] == ip["Status [1]"].apply(lambda x: x.lower())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Status [1]"]), axis=1)
    .groupby(["Status [1]"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

if __name__ == "__main__":
    print(parse_ip_assignees(sys.argv[1]), parse_ip_compressed(sys.argv[1]))
