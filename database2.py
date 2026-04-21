import pandas as pd
import os

# File where all jobs will be saved
FILE = "jobs.csv"

# Columns in our database
COLUMNS = ["Company", "Role", "Date Applied", 
           "Status", "Notes"]

def load_data():
    # If file exists load it, else create empty one
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    else:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    # Save dataframe to CSV
    df.to_csv(FILE, index=False)

def add_job(company, role, date, status, notes):
    df = load_data()
    # Create new row
    new_row = {
        "Company": company,
        "Role": role,
        "Date Applied": date,
        "Status": status,
        "Notes": notes
    }
    # Add new row to dataframe
    df = pd.concat([df, pd.DataFrame([new_row])], 
                    ignore_index=True)
    save_data(df)
    return df

def update_status(index, new_status):
    df = load_data()
    df.at[index, "Status"] = new_status
    save_data(df)
    return df

def delete_job(index):
    df = load_data()
    df = df.drop(index=index).reset_index(drop=True)
    save_data(df)
    return df