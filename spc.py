#!/usr/bin/env python

import sys, getopt
import numpy as np
import pandas as pd

N_s = 3000.
n_student_sections = 3000*10.
Nbar = 21.
baseline = 0.
delta = False
scan_size = False



def get_f(d):
	b = d.values[1]
	return b

def get_f_fte(d):
	b = d.values[0]
	return b

def get_c(d):
	c = get_salary(d) + get_benefits(d)
	return c

def get_salary(d):
	s = d.values[2]
	return s

def get_benefits(d):
	b = d.values[2]*0.40 
	return b

def modify_pd_release(d,percent):
	print d.values[0]
	print d.values[0][3]
	print  (75*24-776+387*percent)/(75*24)
	d.values[0][3] = (75*24-776+387*percent)/(75*24)
	print d
	return d

def cost(f,c,f_fte,N_s,Nbar, debug=False):
	sections_per_student = 10.0
	sections_per_fte = 8.0
	if debug:
		print "sections_per_student: ", sections_per_student
		print "sections_per_fte: ", sections_per_fte
		print "N_s: ", N_s
		print "Nbar: ", Nbar
		print "(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar
		print "f: ",f
		print "f_fte ", f_fte
		print "c: ", c
		print "(f*c/f_fte): ", (f*c/f_fte)
	C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
	return np.sum(C)

def nfac(f,c,f_fte,N_s,Nbar, debug=False):
	# this function returns the number of faculty (bodies - except adjuncts) by ran//k.
	sections_per_student = 10.0
	sections_per_fte = 8.0
	if debug:
		print "N_s: ", N_s
		print "Nbar: ", Nbar
		print "f: ",f
		print "f_fte ", f_fte
		print "c: ", c
	nfac = (f/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
	return nfac

def nfac_fte(f,c,f_fte,N_s,Nbar, debug=False):
	# this function returns the number of faculty (bodies - except adjuncts) by ran//k.
	sections_per_student = 10.0
	sections_per_fte = 8.0
	if debug:
		print "N_s: ", N_s
		print "Nbar: ", Nbar
		print "f: ",f
		print "f_fte ", f_fte
		print "c: ", c
	nfac = (f)*(sections_per_student/sections_per_fte)*N_s/Nbar
	return nfac

def cost_constFTE(f,c,f_fte,N_s,N_fte):
	Nbar = (N_s/N_fte)*(10./8.)
	c = cost(f,c,f_fte,N_s,Nbar)
	return np.sum(c)


def display_rank(n):
	ad = n[0]+n[6]+n[12]
	vi = n[1]+n[2]+n[7]+n[8]+n[13]+n[14]
	ast =  n[3]+n[9]+n[15]
	asc =   n[4]+n[10]+n[16]
	fp =  n[5]+n[11]+n[17]
	print ('adjunct, visitor, assistant, associate, full')
	print ('%.2f, %.2f,  %.2f,  %.2f, %.2f' % (ad,vi,ast,asc,fp))


def n_fte(stud_sect,sect_size):
	n_sections = stud_sect/sect_size
	return n_sections/8.

def main(argv):
	inputfile = 'fac_dat.xlsx'
	outputfile = ''
	N_s = 3000.0
	Nbar = 21
	constFTE = False
	debug = False
	numfac = False
	numfte = False


	try:
		opts, args = getopt.getopt(argv,"hdnei:m:s:f:",["ifile=","ofile=", "--nfte"])
	except getopt.GetoptError:
		print 'spc.py -i <inputfile> -m Nbar -s N_s -f n_fte -n -e -d'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'spc.py -i <inputfile> -m Nbar -s N_s -f n_fte -n -e -d'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-m"):
			Nbar = float(arg)
		elif opt in ("-s"):
			N_s = float(arg)
		elif opt in ("-f"):
			N_fte = float(arg)
			constFTE = True
		elif opt in ("-d"):
			debug = True
		elif opt in ("-n"):
			numfac = True
		elif opt in ("-e", "--nfte"):
			numfte = True

	df = pd.read_excel(inputfile)

	f_fte = get_f_fte(df)
	f = get_f(df)
	c = get_c(df)

	if constFTE:
		cc = cost_constFTE(f,c,f_fte,N_s,N_fte)
	else:
		cc = cost(f,c,f_fte,N_s,Nbar,debug)

	print('%.2f' % cc)

	if numfac:
		nfaculty = nfac(f,c,f_fte,N_s,Nbar,debug)
		display_rank(nfaculty)

	if numfte:
		nfaculty_fte = nfac_fte(f,c,f_fte,N_s,Nbar,debug)
		display_rank(nfaculty_fte)

if __name__ == "__main__":
	main(sys.argv[1:])

