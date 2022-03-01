#!/usr/bin/env python3
import sys
import boto3
from print_html_table import *
from common import *

if len(sys.argv) < 2:
	#err_msg="Usage: "+ sys.argv[0] + "{aws profile}"
	#print_error(err_msg)
	#sys.exit(1)
	aws_profile = "default"
else:
	aws_profile = sys.argv[1]

try:
	session = boto3.session.Session(profile_name=aws_profile)
	ec2c = session.client('ec2')
	response = ec2c.describe_instances() 
except Exception as e:
	print_error("ERROR : failed to connect to boto3 session")
	quit_error(str(e))


if len(response['Reservations']) == 0 or len(response['Reservations'][0]['Instances']) == 0:
	print_html_msg('No EC2 instance configured in this account')
	sys.exit(0)


## Print table ##
try:
	start_tclass()
	start_table()
	start_tbody()
	cheader_list=['Instance Name','Status','Instance ID','AMI ID','Platform','Type','Private IP','Schedule','AZ','VpcId','NetworkInterfaceId','SubnetId','EbsOptimized','RootDeviceType','IAMProfile','SecurityGroups','Launch Time']
	col_list=createRows(cheader_list,((15,'2'),))
#	cheader_list=[{'data':"Instance Name",'span':"1"},{'data':"Status", 'span':"1"},{'data':"Instance ID", 'span':"1"},{'data':"AMI ID",'span':"1"},{'data':"Platform",'span':"1"},{'data':"Type",'span':"1"},{'data':"Private IP",'span':"1"},{'data':"Schedule",'span':"1"},{'data':"AZ",'span':"1"},{'data':"VpcId",'span':"1"},{'data':"NetworkInterfaceId",'span':"1"},{'data':"SubnetId",'span':"1"},{'data':"EbsOptimized",'span':"1"},{'data':"RootDeviceType",'span':"1"},{'data':"IAMProfile",'span':"1"},{'data':"SecurityGroups",'span':"2"},{'data':"Launch Time",'span':"1"}]
	print_col_header(col_list)

	for r in response['Reservations']:
		for i in r['Instances']:
			fdict=flatten(i)
			data_list=[]
			key_list=['Tags#Key#Name','State#Name','InstanceId','ImageId','Platform','InstanceType','PrivateIpAddress','Tags#Key#Schedule','Placement#AvailabilityZone','VpcId','NetworkInterfaces#NetworkInterfaceId','SubnetId','EbsOptimized','RootDeviceType','IamInstanceProfile#Arn','SecurityGroups#GroupName,GroupId','LaunchTime']

			for key in key_list:
				getValAndAppend(fdict,key,data_list)

			
			status=data_list[1]
			if status == "running":
				color="#2CFF33"
			elif status in ("stopping", "stopped"):
				color="#ffd500"
			elif status in ("terminating", "terminated"):
				color="#FF0000"
			else:
				color="#FF0000"

			row_list=createRows(data_list,((1,'1',color),(15,'2')))
			print_trow(row_list)
	
	end_tbody()
	end_table()
	end_tclass()	

except Exception as e:
	quit_error(str(e))
