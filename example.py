#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 pigeon-sable
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pythonファイル生成プログラム：PythonプロジェクトもしくはPythonファイルを生成します。
"""

__author__ = 'pigeon-sable'
__version__ = '0.0.0'
__date__ = '2023/03/04 (Created: 2022/08/05)'

import sys
import os
import textwrap
from datetime import date
import subprocess


def header() -> None:
    """
    ヘッダー文字列（シェバン、マジックコメント、author、version、date）を応答します。
    """
    dt_today = str(date.today())
    date_info = dt_today[0:4] + '/' + dt_today[5:7] + '/' + dt_today[8:10]

    head_str = f"""\
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    \"""
    Python生成プログラム：Pythonファイルを生成します。
    \"""

    __author__ = 'pigeon-sable'
    __version__ = '0.0.0'
    __date__ = '{date_info} (Created: {date_info})'

    import sys

    """

    return textwrap.dedent(head_str)

def gen_class(project_name: str) -> str:
    """
    クラスの情報を応答します。
    """
    class_info = f"""\
    class {project_name}:
        \"""
        {project_name}クラスです。
        \"""

        def __init__(self):
            \"""
            インスタンスを生成します。
            \"""

    """

    return textwrap.dedent(class_info)

def footer() -> str:
    """
    フッター文字列を応答します。
    """
    foot_str = """\
    def main():
        \"""
        Pythonファイルを生成するメイン（main）プログラムです。
        常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
        \"""

    if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
        sys.exit(main())
    """

    return textwrap.dedent(foot_str)

def template(project_name: str = '', project_mode: bool = True) -> str:
    """
    Pythonファイルのテンプレートを応答します。
    """
    if project_mode:
        return header() + gen_class(project_name) + footer()

    return header() + footer()

def command_check() -> int:
    """
    コマンドのチェックを行います。
    コマンドの長さが 1 または 2 以外のとき、プログラムを終了します。
    """
    num_args = len(sys.argv)

    if len(sys.argv) != 1 and len(sys.argv) != 2:
        print("The use of the command is wrong.")
        sys.exit(1)

    return num_args

def make_file_name(num_args: int) -> str:
    """
    pythonファイルの名前を決めるプログラムです。
    作成するPythonファイルの名前を返します。
    """
    if num_args == 1: # コマンドライン引数がないとき
        file_name = input('Please enter the name of the file to be created: ')
    else: # コマンドライン引数があるとき
        file_name = sys.argv[1]

    if '.py' not in file_name:
        file_name = file_name + '.py'

    return file_name

def main() -> None:
    """
    Pythonファイルを生成するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """
    print('-' * 80)
    current_directory = os.getcwd()

    mode = input('Project mode? or Create file mode? (P/c): ')
    if ('c' in mode) or ('C' in mode):
        num_args = command_check()
        file_name = make_file_name(num_args)
        choice_directory = input('Generate python file in current_directory or optional_directory? [C/o] : ')
        if choice_directory != 'o': # カレントディレクトリに生成するとき
            directory = os.getcwd()
        else:
            directory = input('What directory name in absolute path?: ')

        a_file = os.path.join(directory, file_name)
        with open(a_file, 'w', encoding='utf-8') as a_file:
            a_file.write(template(project_mode=False))

        print('-' * 80)
        print('Finish generating ' + file_name + ' in ' + directory)

    else:
        project_name = input('Please enter the name of the project to be created: ')
        if project_name == '':
            project_name = 'Project'
        elif project_name[0].islower(): # 先頭文字が小文字のとき、大文字に変換する。
            project_name = project_name.capitalize()

        try:
            subprocess.run(['mkdir', project_name], check=True) # ディレクトリを作成する。
            target_dir = 'origin'
            subprocess.run(f"cp {current_directory}/{target_dir}/Makefile.txt {project_name}", shell=True, check=True)
            subprocess.run(f"mv {project_name}/Makefile.txt {project_name}/Makefile", shell=True, check=True)
            subprocess.run(f"cp {current_directory}/{target_dir}/modified_pylintrc.txt {project_name}", shell=True, check=True)
            subprocess.run(f"mv {project_name}/modified_pylintrc.txt {project_name}/.pylintrc", shell=True, check=True)
        except subprocess.CalledProcessError as e: # プロセスが非ゼロで終了したとき
            print(e, file=sys.stderr) # 標準エラー出力に出力する。
            sys.exit(1)

        a_file = os.path.join(os.getcwd(), project_name, project_name + '.py')
        with open(a_file, 'w', encoding='utf-8') as a_file:
            a_file.write(template(project_name, True))

        print('-' * 80)

        print('Finish generating ' + project_name + ' in ' + os.getcwd())

if __name__ == '__main__':  # ifによって、このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(main())
