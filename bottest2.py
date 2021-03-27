name_list = []
special_names_list = []
names_dict = {}
file_name = "whitelist.txt"
excl_file_name = "permawhitelist.txt"
with open(file_name, 'r') as names:
    for line in names:
        if (line in names_dict):
            names_dict[line] = names_dict[line] + 1
        else:
            names_dict[line] = 1

        if (line not in name_list):
            name_list.append(line)
            
with open(excl_file_name, 'a+') as special_names:
    special_names.seek(0)
    for line in special_names:
        special_names_list.append(line)
        print(line)
    print(special_names_list)
    for item in list(names_dict.keys()):
        if ((names_dict[item] > 6) and (item not in special_names_list)):
            special_names.write(item)

with open (file_name, 'w') as new_names:
    for item in name_list:
        new_names.write(item)


