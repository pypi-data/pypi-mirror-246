def print_lol(data_list):
    for eachItem in data_list:
        if isinstance(eachItem,list):
            print_lol(eachItem)
        else:
            print(eachItem)