import xarray as xr
import pandas as pd
import numpy as np
import os

def extract_argo_data():
    file_path = "data/raw/BD2902120_001.nc"
    
    print("Opening file...")
    ds = xr.open_dataset(file_path)
    
    print("Available variables:")
    for var in ds.data_vars:
        print(f"  {var}")
    
    print("\nExtracting key variables...")
    
    rows = []
    n_profiles = ds.sizes["N_PROF"]
    
    temp_var = None
    salt_var = None
    pres_var = None
    
    for var in ds.data_vars:
        if "TEMP" in var and "QC" not in var and "ERROR" not in var and "ADJUSTED" not in var:
            temp_var = var
        if "PSAL" in var and "QC" not in var and "ERROR" not in var and "ADJUSTED" not in var:
            salt_var = var
        if "PRES" in var and "QC" not in var and "ERROR" not in var and "ADJUSTED" not in var:
            pres_var = var
    
    print(f"\nUsing: temp={temp_var}, salt={salt_var}, pres={pres_var}")
    
    for i in range(n_profiles):
        try:
            lat = float(ds["LATITUDE"].values[i])
            lon = float(ds["LONGITUDE"].values[i])
            date = str(ds["JULD"].values[i])
            float_id = "2902120"
            
            pres = ds[pres_var].values[i] if pres_var else None
            temp = ds[temp_var].values[i] if temp_var else None
            salt = ds[salt_var].values[i] if salt_var else None
            
            temp_surface = float(temp[0]) if temp is not None and not np.isnan(temp[0]) else None
            salt_surface = float(salt[0]) if salt is not None and not np.isnan(salt[0]) else None
            max_depth = float(np.nanmax(pres)) if pres is not None else None
            
            rows.append({
                "float_id": float_id,
                "profile_index": i,
                "latitude": lat,
                "longitude": lon,
                "date": date,
                "temp_surface_c": round(temp_surface, 3) if temp_surface else None,
                "salinity_surface": round(salt_surface, 3) if salt_surface else None,
                "max_depth_m": round(max_depth, 1) if max_depth else None,
                "num_depth_levels": len(temp) if temp is not None else None
            })
            
        except Exception as e:
            print(f"Skipping profile {i}: {e}")
    
    df = pd.DataFrame(rows)
    
    print("\n--- Clean extracted data ---")
    print(df.to_string())
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/argo_profiles.csv", index=False)
    print("\nSaved to data/argo_profiles.csv")
    
    return df

if __name__ == "__main__":
    extract_argo_data()