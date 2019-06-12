"""
Format of the config file
src=value
dst=value
num_copy=value
"""

import logging
import os
import datetime
import shutil

# path where backup_config.txt is saved
config_file_base = r'C:\\Users\\therock\\backup\\'
config_file = config_file_base + 'backup_config.txt'


def parse_config():
    src_dir, dst_dir, num_copy = 'd', 'd', 0

    with open(config_file) as c_file:
        for line in c_file:
            name, val = line.partition('=')[::2]
            if name == 'src_dir':
                src_dir = val
            elif name == 'dst_dir':
                dst_dir = val
            elif name == 'num_copy':
                num_copy = val
            else:
                raise NameError('Invalid config')

    return src_dir.rstrip("\n\r"), dst_dir.rstrip("\n\r"), num_copy.rstrip("\n\r")


def start_backup(src_dir, dst_dir):
    if not os.path.isdir(src_dir):
        logging.fatal('src_dir doesnot exist')
    if not os.path.isdir(dst_dir):
        logging.fatal('dst_dir doesnot exist')

    base_file_name = os.path.splitext(os.path.basename(src_dir))[0]
    base_file_name += '_' + datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    os.makedirs(dst_dir, exist_ok=True)
    os.chdir(dst_dir)
    shutil.make_archive(base_file_name, 'zip', src_dir)
    logging.info('data backup created ' + base_file_name)


def adjust_backup_count(dst_dir, num_copy):
    os.chdir(dst_dir)
    files = filter(os.path.isfile, os.listdir(dst_dir))
    files = [os.path.join(dst_dir, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files_to_keep = files[-int(num_copy):]

    for f in range(0, len(files)):
        if not files[f] in files_to_keep:
            os.remove(files[f])
            logging.info('data backup deleted ' + os.path.splitext(os.path.basename(files[f]))[0])


def main():
    logging.basicConfig(filename=str(config_file_base + '\\app.log'), filemode='a',
                        format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)

    logging.info('======== Backup script launched ========')
    try:
        src_dir, dst_dir, num_copy = parse_config()
        logging.info('configuration parsed')
        start_backup(src_dir, dst_dir)
        logging.info('data backup done successfully')
        adjust_backup_count(dst_dir, num_copy)
        logging.info('deleted extra copies successfully')
    except NameError:
        logging.fatal('Configuartion Parsing failed')
        print('Configuartion Parsing failed')
        return

    logging.info('======== Backup script exit ========')
    logging.shutdown()


if __name__ == "__main__":
    main()
