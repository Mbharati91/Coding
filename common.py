#!/usr/bin/env python3
import sys
import collections
import re 

def print_error(msg):
	print("<h4 style=\"color:orange\"> " , msg ,"</h4>")

def quit_error(msg):
	print("<h4 style=\"color:orange\"> " , msg ,"</h4>")
	sys.exit(1)

def print_html_msg(msg):
	print("<h4 style=\"color:white\"> " , msg ,"</h4>")


def joinDictItems(dict_param,separator):
	'''
	join the values from dictionary
	'''
	try:	
		if type(dict_param) != dict:
			join_val = "Input Param must be Dict!"
		else:	
			join_val = separator.join('{}: {}'.format(key, value) for key, value in dict_param.items())

		return join_val
	except Exception as e:
		return str(e)
	
def joinListItems(list_param,separator):
	'''
	join the values from list
	'''
	try:
		if type(list_param) != list:
			join_val = "Input Param must be list!"
		else:
			join_val = separator.join(map(str,list_param))

		return join_val
	except Exception as e:
		return str(e)


def join_val(val):
	'''
	Join items according to list or dict
	'''
	try:
		if type(val) is list:
			val_append = joinListItems(val,', ')
		elif type(val) is dict:
			val_append = joinDictItems(val,', ')
		else:
			val_append = str(val)
	
		return val_append
	except Exception as e:
		return str(e)

def dictKeyCheck(dc,key):
	'''
	check if key is present in dict
	'''
	try:
		if key in dc.keys():
			return True
		else:
			return False
	except Exception as e:
		return False 
	
def dictRegexKeyCheck(dc,key):
	'''
	check if regex key is present in dict
	'''
	try:
		chk=False
		for k,v in dc.items():
			if re.match(key,k):
				chk=True
				break
		return chk 
	except Exception as e:
		return str(e)
	
def getDictValRegex(dc,key):
	'''
	get values as per regex key match from flattern dict
	'''
	try:
		if dictRegexKeyCheck(dc,key):
			key_list = [ k for k, v in dc.items() if re.match(key, k)]
			regex = '^(?=.*[0-9])(?=.*[a-zA-Z])' 
			num_list = [ v for v in key_list if re.match(regex,v)]
			if len(num_list) > 0:	
				val_list = [str(v) for k, v in dc.items() if re.match(key, k)]
				val = join_val(val_list)
			else:
				val = getDictKeyValPairRegex(dc,key)
		else:
			val = '-'

		return val
	except Exception as e:
		return str(e)

def getDictVal(dc,key):
	'''
	get plain value from flattern dict 
	'''
	try:
		if dictKeyCheck(dc,key):
			val = dc[key]
		else:
			val = '-'
		
		return val
	except Exception as e:
		return str(e)

def getDictKeyVal(dc,key):
	'''
	get key/val from flattern dict either in key/pair form of plain value
	'''
	try:
		if dictKeyCheck(dc,key):
			if type(dc[key]) == dict:
				val = getDictKeyValPair(dc,key)
			else:
				val_list = [str(v) for k, v in dc.items() if k==key]
				val = join_val(val_list)
		else:
			val = '-'
		return val

	except Exception as e:
		return str(e)

def getDictKeyValPairRegex(dc,key):
	'''
	get values from flattern dict in form of key,pair matteched by regex key
	'''
	try:
		if dictRegexKeyCheck(dc,key):
			vlen = [v for k,v in dc.items() if re.match(key, k)]
			if len(vlen) == 1 and vlen[0] == u'':
				val = '-'
			else:
				val_list = ['{}: {} '.format(k.split('#')[-1], v) for k, v in dc.items() if re.match(key, k)]
				val = join_val(val_list)
		else:
			val = '-'

		return val
	except Exception as e:
		return str(e)

def getDictKeyValPair(dc,key=''):
	'''
	get values from flattern dict in form of key,pair
	'''
	try:
		if (not key):
			val_list = ['{}: {}'.format(k, v) for k, v in dc.items()]
			val = join_val(val_list)
		elif dictKeyCheck(dc,key):
			val_list = ['{}: {}'.format(k, v) for k, v in dc.items() if k==key]
			val = join_val(val_list)
		else:
			val = '-'

		return val
	except Exception as e:
		return str(e)

def getTagKeyVal(dc,key):
	'''
	get values of Tags from flattern dict
	'''
	try:
		val='-'
		key_list=key.split('#')[:-1]
		key_val=key.split('#')[-1]
		tag_key='#.*'.join(map(str,key_list))
		for k,v in dc.items():
			if re.match(tag_key,k) and v == key_val:
				val_key = k.replace('Key','Value')
				val = str(dc[val_key])
		return val
	except Exception as e:
		return str(e)


def flatten(d,sep="#"):
	'''
	This function is to create a ordered flat dictionary out of multi nested list/dictionalries
	'''
	obj = collections.OrderedDict()
	def recurse(t,parent_key=""):
		if isinstance(t,list):
			if len(t):
				for i in range(len(t)):
					recurse(t[i],parent_key + sep + str(i) if parent_key else str(i))
			else:
				obj[parent_key] = u''

		elif isinstance(t,dict):
			if len(t):
				for k,v in t.items():
					recurse(v,parent_key + sep + k if parent_key else k)
			else:
				obj[parent_key] = u''
		else:
			obj[parent_key] = t

	recurse(d)

	return obj

def check_sub_str(string, sub_str): 
	'''
	Check if substring is present
	'''
	if (string.find(sub_str) == -1): 
		return False 
	else: 
		return True 

def check_multi_substr(string,substr_list):
	'''
	check if multiple substrings are present
	the substings must be provided in form of list
	the output will be returned in form of list with True/False for each substr in list
	'''
	
	try:
		sub_check=[str in string for str in substr_list]
	except:
		sub_check=[]	

	return sub_check

def getSubDictVal(dc,start_keys,end_keys):
	try:
		val=u''
		dc_list=[]
		new_dc = {k: v for k,v in dc.items() if re.match(start_keys,k)}
		val_list = ['{}: {}'.format(k.split('#')[-1], v) for k, v in dc.items() if re.match("|".join(end_keys), k)]
		val = join_val(val_list)
		return val
	except Exception as e:
		return str(e)
				

def createRows(data_list,row_conf=()):
	row_list=[]
	try:
		if len(row_conf) == 0:
			for val in data_list:
				row_data = {'data': val , 'span':"1"}
				row_list.append(row_data)
		else:
			for index,val in enumerate(data_list):
				if any(index in conf for conf in row_conf):
					for conf in row_conf:
						if index == conf[0]:
							if len(conf) == 3:
								row_data = {'data': val , 'span':conf[1], 'color':conf[2]}
							else:
								row_data = {'data': val , 'span':conf[1]}
					row_list.insert(index,row_data)
				else:
					row_data = {'data': val , 'span':'1'}
					row_list.insert(index,row_data)

		return row_list
	except Exception as e:
		row_list.append({'data':str(e),'span':len(row_conf)})
					
def getValAndAppend(dc,keys,data_list):
	try:
		if dictKeyCheck(dc,keys):
			val = join_val(dc[keys])
		elif check_sub_str(keys,'Tags'):
			val = getTagKeyVal(dc,keys)
		elif check_sub_str(keys,'#'):
			if check_sub_str(keys,','):
				key_list = keys.split('#')
				start_keys = '#'.join(map(str,key_list[:-1])) + '#'
				## filter will remove any empty keys from list ##
				end_keys = list(filter(None,key_list[-1].split(','))) 
				val = u''
				nkey_list=[]
				for key in end_keys:
					nkey = (start_keys + key).replace('#','.*')
					nkey_list.append(nkey)
				nkeys = "|".join(nkey_list)	
				val = getDictKeyValPairRegex(dc,nkeys)
			else:
				nkey = keys.replace('#','.*')
				val = getDictValRegex(dc,nkey)
		elif check_sub_str(keys,','):
			key_list = list(filter(None,keys.split(',')))
			val = getDictKeyValPairRegex(dc,key_list)	
		else:
			val='-'

		data_list.append(val)

	except Exception as e:
		data_list.append(str(e))
