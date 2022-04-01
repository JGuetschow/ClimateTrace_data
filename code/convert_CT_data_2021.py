# convert 2021 inventory to PRIMAP2 format

#imports
import primap2 as pm2
import pandas as pd
import os
import sys
from pathlib import Path

# configuration
### folders and filenames
input_folder = Path("../downloaded_data/2021")
input_file = "climatetrace_emissions_by_subsector_timeseries_interval_year_since_2015_to_2020.csv"
output_folder = Path("../data_primap2/2021")
output_filename = "ClimateTRACE_Inventory_2021"
compression = dict(zlib=True, complevel=9)

### primap2 format definitions
coords_terminologies = {
    "area": "ISO3",
    "category": "ClimateTrace2021",
    "scenario": "ReleaseDate",
}

coords_defaults = {
    "source": "Climate Trace",
    "provenance": "measured",
    "scenario": "2021",
    "entity": "KYOTOGHG (AR4GWP100)",
    # GWPs are unclear as they only state that it's 100 year potentials but not from which AR
    "unit": "t CO2 / yr"
}

coords_cols = {
    "category": "sector",
    "area": "country",
}

meta_data = {
    "references": "https://www.climatetrace.org/inventory",
    "rights": "",
    "contact": "johannes.guetschow@pik-potsdam.de",
    "title": "Climate Trace Emissions Inventory 2021",
    "comment": "Read fom csv file by Johannes Gütschow",
    "institution": "Climate Trace - www.climatetrace.org",
}

# change working directory to script directory for proper folder names
script_path = os.path.abspath(sys.argv[0])
script_dir_name = os.path.dirname(script_path)
os.chdir(script_dir_name)

# read the data
ct_data = pd.read_csv(input_folder / input_file)

# convert dates to just years
ct_data["start"] = ct_data["start"].replace(r"([0-9]{4})\-[0-9]{2}\-[0-9]{2}", r"\1", regex=True)

# combine sector information in one column
ct_data["sector"] = ct_data["sector"] + " - " + ct_data["subsector"]

# drop old columns and rename columns
ct_data = ct_data.drop(columns = ["end", "subsector", "country_full"])
ct_data = ct_data.rename(columns={"Tonnes Co2e": "data", "start": "time"})

# convert to primap2 format
ct_data_if = pm2.pm2io.convert_long_dataframe_if(
    ct_data,
    coords_cols=coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    meta_data=meta_data,
    convert_str=True
    )

# write the result in IF
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(output_folder / output_filename, ct_data_if)

# Convert to native pm2 format and write result
ct_data_pm2 = pm2.pm2io.from_interchange_format(ct_data_if)
encoding = {var: compression for var in ct_data_pm2.data_vars}
ct_data_pm2.pr.to_netcdf(output_folder / (output_filename + ".nc"), encoding=encoding)