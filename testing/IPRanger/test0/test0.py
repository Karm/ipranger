import string
import random
import ipaddress
from tqdm import tqdm
from itertools import product

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1
#source: https://stackoverflow.com/questions/21014618/python-randomly-generated-ip-address-as-string


## This test aims to create a small volume of users that are frequently changing address (N iterations)
## Test0 tests only the switching of address,so the last address of each user should be the correct.
## The created addresses are unique and have a mask of /32 or /128 so **the case of subnets is not covered**.

def test0(letters, numbers,n,dataset,testfile,version):

	# set that holds the generated IP addresses
	ips = set()
	# list that holds the generated user IDs
	ids = []

	# open two files for writing: input dataset and test file
	with open(dataset,"w") as d,open(testfile,"w") as t:

		# generate all the possible combinations of #letters with a vocabulary of ascii lowercase charactes
		for letter in product(string.ascii_lowercase, repeat=letters):
			x = ''.join(letter)

			# for each combination, append all the possible numbers
			# the final ID will have the form: (letters){pow(26,letters)}-(numbers){pow(10,numbers)}
			for i in range(0,pow(10,numbers)):
				ids.append(x+"-"+str(i))

		# perform n IP assignments/user
		for rounds in range(n):
			print("Iteration #"+str(rounds))
			for i in tqdm(range(len(ids))):
				# pick a user
				id_=ids[i]
			
				# we want to generate unique IP addresses in order to avoid collisions (same IP address to N different users)
				while True: 
					# if version equals 4, generate an IPv4 address
					if version == 4:				
						ip = str(ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4))) + "/32"
					# if version equals 6, generate an IPv6 address
					elif version == 6:
						ip = str(ipaddress.IPv6Address._string_from_ip_int(random.randint(0, MAX_IPV6))) + "/128"

					# store the current size of the set
					old_len = len(ips)
					# update the set 
					ips.add(ip)
					# if the new size is larger, then we have a unique IP address, else try again
					if len(ips)>old_len:
						break
						
				# write tuple to the dataset
				d.write(id_+"\n"+ip+"\n")

				# if this is the last round, create the test file that holds the last know address of each user
				if (rounds == n-1):
					t.write(ip+"\n"+id_+"\n")



if __name__ == "__main__":	

	# Small Dataset
	## the total number of combinations is pow(26,<num_of_letters>:2)*pow(10,<num_of_numbers>:3) = 676000	
	## We are creating 6760000 touples of <user,address> as each user is changing 10 times IP address. 
	test0(2,1,10,"dataset0v4_small.txt","test0v4_small.txt",4)
	test0(2,1,10,"dataset0v6_small.txt","test0v6_small.txt",6)

	# Large Dataset
	## the total number of combinations is pow(26,<num_of_letters>:2)*pow(10,<num_of_numbers>:3) = 676000	
	## We are creating 6760000 touples of <user,address> as each user is changing 10 times IP address. 
	test0(2,3,10,"dataset0v4_large.txt","test0v4.txt_large",4)
	test0(2,3,10,"dataset0v6_large.txt","test0v6.txt_large",6)







