import os
import argparse


LOG_LEVELS:list[str] = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('logs', nargs="*")
parser.add_argument('-r', '--report')


def check_files(files: list[str]) -> bool:
    """Check if all files exist and are log files"""
    if len(files) == 0:
        return False
    for f in files:
        if not os.path.exists(f) or not f.endswith('.log'):
            print(f"Invalid file path: {f}")
            return False
    return True


def process_line(line: str) -> (tuple[str, str] | bool):
    """Process a line"""
    try:
        splitted: list[str] = line.split(" ")
        handler: str = splitted[3][:-1]
        error_level: str = splitted[2]
        if error_level not in LOG_LEVELS:
            print(f"Invalid error level: {error_level}")
            return False
        return handler, error_level
    except IndexError:
        pass
    return False


def process_files(files: list[str], handlers: dict) -> int:
    """Process the files"""
    total_count: int = 0
    if not check_files(files):
        return 0
    for i in files:
        file = open(i, 'r')
        for line in file:
            handler, error_level = process_line(line)
            if handlers.get(handler, None) == None:
                handlers[handler] = {
                    'DEBUG': 0,
                    'INFO': 0,
                    'WARNING': 0,
                    'ERROR': 0,
                    'CRITICAL': 0
                }
            handlers[handler][error_level] += 1
            total_count += 1
    return total_count


def output_report(report_filename: str, handlers: dict, total_count: int):
    """Output the report"""
    if report_filename == None:
        report_filename = "handlers"
    report = open(report_filename+".txt", "w")
    report.write(f"Total requests: {total_count}\n\n")
    report.write("HANDLER".ljust(30))
    report.write("DEBUG".ljust(10))
    report.write("INFO".ljust(10))
    report.write("WARNING".ljust(10))
    report.write("ERROR".ljust(10))
    report.write("CRITICAL".ljust(10))
    for handler, counts in handlers.items():
        report.write("\n")
        report.write(handler.ljust(30))
        for level, count in counts.items():
            report.write(str(count).ljust(10))
    report.write("\n")


def parse_and_write_report(files: list[str], report_filename: dict):
    """Process files, and output report"""
    handlers: dict = {}
    total_count: int = process_files(files, handlers)
    output_report(report_filename, handlers, total_count)

if __name__ == '__main__':
    args = parser.parse_args()
    parse_and_write_report(args.logs, args.report)
    
