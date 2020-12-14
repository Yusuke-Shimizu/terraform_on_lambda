#!/usr/bin/env python
# coding: utf-8
import os
import subprocess
import re
import json

def logger(f):
    def wrapper(*args, **kwargs):
        stdout, stderr = f(*args, **kwargs)
        print('stdout')
        print(stdout.decode("utf-8"))
        print('stderr')
        print(stderr.decode("utf-8"))
        if stderr == "":
            return stdout.decode("utf-8")
        else:
            return stdout.decode("utf-8")
    return wrapper

@logger
def cmd(path, command):
    os.chdir(path)
# Popenの第1引数にコマンドを指定、第2/3引数で標準出力、標準エラーにパイプを第二引数、第三引数の指定によって繋ぐ
    result = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate() # 標準出力、標準エラーの取得
    return (stdout, stderr)


def extraction(plan):
    print(plan)
    if "No changes" in plan:
        line_extraction = re.findall("No changes.*", plan) #検索してマッチした行をリストで返す
        result = "".join(line_extraction) #リストをstrにしてる
        return result
    elif "Plan" in plan:
        line_extraction = re.findall("Plan.*", plan)
        result = "".join(line_extraction)
        return result
    elif "Error" in plan:
        line_extraction = re.findall("Error.*", plan)
        result = "".join(line_extraction)
        return result
    else:
        result = "予期せぬエラーです。ログを確認して下さい。"
        return result


def main():
    # `terraform init --upgrade` で初期化とprovider versionのアップデート
    # cmd('./', "terraform init --upgrade")
    # terraform planの結果を格納
    result = cmd('./', "terraform plan")
    # print("result")
    # print(result)
    # 結果をextraction関数で判定してdictに格納
    last_result = extraction(result)
    print('last_result')
    print(last_result)


if __name__ == "__main__":
    main()
