import pandas as pd
import openpyxl
from isbe.IsbeScrape import contribution_search

def get_names(sheet1):
    return [cell.value for cell in sheet1['A'] if cell.value is not None][1:]


def remove_bad_breaks(string):
    string = string.rsplit("|  Occ")[0]
    if string.count("|") > 1:
        string = string.replace(" | ", " ", 1)
    return string


def street_name_fix(StreetName):
    replacements = {
        'DR': 'DRIVE',
        'RD': 'ROAD', 
        'BLVD':'BOULEVARD',
        'ST':'STREET', 
        'STE':'SUITE',
        'APTS':'APARTMENTS', 
        'APT':'APARTMENT',
        'CT':'COURT',
        'LN' : 'LANE',
        'AVE':'AVENUE',
        'CIR':'CIRCLE',
        'PKWY': 'PARKWAY',
        'HWY': 'HIGHWAY',
        'SQ':'SQUARE',
        'BR':'BRIDGE',
        'LK':'LAKE',
        'MT':'MOUNT',
        'MTN':'MOUNTAIN',
        'PL':'PLACE',
        'RTE':'ROUTE',
        'TR':'TRAIL',
        'N': 'NORTH',
        'S': 'SOUTH',
        'E': 'EAST',
        'W': 'WEST'
    }
                    
    StreetName = StreetName.upper().strip().rstrip('.')
    return ' '.join(replacements.get(c, c) for c in StreetName.split())


def get_all_contributions(excel_filename):
    # Excel file should just have a column with names on "Sheet 1"
    writer = pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a', if_sheet_exists='replace')
    writer.book = openpyxl.load_workbook(excel_filename)
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    sheet1 = writer.sheets["Sheet1"]
    names = get_names(sheet1)
    list_of_dfs = []
    for name in names:
        first,last = name.split()
        table_txt = contribution_search(first, last)
        if table_txt is None:
            continue
        df = pd.read_html(table_txt)[0]
        list_of_dfs.append(df.drop(df.tail(1).index))
    df = pd.concat(list_of_dfs).reset_index(drop=True)
    df[["Contributed By", "Street Address"]] = df["Contributed By"].str.split(pat="|", n=1, expand=True)
    df["Street Address"] = df["Street Address"].apply(remove_bad_breaks)
    df[["Street Address", "City"]] = df["Street Address"].str.split(pat="|", n=1, expand=True)
    df[["City", "ZIP"]] = df["City"].str.rsplit(n=1, expand=True)
    df[["Contribution Type", "Received By"]] = df["Received By"].str.split(pat="|", expand=True)
    df["Amount"] = df["Amount"].str[1:-1]
    df = df.apply(lambda x: x.str.strip())
    df["Amount"] = df["Amount"].str.replace(',', '').astype("float")
    df["Amount Received Year"] = pd.to_datetime(df["Amount Received Date"], infer_datetime_format=True).dt.year
    df["Report Received Year"] = pd.to_datetime(df["Report Received Date"], infer_datetime_format=True).dt.year
    df = df[[
        "Contributed By",
        "Contribution Type",
        "Street Address",
        "City",
        "ZIP",
        "Amount",
        "Received By",
        "Amount Received Year",
        "Report Received Year",
        "Description",
        "Vendor Name",
        "Vendor Address",
    ]]
    df["Street Address"] = df["Street Address"].str.replace(".", "").apply(street_name_fix)
    df.to_excel(writer, 'Raw Data')

    grouped_df = pd.DataFrame(df.groupby(["Contributed By", "Received By", "ZIP", "Amount Received Year"])["Amount"].sum())
    grouped_df.to_excel(writer, 'Grouped Data')
    writer.save()
