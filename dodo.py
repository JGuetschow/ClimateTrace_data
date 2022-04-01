# define tasks for Climate TRACE data repository
from doit import get_var


# create virtual environment
def task_setup_venv():
    """Create virtual environment"""
    return {
        'file_dep': ['code/requirements.txt'],
        'actions': ['python3 -m venv venv',
                    './venv/bin/pip install --upgrade pip',
                    './venv/bin/pip install -Ur code/requirements.txt',
                    'touch venv',],
        'targets': ['venv'],
        'verbosity': 2,
    }


# convert inventory

def task_convert_2021():
    """
    Convert the 2021 inventory to PRIMAP2 format
    """
    return {
        'targets': [f"data_primap2/2021/ClimateTRACE_Inventory_2021.csv",
                    f"data_primap2/2021/ClimateTRACE_Inventory_2021.yaml",
                    f"data_primap2/2021/ClimateTRACE_Inventory_2021.nc"],
        'actions': [f"datalad run -m 'Convert 2021 inventory to PRIMAP2 format' "
                    "--explicit "
                    f"-o data_primap2/2021/ClimateTRACE_Inventory_2021.* "
                    f"./venv/bin/python code/convert_CT_data_2021.py "],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


