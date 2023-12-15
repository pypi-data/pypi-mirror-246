import argparse
from datetime import datetime
from datacentertracesdatasets import loadtraces

def main():
    parser = argparse.ArgumentParser(
        usage='datacentertracesdatasets-cli --trace_name [alibaba2018, azure_v2, google2019] [--filename] file_name_with_path [--trace_type] [machine_usage] [--stride_seconds] [10, 30, 300] [--generation_strategy] [real, synthetic]'
    )
    parser.add_argument(
        '-trace',
        '--trace_name',
        help='<Required> Select the data centre trace to be generated. The available options are: alibaba2018, azure_v2, and google2019.',
        choices=['alibaba2018', 'azure_v2', 'google2019'],
        required=True,
    )
    parser.add_argument(
        '-file',
        '--filename',
        help='<Optional> Include the a valida file name for the result. Both a filename (result.csv) or an absolute path (/Users/john/result.csv) are valid.',
        type=str,
        default=None,
        required=False,
    )
    parser.add_argument(
        '-type',
        '--trace_type',
        help='<Optional> Include the type of trace to be generated. The available options are: machine_usage',
        choices=['machine_usage'],
        default='machine_usage',
        required=False,
    )
    parser.add_argument(
        '-stride',
        '--stride_seconds',
        help='<Optional>  Include the frequency in seconds in which samples were taken. 300 seconds by default.',
        choices=['10', '30', '300'],
        default=300,
        required=False,
    )
    parser.add_argument(
        '-generation',
        '--generation_strategy',
        help='<Optional> Choose the generation mode for the traces. The available options are: real, synthetic. Synthetic traces are generated with: https://github.com/DamianUS/timegan-pytorch.',
        choices=['real', 'synthetic'],
        default='real',
        required=False,
    )
    args = parser.parse_args()
    __main_script(args)


def __main_script(arguments):
    dataframe = loadtraces.get_trace(trace_name=arguments.trace_name, trace_type=arguments.trace_type, stride_seconds=int(arguments.stride_seconds), generation_strategy=arguments.generation_strategy)
    filename = __get_file_path(arguments)
    dataframe.to_csv(filename, index=False)
    print(f"Data center trace successfuly generated and saved as {filename}.")

def __get_file_path(arguments):
    if arguments.filename is None:
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return f"{arguments.trace_name}-{arguments.trace_type}-{arguments.stride_seconds}s-{arguments.generation_strategy}-{timestamp}.csv"
    return arguments.filename

if __name__ == '__main__':
    main()
