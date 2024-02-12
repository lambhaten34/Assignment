import json
import os
import time
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Python equivalent of ls command")
    parser.add_argument("-A", "--all", action="store_true", help="do not ignore entries starting with .")
    parser.add_argument("-l", action="store_true", help="use a long listing format")
    parser.add_argument("-r", action="store_true", help="reverse the order of the results")
    parser.add_argument("-t", action="store_true", help="sort by time_modified")
    parser.add_argument("--filter", choices=["file", "dir"], help="filter the output based on file or directory")
    parser.add_argument("path", nargs='?', default=".", help="optional path to list contents")

    args = parser.parse_args()
    return args


def list_directory_contents(data, show_hidden=False, long_format=False, reverse_order=False, sort_by_time=False,
                            filter_option=None, path="."):
    """
    List directory contents based on the provided arguments.
    """
    if path == ".":

        contents = data.get("contents", [])
    else:
        path_components = path.split('/')

        current_item = data

        for component in path_components:
            found = False
            for item in current_item.get("contents", []):

                if item["name"] == component:
                    current_item = item
                    found = True
                    break
            if not found:
                print(f"error: cannot access '{path}': No such file or directory")
                return
        contents = current_item
        if len(path_components) == 2:
            if long_format:
                permissions = contents["permissions"]
                size = contents["size"]
                time_modified = contents["time_modified"]
                modified_time = time.strftime("%b %d %H:%M", time.gmtime(time_modified))
                print(f"{permissions} {size} {modified_time} {os.path.splitext(contents['name'])[0]}")
                return
            else:
                print(contents['name'], end=' ')
                return
        else:
            if long_format:
                for item in contents.get('contents'):
                    permissions = item["permissions"]
                    size = item["size"]
                    time_modified = item["time_modified"]
                    modified_time = time.strftime("%b %d %H:%M", time.gmtime(time_modified))
                    print(f"{permissions} {size} {modified_time} {os.path.splitext(item['name'])[0]}")
                return
            else:
                for item in contents:
                    print(item['name'], end=' ')
                return
    if not show_hidden:
        contents = [item for item in contents if not item['name'].startswith('.')]

    if filter_option:
        if filter_option == "dir":
            contents = [item for item in contents if "contents" in item]
        elif filter_option == "fir":
            contents = [item for item in contents if "contents" not in item]

    if sort_by_time and reverse_order:
        contents.sort(key=lambda x: x["time_modified"], reverse=reverse_order)
        contents.reverse()
    if reverse_order:
        contents.reverse()

    if long_format:
        for item in contents:
            permissions = item["permissions"]
            size = item["size"]
            time_modified = item["time_modified"]
            modified_time = time.strftime("%b %d %H:%M", time.gmtime(time_modified))
            print(f"{permissions} {size} {modified_time} {os.path.splitext(item['name'])[0]}")
    else:
        for item in contents:
            print(item['name'], end=' ')


def main():
    args = parse_arguments()

    with open("Structure.json", "r") as file:
        data = json.load(file)

    reverse_order = args.r
    sort_by_time = args.t

    list_directory_contents(data, args.all, args.l, reverse_order, sort_by_time, args.filter, args.path)


if __name__ == "__main__":
    main()
