from genericpath import isdir
import os
import shutil
import argparse
import json
import yaml
import time

# Cmd parameters
parse = argparse.ArgumentParser(description='A desktop clearning script!')
parse.add_argument('--setting_file', '-s', help='setting file', default="setting.yaml")

args = parse.parse_args()


# Loading setting file --> setting_data
setting_file_name = args.setting_file
with open(setting_file_name, 'r', encoding='utf') as fs:
    if os.path.splitext(setting_file_name)[-1] == '.json':
        setting_data = json.load(fs)
    elif os.path.splitext(setting_file_name)[-1] == '.yaml':
        setting_data = yaml.load(fs.read(), Loader=yaml.Loader)
    else:
        print("[error] The setting file's type is illegal!")
        exit()


# Get settings 
base_path = setting_data["base_path"]
default_time = setting_data["default_time"]


try:
    local_time = time.strftime('%Y_%m_%d_%H%M%S', time.localtime(time.time()))
    dst_dir = os.path.join(base_path, local_time)
    os.mkdir(dst_dir)
except Exception as e:
    print(e)

items = os.listdir(base_path)
# print(items)
for item in items:
    tmp_item_path = os.path.join(base_path, item)
    if time.strftime("%Y-%m-%d %H:%M:%S'", time.localtime(os.stat(tmp_item_path).st_ctime)) > default_time:
        shutil.move(os.path.join(base_path, item), dst_dir)


setting_data['default_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
with open(setting_file_name, 'w', encoding='utf-8') as fs:
    if os.path.splitext(setting_file_name)[-1] == '.json':
        setting_data = json.load(fs)
    elif os.path.splitext(setting_file_name)[-1] == '.yaml':
        yaml.safe_dump(setting_data, fs, default_flow_style=False)
    else:
        print("[error] The setting file's type is illegal!")
        exit()

print("SUCCESSFUL!")