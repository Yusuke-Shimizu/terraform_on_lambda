#!/usr/bin/env python
# coding: utf-8
import os
import subprocess
import re
import json
import sys

def handler(event, context): 
    cmd('./', "cp ./main.tf /tmp/")
    cmd('/tmp/', "terraform init --upgrade")
    result = cmd('/tmp/', "terraform plan")
    last_result = extraction(result)
    return last_result


def logger(f):
    def wrapper(*args, **kwargs):
        stdout, stderr = f(*args, **kwargs)
        print('stdout')
        print(stdout.decode("utf-8"))
        print('stderr')
        print(stderr.decode("utf-8"))
        if stderr == "":
            return stdout.decode("utf-8")
            # return stdout
        else:
            return stdout.decode("utf-8")
            # return stdout
    return wrapper

@logger
def cmd(path, command):
    print('command')
    print(command)
    os.chdir(path)
    result = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate() # 標準出力、標準エラーの取得
    return (stdout, stderr)


def extraction(plan):
    print(plan)
    change_state = {'add': 0, 'change': 0, 'destroy': 0}
    if "No changes" in plan:
        return change_state
    elif "Plan" in plan:
        line_extraction = re.findall("Plan.*", plan)
        result = "".join(line_extraction)
        
        change_state['add'] = int(re.findall('(\d)\sto\sadd', result)[0])
        change_state['change'] = int(re.findall('(\d)\sto\schange', result)[0])
        change_state['destroy'] = int(re.findall('(\d)\sto\sdestroy', result)[0])
        print("add, change, destroy")
        print(change_state)
        return change_state
    elif "Error" in plan:
        line_extraction = re.findall("Error.*", plan)
        result = "".join(line_extraction)
        return result
    else:
        result = "予期せぬエラーです。ログを確認して下さい。"
        return result
