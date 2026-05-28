import requests
import os
import xarray as xr
import pandas as pd
import numpy as np
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, value in attrs:
                if attr == "href" and value.endswith(".nc"):
                    self.links.append(value)

def get_file_list(float_id):
    base_url = f"https://data-argo.ifremer.fr/dac/incois/{float_id}/profiles/"
    response = requests.get(base_url)
    parser = LinkParser()
    parser.feed(response.text)
    return base_url, parser.links

def download_files(float_id, max_files=10):
    base_url, files = get_file_list(float_id)
    save_folder = "data/raw"
    os.makedirs(save_folder, exist_ok=True)
    
    downloaded = []
    print(f"Found {len(files)} files for float {float_id}")
    
    for filename in files[:max_files]:
        save_path = os.path.join(save_folder, filename)
        if os.path.exists(save_path):
            print(f"Already exists: {filename}")
            downloaded.append(save_path)
            continue
        
        url = base_url + filename
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            downloaded.append(save_path)
        else:
            print(f"Failed: {filename}")
    
    return downloaded

def extract_profiles(file_path, float_id):
    rows = []
    try:
        ds = xr.open_dataset(file_path)
        n_profiles = ds.sizes["N_PROF"]
        
        for i in range(n_profiles):
            try:
                lat = float(ds["LATITUDE"].values[i])
                lon = float(ds["LONGITUDE"].values[i])
                date = str(ds["JULD"].values[i])
                
                temp, salt, pres = None, None, None
                
                if "TEMP" in ds.data_vars:
                    temp = ds["TEMP"].values[i]
                if "PSAL" in ds.data_vars:
                    salt = ds["PSAL"].values[i]
                if "PRES" in ds.data_vars:
                    pres = ds["PRES"].values[i]
                
                temp_surface = round(float(temp[0]), 3) if temp is not None and not np.isnan(temp[0]) else None
                salt_surface = round(float(salt[0]), 3) if salt is not None and not np.isnan(salt[0]) else None
                max_depth = round(float(np.nanmax(pres)), 1) if pres is not None and not all(np.isnan(pres)) else None
                
                if lat != 0 and lon != 0:
                    rows.append({
                        "float_id": float_id,
                        "profile_index": i,
                        "latitude": lat,
                        "longitude": lon,
                        "date": date,
                        "temp_surface_c": temp_surface,
                        "salinity_surface": salt_surface,
                        "max_depth_m": max_depth,
                        "num_depth_levels": len(temp) if temp is not None else None,
                        "source_file": os.path.basename(file_path)
                    })
            except Exception as e:
                pass
        ds.close()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return rows

if __name__ == "__main__":
    float_ids = ["2902120", "2902121", "2902122"]
    
    all_rows = []
    
    for float_id in float_ids:
        print(f"\nProcessing float {float_id}...")
        try:
            files = download_files(float_id, max_files=10)
            for f in files:
                rows = extract_profiles(f, float_id)
                all_rows.extend(rows)
                print(f"  Extracted {len(rows)} profiles from {os.path.basename(f)}")
        except Exception as e:
            print(f"  Skipping float {float_id}: {e}")
    
    df = pd.DataFrame(all_rows)
    print(f"\nTotal profiles collected: {len(df)}")
    print(df.head(10).to_string())
    
    df.to_csv("data/argo_profiles.csv", index=False)
    print("\nSaved to data/argo_profiles.csv")

    from sqlalchemy import create_engine
import pandas as pd

def load_to_postgres():
    df = pd.read_csv("data/argo_profiles.csv")
    
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/floatchat_db")
    
    df.to_sql("argo_profiles", engine, if_exists="replace", index=False)
    
    print(f"Loaded {len(df)} rows into PostgreSQL!")
    print("Table: argo_profiles")

if __name__ == "__main__":
    load_to_postgres()