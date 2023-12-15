[![version](https://img.shields.io/badge/pypi-1.0.1-blue)](https://pypi.org/project/datacentertracesdatasets-cli/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-darkgreen)](https://www.python.org/downloads/release/python-390/)
[![license](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

# Datacentertracesdatasets_clicli: Command-line interface for datacentertracesdatasets package

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Description

Datacentertracesdatasets-cli is a command-line interface tool that act as an interface of the [datacentertracesdatasets package](https://github.com/DamianUS/datacentertracesdatasets). Datacentertracesdatasets package facilitates the access to three dataset traces: Alibaba2018, Azure_v2 and Google2019.

This command-line interface is OS independent and can be easily installed and used.

### Available original datasets
Public datasets organized for machine learning or artificial intelligence usage. The following dasets can be used:

## Alibaba 2018 machine usage
Processed from the original files found at:
https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2018

This repository dataset of machine usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field            | Type       | Label | Comment                                            |
+--------------------------------------------------------------------------------------------+
| cpu_util_percent | bigint     |       | [0, 100]                                           |
| mem_util_percent | bigint     |       | [0, 100]                                           |
| net_in           | double     |       | normarlized in coming network traffic, [0, 100]    |
| net_out          | double     |       | normarlized out going network traffic, [0, 100]    |
| disk_io_percent  | double     |       | [0, 100], abnormal values are of -1 or 101         |
+--------------------------------------------------------------------------------------------+
```

Three sampled datasets are found: average value of each column grouped every 10 seconds as original, and downsampled to 30 seconds and 300 seconds as well.
Every column includes the average utilization of the whole data center.

### Figures
Some figures were generated from these datasets

| ![cpu_util_percent_usage_days_1_to_8_grouped_10_seconds](https://user-images.githubusercontent.com/19324988/202569296-3bb72ad4-92e7-4200-a19d-ef6fc26722ce.png) |
|:--:|
|Figure: CPU utilization sampled every 10 seconds|

|![mem_util_percent_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202569501-7840c0a0-b4e8-4f7d-bb92-875e38c616e8.png)|
|:--:|
|Figure: Memory utilization sampled every 300 seconds|

|![net_in_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571345-79581b7f-c7cd-4690-aeea-56cc9f903396.png)|
|:--:|
|Figure: Net in sampled every 300 seconds|

|![net_out_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571570-d0067db7-3b75-4fb1-a866-8eeec78dd415.png)|
|:--:|
|Figure: Net out sampled every 300 seconds|

|![disk_io_percent_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571350-1f5defbf-6cb0-456a-b9d3-2f4d64a8021b.png)|
|:--:|
|Figure: Disk io sampled every 300 seconds|



## Google 2019 instance usage
Processed from the original dataset and queried using Big Query. More information available at:
https://research.google/tools/datasets/google-cluster-workload-traces-2019/

This repository dataset of instance usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field                         | Type       | Label | Comment                               |
+--------------------------------------------------------------------------------------------+
| avg_cpu                       | double     |       | [0, 1]                                |
| avg_mem                       | double     |       | [0, 1]                                |
| avg_assigned_mem              | double     |       | [0, 1]                                |
| avg_cycles_per_instruction    | double     |       | [0, _]                                |
+--------------------------------------------------------------------------------------------+
```
One sampled dataset is found: average value of each column grouped every 300 seconds as original.
Every column includes the average utilization of the whole data center.

### Figures
Some figures were generated from these datasets

|![cpu_usage_day_26](https://user-images.githubusercontent.com/19324988/202570580-6be32fd7-3e39-4e0a-bc8e-abda05c5edd2.png)|
|:--:|
|Figure: CPU usage day 26 sampled every 300 seconds|

|![mem_usage_day_26](https://user-images.githubusercontent.com/19324988/202570586-388eafcd-a70e-40d3-8a80-9cdab0ef6236.png)|
|:--:|
|Figure: Mem usage day 26 sampled every 300 seconds|

|![assigned_mem_day_26](https://user-images.githubusercontent.com/19324988/202570579-6d9744f8-97fb-42d2-bb9a-b9c7cf88bdb4.png)|
|:--:|
|Figure: Assigned mem day 26 sampled every 300 seconds|

|![cycles_per_instruction_day_26](https://user-images.githubusercontent.com/19324988/202570583-e28bae12-8540-4a69-845b-12cfc9be8c33.png)|
|:--:|
|Figure: Cycles per instruction day 26 sampled every 300 seconds|




## Azure v2 virtual machine workload
Processed from the original dataset. More information available at:
https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md

This repository dataset of instance usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field                         | Type       | Label | Comment                               |
+--------------------------------------------------------------------------------------------+
| cpu_usage                     | double     |       | [0, _]                                |
| assigned_mem                  | double     |       | [0, _]                                |
+--------------------------------------------------------------------------------------------+
```
One sampled dataset is found: sum value of each column grouped every 300 seconds as original. For computing CPU_usage, we used core_count usage of each virtual machine.
Every column includes the total consumption of the whole data center virtual machines.
There is a version of each file including timestamp (from 0 to 2591700, in 300 seconds timestep), and other version without timestamp

### Figures
Some figures were generated from these datasets

|![cpu_usage_month](https://user-images.githubusercontent.com/19324988/202569892-50ceb7d1-7892-4c36-bd81-ab2b3398bf58.png)|
|:--:|
|Figure: CPU total usage by virtual machines sampled every 300 seconds.|

|![assigned_mem_month](https://user-images.githubusercontent.com/19324988/202569860-c85fe1da-4604-435f-8315-7d6b828a8ba2.png)|
|:--:|
|Figure: Total assigned memory for virtual machines sampled every 300 seconds.|


### Available sythetic datasets

Moreover, for dataset augmentation and deep learning purposes, the datasets have been augmented using TimeGAN (https://github.com/DamianUS/timegan-pytorch) trained models.

The augmented datasets are composed of time series of lenght 288 and sampled to 300 seconds, that would correspond to one operational day of the data center.

## Installation

To install the tool in your local environment, just run follow command:

```Bash
pip install datacentertracesdatasets-cli
```

## Basic usage examples:

Some examples for obtaining the datasets are shown below.

1. Full Azure_V2 original dataset sampled at 300 seconds:
    ```Bash
    datacentertracesdatasets-cli -trace azure_v2
    ```
   The resulting file will be found at:

1. Full Alibaba2018 original dataset sampled at 10 seconds:
    ```Bash
    datacentertracesdatasets-cli -trace alibaba2018 -stride 10
    ```

1. A synthetic sample of 1 day for Google2019 sampled at 300 seconds:
    ```Bash
    datacentertracesdatasets-cli -trace google2019 -generation synthetic
    ```

1. A synthetic sample of 1 day for Google2019 sampled at 300 seconds providing a filename:
    ```Bash
    datacentertracesdatasets-cli -trace google2019 -generation synthetic -file my_dataset.csv
    ```

## License

Datacentertracesdatasets-cli is free and open-source software licensed under the [MIT license](LICENSE).

## Acknowledgements
Project PID2021-122208OB-I00, PROYEXCEL\_00286 and  TED2021-132695B-I00 project, funded by MCIN / AEI / 10.13039 / 501100011033, by Andalusian Regional Government, and by the European Union - NextGenerationEU.