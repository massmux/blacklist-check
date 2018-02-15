#!/usr/bin/python

"""
massmux@gmail.com
check a list of IPs against a list of blacklists
"""

import dns.resolver
import sys, os, socket

def sendmessage(fromstring,emailto,emailsubject,emailmessage):
        p = os.popen ("/usr/sbin/sendmail -t -i "+ fromstring +" " + emailto, "w")
        mess="From: "+fromstring+"\r\nReturn-Path: "+ fromstring +"\r\nReply-To: "+ fromstring +"\r\nSubject: "+emailsubject+"\r\n\n"+emailmessage
        p.write(mess)
        exitcode = p.close()
        return exitcode

##thisHost=socket.gethostname()

f=open("blacklist_list.txt")
bls = [line.rstrip('\n') for line in f]
 
if len(sys.argv) != 2:
    print 'Usage: %s <ip>' %(sys.argv[0])
    quit()
 
myIP = sys.argv[1]
thisHost=socket.gethostbyaddr(myIP)[0]
 
resStr=""

for bl in bls:
    try:
        my_resolver = dns.resolver.Resolver()
	my_resolver.nameservers = ['8.8.8.8']
	my_resolver.timeout=5
        query = '.'.join(reversed(str(myIP).split("."))) + "." + bl
        answers = my_resolver.query(query, "A")
        answer_txt = my_resolver.query(query, "TXT")
        print 'IP: %s IS listed in %s (%s: %s)' %(myIP, bl, answers[0], answer_txt[0])
	resStr=resStr + ' IP: %s IS listed in %s (%s: %s)' %(myIP, bl, answers[0], answer_txt[0])+"\n"
    except dns.resolver.NXDOMAIN:
        print 'IP: %s is NOT listed in %s' %(myIP, bl)
    except:
	print 'General DNS error'

if resStr!="":
	sendmessage("info@tritema.ch","info@tritema.ch","ALARM: blacklist "+thisHost,resStr)
