# -*- coding: utf-8 -*-
import os, sys, datetime, re
from jinja2 import Environment, FileSystemLoader

# 引数取得
argvs = sys.argv
argc = len(argvs)
print str(argc) + ": " + ', '.join(argvs)

if (argc != 2):
	print "argv error"
	quit()

# 指定ファイルの存在確認
path_content_file = argvs[1]
if not os.path.exists(path_content_file):
	print path_content_file + " is not found."
	quit()

# 指定ファイルからテンプレートに挿入するデータを取得
param_member_list = []
param_info_list = []
for line in open(path_content_file, 'r'):
	if not re.match("^\s*#", line):
		array = ""
		size = ""
		if re.match("^\s*@", line):
			param_info_list.append(line.strip())
		else:
			prefix, format, type, name, comment = line[:-1].split(',')
			prefix = prefix.strip()
			type = type.strip()
			name = name.strip()
			comment = comment.strip()
			format = format.strip()
			if re.match(".*\[.*\]", name):
				name, size = name.split("[")
				size = "[" + size
				if format == "w":
					array = "string"
				else:
					array = "binary"
			param_member_list.append({'prefix':prefix, 'format':format, 'type':type, 'array':array, 'name':name, 'size':size, 'comment':unicode(comment, 'utf-8')})

root, ext = os.path.splitext(path_content_file)
param_struct = os.path.basename(root)
param_define = param_struct.upper() + "_H_"

now = datetime.datetime.now()
param_date = now.strftime("%Y-%m-%d")

# テンプレートファイルを指定
path_template = "struct.h.template"
if os.path.exists(path_template):
	env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
	tpl = env.get_template(path_template)
else:
	print "file:" + path_template + " is not found."
	quit()

# テンプレートへの挿入
html = tpl.render({'struct':param_struct, 'date':param_date, 'define':param_define, 'info_list':param_info_list, 'member_list':param_member_list})

# ファイルへの書き込み
tmpfile = open(param_struct + ".h", 'w')
tmpfile.write(html.encode('utf-8'))
tmpfile.close()
