import os


def get_pretty_file_size(file_path):
    # Get the file size in bytes
    file_size = os.path.getsize(file_path)

    # Define the units and their conversion values
    units = ["B", "KB", "MB", "GB", "TB"]
    conversion_values = [1, 1024, 1024 ** 2, 1024 ** 3, 1024 ** 4]

    # Determine the appropriate unit to use based on the file size
    for i, value in enumerate(conversion_values[::-1]):
        if file_size >= value:
            pretty_size = file_size / value
            pretty_unit = units[len(units) - 1 - i]
            break

    # Format the size and unit as a string with two decimal places
    pretty_string = "{:.2f} {}".format(pretty_size, pretty_unit)

    return pretty_string
