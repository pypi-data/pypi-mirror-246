import pandas as pd
from io import StringIO
import random
from importlib import import_module
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

def __get_random_csv_file_from_folder(package):
    synthetic_csv_files = [file for file in pkg_resources.contents(package) if file.endswith('.csv')]
    random_synthetic_csv_file = random.choice(synthetic_csv_files)
    return pkg_resources.read_text(package, random_synthetic_csv_file)

def __get_alibaba_2018_trace(trace="machine_usage", stride_seconds=10, generation_strategy='real'):
    assert trace in ["machine_usage"], 'only "machine_usage" trace is supported right now for alibaba'
    assert stride_seconds in [10, 30, 300], 'only 10, 30 and 300 seconds are currently suported as stride_seconds in alibaba 2018 machine usage'
    assert generation_strategy in ["real", "synthetic"], 'only real and synthetic generation strategies are currently supported in alibaba 2018 machine usage'
    if generation_strategy == "real":
        module = import_module(f".alibaba2018", package=__package__)
        contents = pkg_resources.read_text(module, f'{trace}_grouped_{stride_seconds}_seconds.csv')
    else:
        assert stride_seconds in [300], 'only 300 seconds are currently suported as stride_seconds in synthetically-generated alibaba 2018 machine usage'
        submodule = import_module(f".alibaba2018.synthetic_{1}_day_{stride_seconds}_seconds", package=__package__)
        contents = __get_random_csv_file_from_folder(submodule)
    return pd.read_csv(StringIO(contents), index_col=False)


def __get_azure_v2_trace(trace="machine_usage", stride_seconds=300, generation_strategy='real'):
    assert trace in ["machine_usage"], 'only "machine_usage" trace is supported right now for azure_v2'
    assert stride_seconds in [300], 'only 300 seconds is currently supported as stride_seconds in azure_v2'
    assert generation_strategy in ["real", "synthetic"], 'only real and synthetic generation strategies are currently supported in azure_v2 machine usage'
    if generation_strategy == "real":
        module = import_module(f".azure_v2", package=__package__)
        contents = pkg_resources.read_text(module, f'{trace}_grouped_{stride_seconds}_seconds.csv')
    else:
        submodule = import_module(f".azure_v2.synthetic_{1}_day_{stride_seconds}_seconds", package=__package__)
        contents = __get_random_csv_file_from_folder(submodule)
    return pd.read_csv(StringIO(contents), index_col=False)


def __get_google_2019_trace(trace="machine_usage", stride_seconds=300, generation_strategy='real'):
    assert trace in ["machine_usage"], 'only "machine_usage" trace is supported right now for azure_v2'
    assert stride_seconds in [300], 'only 300 seconds is currently suported as stride_seconds in google2019'
    assert generation_strategy in ["real", "synthetic"], 'only real and synthetic generation strategies are currently supported in google2019 machine usage'
    if generation_strategy == "real":
        module = import_module(f".google2019", package=__package__)
        contents = pkg_resources.read_text(module, f'{trace}_grouped_{stride_seconds}_seconds_percent.csv')
    else:
        submodule = import_module(f".google2019.synthetic_{1}_day_{stride_seconds}_seconds", package=__package__)
        contents = __get_random_csv_file_from_folder(submodule)
    return pd.read_csv(StringIO(contents), index_col=False)

def get_trace(trace_name='alibaba2018', trace_type='machine_usage', stride_seconds=300, format='dataframe', generation_strategy='real'):
    assert trace_name in ['alibaba2018', 'azure_v2', 'google2019'], 'only alibaba2018, azure_v2 and google2019 traces are supported right now'
    assert trace_type in ['machine_usage'], 'only machine_usage traces are supported right now'
    assert stride_seconds in [10, 30, 300], 'only 10, 30 and 300 seconds are valid right now'
    assert format in ['dataframe', 'ndarray'], 'only "dataframe" and "ndarray" are supported right now'
    if trace_name == 'alibaba2018':
        res = __get_alibaba_2018_trace(trace=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
    elif trace_name == 'azure_v2':
        res = __get_azure_v2_trace(trace=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
    elif trace_name == 'google2019':
        res = __get_google_2019_trace(trace=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
    if format == 'ndarray':
        res = res.to_numpy()
    return res

def get_dataset_info(trace_name='alibaba2018', trace_type='machine_usage', stride_seconds=300):
    assert trace_name in ['alibaba2018', 'azure_v2',
                          'google2019'], 'only alibaba2018, azure_v2 and google2019 traces are supported right now'
    assert trace_type in ['machine_usage'], 'only machine_usage traces are supported right now'
    if trace_type == 'machine_usage':
        if trace_name == 'alibaba2018':
            dataset_info = {
                "timestamp_frequency_secs": stride_seconds,
                "column_config": {
                    "cpu_util_percent": {
                        "column_index": 0,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "mem_util_percent": {
                        "column_index": 1,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "net_in": {
                        "column_index": 2,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "net_out": {
                        "column_index": 3,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "disk_io_percent": {
                        "column_index": 4,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    }

                },
                "metadata": {
                    "fields": {
                        "cpu_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "mem_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "net_in": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "net_out": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "disk_io_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        }
                    }
                }
            }
        elif trace_name == 'google2019':
            dataset_info = {
                "timestamp_frequency_secs": stride_seconds,
                "column_config": {
                    "cpu_util_percent": {
                        "column_index": 0,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "mem_util_percent": {
                        "column_index": 1,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "assigned_mem_percent": {
                        "column_index": 2,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "cycles_per_instruction": {
                        "column_index": 3
                    }
                },
                "metadata": {
                    "fields": {
                        "cpu_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "mem_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "assigned_mem_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "cycles_per_instruction": {
                            "type": "numerical",
                            "subtype": "float"
                        }
                    }
                }
            }
        elif trace_name == 'azure_v2':
            dataset_info = {
                "timestamp_frequency_secs": stride_seconds,
                "column_config": {
                    "cpu_usage": {
                        "column_index": 0
                    },
                    "assigned_mem": {
                        "column_index": 1
                    }
                },
                "metadata": {
                    "fields": {
                        "cpu_usage": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "assigned_mem": {
                            "type": "numerical",
                            "subtype": "float"
                        }
                    }
                }
            }
    return dataset_info
