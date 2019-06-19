"""
Format of the config file
src_path=path_to_what_backup ( file name or folder name)
dst_path=path_to_where_to_backup
num_copy=number of copies to maintain
"""

import datetime
import logging
import os
import shutil
import sys
import zipfile


class bad_config_exception(Exception):
    pass


class invalid_input_exception(Exception):
    pass


class bad_src_exception(Exception):
    pass


def parse_input_params():
    if (len(sys.argv) == 2) and os.path.isfile(sys.argv[1]):
        return sys.argv[1]

    raise invalid_input_exception('Invalid input')


def parse_config(config_file):
    with open(config_file) as c_file:
        for line in c_file:
            name, val = line.partition('=')[::2]
            if name == 'src_path':
                src_path = val
            elif name == 'dst_path':
                dst_path = val
            elif name == 'num_copy':
                num_copy = val
            else:
                raise bad_config_exception('Invalid config')

    return src_path.rstrip("\n\r"), dst_path.rstrip("\n\r"), num_copy.rstrip("\n\r")


def start_backup(src_path, dst_path):
    base_file_name = os.path.splitext(os.path.basename(src_path))[0]
    backup_file_name = base_file_name + '_' + datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    logging.info('data backup from ' + src_path)

    if not os.path.isdir(src_path) and not os.path.isfile(src_path):
        raise bad_src_exception('src_path does not exist')

    os.makedirs(dst_path, exist_ok=True)
    os.chdir(dst_path)

    if os.path.isdir(src_path):
        shutil.make_archive(backup_file_name, 'zip', src_path)
    elif os.path.isfile(src_path):
        with zipfile.ZipFile(backup_file_name + '.zip', 'w') as myzip:
            myzip.write(src_path)
        myzip.close()

    logging.info('data backup created ' + dst_path + '/' + backup_file_name)


def adjust_backup_count(dst_path, num_copy):
    os.chdir(dst_path)
    files = filter(os.path.isfile, os.listdir(dst_path))
    files = [os.path.join(dst_path, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files_to_keep = files[-int(num_copy):]

    for f in range(0, len(files)):
        if not files[f] in files_to_keep:
            os.remove(files[f])
            logging.info('data backup deleted ' + os.path.splitext(os.path.basename(files[f]))[0])


def main():
    try:
        config_file = parse_input_params()
        config_file_parent = os.path.abspath(os.path.join(config_file, '..'))
        # create logfile in same dir as the config file passed.
        logging.basicConfig(filename=str(config_file_parent + '/app.log'), filemode='a',
                            format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)

        logging.info('======== Backup script launched ========')
        src_path, dst_path, num_copy = parse_config(config_file)
        logging.info('configuration parsed = ' + config_file)
        start_backup(src_path, dst_path)
        logging.info('data backup done successfully')
        adjust_backup_count(dst_path, num_copy)
        logging.info('deleted extra copies successfully')
    except bad_config_exception:
        logging.fatal('Failed to backup: bad configuration passed')
    except invalid_input_exception:
        logging.fatal('Failed to backup: invalid input passed')
    except bad_src_exception:
        logging.fatal('src_path does not exist')
    except:
        logging.fatal('Failed to backup: unknown error')

    logging.info('======== Backup script exit ========')
    logging.shutdown()


if __name__ == "__main__":
    main()
