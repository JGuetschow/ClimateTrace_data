# Climate Trace GHG emissions inventory data in PRIMAP2 format

## Author
* Johannes Gütschow: mail@johannes-guetschow.de

## Important Note
Climate trace does not specify the global warming potential used, thus the use of 100 year GWPs from AR4 is currently just guessed.

## Versions
* currently only the 2021 Repository is available

## Usage
* The data is ready to use in the folder data_primap2/<version>
* If you want to modify or run the code create the virtual environment using
  `doit setup_venv`. To convert the data to PRIMAP2 format run `doit convert_2021`.

## Requirements
* The code uses primap2 and pandas
* The repository uses datalad and pydoit

## References
* [Climate Trace](https://climatetrace.org)
* [PRIMAP2](https://github.com/pik-primap/primap2)
