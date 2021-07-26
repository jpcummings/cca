#!/usr/bin/env python

import sys
import argparse
import numpy as np
import pandas as pd

#definition of a class to represent faculty member
class faculty:
	def __init__(self, fname='fname',lname='lname',wl=0,dept='dept',salary=0,rank='none'):
		self.fname = fname.lstrip()
		self.lname = lname.lstrip()
		self.teachWL = wl
		self.dept = dept
		self.salary = salary
		self.rank = 'none'

	def display(self):
		print self.name(), self.dept, self.salary, self.teachWL

	def write_csv_hdr(self):
		print 'fname',',','lname',',','rank',',', 'dept',',','salary',',', 'teachWL'

	def write_csv(self):
		print self.fname,',',self.lname,',', self.rank,',',  self.dept,',', self.salary,',', self.teachWL

	def setrank(self,r):
		self.rank = r
		return self

	def setsalary_to_rank(self):
		if self.rank == 'Professor':
			self.salary = 90000.
		return self

	def sal_per_WLhour(self):
		try:
			spwl = self.salary/self.teachWL
		except ZeroDivisionError:
			print 'error!'
			self.display()
		return spwl

	def setname(self,lcf):
		ln, fn = lcf.split(',')
		self.fname = fn.lstrip()
		self.lname = ln.lstrip()

	def hasname(self,lname,fname):
		if self.lname == lname and self.fname == fname:
			return True
		else:
			return False

	def name(self):
		name=self.fname+' '+self.lname
		return name



# Class for a roster of faculty		
class fac_list:
	def __init__(self):
		self.flist = []
	
	def append(self,f):
		for ff in self.flist:
			if ff.hasname(f.lname, f.fname):
				return self
		self.flist.append(f)
		return self

	def add(self,f):
		for ff in self.flist:
			if ff.hasname(f.lname, f.fname):
				return ff
		self.flist.append(f)
		return f

	def testrank(self):
		for f in self.flist:
			f.setrank('Professor')
			f.setsalary_to_rank()
			f.teachWL = 18.
		return self
		
	def display(self):
		print 'Table of faculty:'
		for f in self.flist:
			f.display()

	def write_csv(self):
		self.flist[0].write_csv_hdr()
		for f in self.flist:
			f.write_csv()

	def fill_table(self,xlfile):
		df = pd.read_excel(xlfile)
		for f in self.flist:
			for i, row in df.iterrows():
#				print 'Comparing:'
#				print f.fname, f.lname
#				print row['fname'], row['lname']
				if row['lname'] == f.lname and row['fname'] == f.fname:
#					print 'FOUND A MATCH!  ', f.fname,' ',f.lname
					f.rank = row['rank']
					f.salary = row['salary']
					f.teachWL = row['teachWL']
			


# Definition of course class to hold record from Brad Dorr's spreadsheet
class course:
	def __init__(self):
		self.termcode = 0
		self.subject = 'none'
		self.ncourse = 0
		self.scheduletype = 'none'
		self.credithours = 0
		self.WLhours = 0
		self.faculty = faculty()
		self.fees = 0
		self.enrollment = 0

	def cost(self):
		return self.WLhours*self.faculty.sal_per_WLhour()

	def display(self):
		print self.termcode, self.subject, self.ncourse, self.scheduletype, self.credithours, self.faculty.name(), self.WLhours, self.enrollment

	def dump(self):
		print self.termcode, self.subject, self.ncourse, self.scheduletype, self.credithours, self.faculty.name(), self.WLhours, self.enrollment

	def set(self,tc,sub,nc,st,ch,wlh,fac,fee,enrl):
		self.termcode = tc
		self.subject = sub
		self.ncourse = nc
		self.scheduletype = st
		self.credithours = ch
		self.WLhours = wlh
		self.faculty = fac
		self.fees = fee
		self.enrollment = enrl
		if self.scheduletype == 'Independent Research' or self.scheduletype == 'Independent Study':
#			print 'setting lwh = 0'
			self.WLhours = 0
		nm = self.faculty.name()
		if nm == 'James Serbalik':
#			print 'setting lwh = 0'
			self.WLhours = 0
		return self


class crs_list:
	def __init__(self):
		self.clist = []
	
	def append(self,c):
		self.clist.append(c)
		return self

	def select_dept(self,dept):
		r = crs_list()
		for c in self.clist:
			if c.subject == dept:
#				print 'appending'
#				c.display()
				r.append(c)
		return r

	def cost(self):
		cc = 0.
		for c in self.clist:
			cc = cc +  c.cost()
		return cc

	def cost_by_class(self):
		cc = 0.
		for c in self.clist:
			c.display()
			print 'cost ', c.cost()
			cc = cc +  c.cost()
		return cc

	def display(self):
		print 'List of courses:'
		for c in self.clist:
			c.display()
	
if __name__ == "__main__":
	classes = []
	faculty_list = fac_list()
	course_list = crs_list()
	
	df = pd.read_excel('SD_Credits_r3.xlsx')
	
	for i, row in df.iterrows():
	#	print row
		fac = faculty()
		fac.setname(row['Faculty'])
		f = faculty_list.add(fac)
		c = course()
		if row['Enrollment']>0:
			c.set(row['TermCode'],row['Subject'],row['Course'],row['ScheduleType'],row['Credits'],row['ScheduleTypeWorkload'],f,row['Fees'],row['Enrollment'])
			course_list.append(c)
	
	#faculty_list.testrank()
	#faculty_list.write_csv()
	faculty_list.fill_table('fac_list.xlsx')
	faculty_list.display()
	
	astr_classes = course_list.select_dept('ASTR')
	astro_cost = astr_classes.cost()
	print 'Astro cost: ', astro_cost
	biol_classes = course_list.select_dept('BIOL')
	print 'Biol cost: ', biol_classes.cost()
	chem_classes = course_list.select_dept('CHEM')
	print 'Chem cost: ', chem_classes.cost()
	csis_classes = course_list.select_dept('CSIS')
	print 'CSIS cost: ', csis_classes.cost()
	enva_classes = course_list.select_dept('ENVA')
	print 'Enva cost: ', enva_classes.cost()
	math_classes = course_list.select_dept('MATH')
	print 'Math cost: ', math_classes.cost()
	phys_classes = course_list.select_dept('PHYS')
	print 'Physics (and Astro) cost: ', phys_classes.cost()+astro_cost
