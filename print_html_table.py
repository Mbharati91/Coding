#!/usr/bin/env python3

### NOTE ####
# data passed to below functions must be list #
# the list item should be list which contains dict with data and span key #

def start_tclass():
	print("<div class=\"tab-content\">")
	
def start_table():
	print("<table id=\"myTable\" class=\"sortable customTable\">")

def start_tbody():
        print("<tbody>")

def print_theader(cdata,cspan):
	print("<thead><th style=\"text-align:left;font-size:16px\" colspan=" + cspan + ">" + cdata + "</th></thead>")	

	
def print_col_header(cdata):
	print("<thead><tr>")
	for val in cdata:
		if 'color' in val:
			print("<th colspan=" + val['span'] + " bgcolor=" + val['color'] + ">" + val['data'] +"</th>")
		else:
			print("<th colspan=" + val['span'] + ">" + val['data'] +"</th>")	
		
	print("</tr></thead>")
	

def print_col(cdata):
	print("<tr>")
	for val in cdata:
		if 'color' in val:
			print("<th colspan=" + val['span'] + " bgcolor=" + val['color'] + ">" + val['data'] +"</th>")
		else:
			print("<th colspan=" + val['span'] + ">" + val['data'] +"</th>")

	print("</tr>")

def print_trow(rdata):
	print("<tr>")
	for val in rdata:
		if 'color' in val:
			print("<td colspan=" + val['span'] + " bgcolor=" + val['color'] + ">" + val['data'] +"</td>")
		else:
			print("<td colspan=" + val['span'] + ">" + val['data'] +"</td>")

	print("</tr>")

def end_tbody():
	print("</tbody>")

def end_table():
	print("</table>")

def end_tclass():
	print("</div>")

def add_break():
	print("<br>")	
