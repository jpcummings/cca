import xlrd
import numpy as np
from matplotlib import pyplot as plt

import sys

# assumptions

# faculty salaries
salary_assistant = 70000.  # min 62950
salary_associate = 80000. # min 74920
salary_full = 95000.           # min 92900
salary_adjunct = 850. #per credit hour
salary_visitor = 65000. 

benefits_overhead = 1.5
    
assistants = ['Bellis','McColgan','Moustakas','Hassel', # Physics
              'Brookins','Vernooy','Swinton','Goldman','Berke','Springer',#Biology
              'Karr','Deyrup',# Computer Science
              'Fryling','DiTursi','Small',# Computer Science
              'Meierdiercks','Kolozsvary', #Env
              'Javaheri', 'Henry' # Math
              ]
              
associates = ['Finn','Cummings','Vernizzi','Rosenberry', # Physics
              'Memmo-Signor','Mason','Harbison','Byrnes', #Biology
              'Hofstein','Tucker','Moriarty','Barnes',"O'Donnell",'Hughes','Kolonko',#Chemistry
              'Lim','Cotler','Berman','Breimer','Cutler',# Computer Science
              'Ellard', #ENVA
              'Bannon','Krylov',"O'Neill" #Math
              ]

full = ['Coohill','Medsker','Weatherwax', #Physics
        'Woolbright','Angstadt','Helm','Hayden','Wilson','Worthington','Zanetti','Sterne-Marr','LaRow', #Biology
        'Rhoads', # Chemistry
        'Egan','Vandenberg','Horowitz','Flatland','Matthews','Lederman','Yoder', # Computer Science
        'Mangun', 'Dollar','Booker', #Env
        'Kenney', 'Rogers' #Math
       ]

visitors = ['Caldaro','Russell',
           'Rapp', 'Pier','Chaturvedi', #Biology
            'Wos','Barbera','LaGraff','McNamara','Lee','Vanderover','Perry', #Chemistry
            'Liss','Sherman','Mehta','Goldstein','Yates','Todaro', #Computer Science
            'Bogan', #Environmental Science
            'Smitas', 'Cade', #Math
            ]

adjuncts = ['Broder','Gigante', #Physics 
           #Biology
          "O'Brien",#Chemistry
            'Coco','Mendez','Rivituso','Schindler','Baciewicz', #Computer Science
            'Pipino', #ENVA
            'Kiehle','Mazzone' #Math
           ]

# make a dictionary of faculty and rank
nfaculty = len(assistants) + len(associates) + len(full) + len(visitors)
faculty_salaries = np.zeros(nfaculty,'f')
faculty_salaries[0:len(assistants)] = salary_assistant*np.ones(len(assistants))
faculty_salaries[len(assistants):len(assistants)+len(associates)] = salary_associate*np.ones(len(associates))
faculty_salaries[len(assistants)+len(associates):len(assistants)+len(associates)+len(full)] = salary_full*np.ones(len(full))
faculty_salaries[len(assistants)+len(associates)+len(full):] = salary_visitor*np.ones(len(visitors))
salary_dict = dict((a,b) for a,b in zip(assistants+associates+full+visitors,faculty_salaries))

# student numbers
discount_rate = .62   # 2012: 0.488   2013: 0.605  2014: 0.653  2015: 0.628   2016: 0.624  2017: 0.629  
tuition = 32000.
tuition_paid = tuition * (1.-discount_rate)
revenue_per_sch = tuition_paid/30.


department_budget = {'PHYS':35000.,'BIOL':157000.,'CSIS':57000.,'MATH':10000.,'CHEM':68000.,'ENVA':27000.}
sos_budget = 250000.  # includes student workers, phones, etc
saint_center_budget = 1700.

austen_cost_per_sch = {'PHYS':346., 'BIOL':411., 'CHEM':360., 'MATH':286., 'CSIS':320., 'ENVA':353.}
austen_revenue_per_sch = {'PHYS':470., 'BIOL':458., 'CHEM':418., 'MATH':393., 'CSIS':517., 'ENVA':509.}
austen_margin_per_sch = {'PHYS':124., 'BIOL':46., 'CHEM':58., 'MATH':107., 'CSIS':196., 'ENVA':155.}

austen_revenue_total = {'PHYS':  2739528., 'BIOL': 4242220., 'CHEM':  2877539., 'MATH':  2718580., 'CSIS':  4420093. , 'ENVA':  1188391.}
austen_cost_total = {'PHYS':  2013888., 'BIOL':  3809448., 'CHEM':  2478207., 'MATH':  1978206., 'CSIS':  2736747., 'ENVA':  825598.}
austen_margin_total = {'PHYS':  725640., 'BIOL':  432773., 'CHEM':  399332., 'MATH':  740374., 'CSIS':  1683346., 'ENVA':  362793.}

austen_revenue_major = {'PHYS': 1413689., 'BIOL':3836713., 'CHEM': 1880022., 'MATH': 1797148., 'CSIS': 3255046. , 'ENVA': 813680.}
austen_cost_major = {'PHYS': 1546391., 'BIOL': 3660433., 'CHEM': 2080068., 'MATH': 1406732., 'CSIS': 2183568., 'ENVA': 620909.}
austen_margin_major = {'PHYS': -132702., 'BIOL': 176279., 'CHEM': -200046., 'MATH': 390416., 'CSIS': 1071478., 'ENVA': 192771.}




def readScheduleDorr(file,match_string): # for reading F2013-S2015 file from Brad Dorr
    '''
    
    Brad sent a file with contact and credit hours.
    The file contains data for period covered by Austen Group report: Fall 2013 - Spring 2015.
    This function to reads SD_Credits_r1.xlsx
    
    '''
    block=[]
    fac=[]
    credit=[]
    course=[]
    credit_hrs = []
    contact_hrs = []
    enrollment = []
    lab_fee = []
    term = []
    course_number = []
    
    xdat=xlrd.open_workbook(file)
    sheet=xdat.sheet_by_index(0)
    ncol=sheet.ncols
    nrow=sheet.nrows
    # find course index
    for i in range(nrow):
        courseprefix=sheet.cell_value(i,3)

        if courseprefix.startswith(match_string):  
            if float(sheet.cell_value(i,0)) > 201540.: # stop at spring 2015
                break
            # skip Shen Physics
            if sheet.cell_value(i,8).find('Shen') > -1:
                #print 'skipping shen physics in', sheet.cell_value(i,0)
                continue
                
            # skip independent studies
            if sheet.cell_value(i,10).find('Independent') > -1:
                #print 'skipping independent study ',  sheet.cell_value(i,8)
                continue

            # skip tutorials
            if sheet.cell_value(i,10).find('Tutorial') > -1:
                #print 'skipping tutorial ', sheet.cell_value(i,8)
                continue
               
            # skip practicum
            if sheet.cell_value(i,10).find('Practicum') > -1:
                #print 'skipping tutorial ', sheet.cell_value(i,8)
                continue
               
            # skip course with enrollment < 5
            if float(sheet.cell_value(i,9)) < 5.: 
                #print 'skipping low enrollment course ', sheet.cell_value(i,8)
                continue
            
            enrollment.append(sheet.cell_value(i,9))
            course.append(sheet.cell_value(i,3)+sheet.cell_value(i,4))
            course_number.append(sheet.cell_value(i,4))
            term.append(sheet.cell_value(i,1))
            block.append(sheet.cell_value(i,5))
            fac.append(sheet.cell_value(i,14).split(',')[0])
            credit.append(sheet.cell_value(i,6))
            try:
                t = float(sheet.cell_value(i,6))
                credit_hrs.append(sheet.cell_value(i,6))
            except ValueError: # some are blank - use column Student Credit instead
                print 'Using column 13 for credit_hrs',sheet.cell_value(i,3)+sheet.cell_value(i,4),sheet.cell_value(i,2),sheet.cell_value(i,6),sheet.cell_value(i,12)
                
                credit_hrs.append(float(sheet.cell_value(i,12)))
            #if credit_hrs[-1] == 0:
                #print course[-1],' in ',sheet.cell_value(i,0), 'is zero credits.'
            contact_hrs.append(sheet.cell_value(i,11))
                          
            try:
                lab_fee.append(float(sheet.cell_value(i,15)))
            except ValueError:
                #print 'no lab fee ',sheet.cell_value(i,15)
                lab_fee.append(0.)
        #xdat=xlrd.close_workbook(file)
    return block,fac,credit,course,credit_hrs,contact_hrs,enrollment,lab_fee,term,course_number
    


class department:

    def __init__(self,prefix,infile):
        self.prefix = prefix
        if prefix.find('PHYS') > -1: # read file twice to get PHYS and ASTR courses
            block,fac,credit,course,credit_hrs,contact_hrs,enrollment,lab_fee,term,course_number = readScheduleDorr(infile,prefix)
            t = readScheduleDorr(infile,'ASTR')
            self.faculty = np.array((fac + t[1]),'S16')
            self.course = np.array((course + t[3]),'S7')
            try:
                self.credit_hrs = np.array((credit_hrs + t[4]),'f')
            except ValueError:
                print 'Value Error when converting credit_hrs to float'
                print credit_hrs
                sys.exit()
            
            self.contact_hrs = np.array((contact_hrs + t[5]),'f')
            self.enrollment = np.array((enrollment + t[6]),'f')
            self.lab_fee = np.array((lab_fee + t[7]),'f')
            self.term = np.array((term + t[8]),'S11')
            self.course_number = np.array(course_number + t[9],'i')
        else:
            block,fac,credit,course,credit_hrs,contact_hrs,enrollment,lab_fee,term,course_number = readScheduleDorr(infile,prefix)
            self.faculty = np.array((fac),'S16')
            self.course = np.array((course),'S7')
            try:
                self.credit_hrs = np.array((credit_hrs),'f')
            except ValueError:
                print 'Value Error when converting credit_hrs to float'
                print credit_hrs
                sys.exit()
            self.contact_hrs = np.array((contact_hrs),'f')
            self.enrollment = np.array((enrollment),'f')
            self.lab_fee = np.array((lab_fee),'f')
            self.term = np.array((term),'S11')
            self.course_number = np.array(course_number,'i')
        self.upperlevel = self.course_number > 200.
        self.calc_cost()
        self.calc_revenue()
        self.calc_margin()
        self.austen_cost_per_sch = austen_cost_per_sch[self.prefix]
        self.austen_revenue_per_sch = austen_revenue_per_sch[self.prefix]
        self.austen_margin_per_sch = austen_margin_per_sch[self.prefix]
        
        self.austen_cost_total = austen_cost_total[self.prefix]
        self.austen_revenue_total = austen_revenue_total[self.prefix]
        self.austen_margin_total = austen_margin_total[self.prefix]
        
        self.austen_cost_major = austen_cost_major[self.prefix]
        self.austen_revenue_major = austen_revenue_major[self.prefix]
        self.austen_margin_major = austen_margin_major[self.prefix]
    
        
    def calc_cost(self):
        self.cost_per_course = np.zeros(len(self.faculty))
        nhassel = 0
        for i in range(len(self.faculty)):
            #print faculty[i]
            #print salary_dict[self.faculty[i]]
            try:
                if self.faculty[i].find('Hassel') > -1:
                    nhassel += 1
                    if nhassel < 2:
                        self.cost_per_course[i] = salary_dict[self.faculty[i]]/24.*self.contact_hrs[i]*benefits_overhead
                    else:
                        self.cost_per_course[i] = self.contact_hrs[i] * salary_adjunct
                else:
                    self.cost_per_course[i] = salary_dict[self.faculty[i]]/24.*self.contact_hrs[i]*benefits_overhead
        
            except KeyError: # enter here for adjunct faculty
                #print 'Key error for ',i,self.faculty[i]
                #if faculty[i].find('Gig') > -1:
                #    print 'Key error for ', self.faculty[i]
                #else:
                #    print salary_dict[self.faculty[i]]
                #print 'got here!'
                # print self.prefix,': assuming ',self.faculty[i],' is an adjunct professor who teaches ',np.sum(self.contact_hrs[self.faculty == self.faculty[i]]),' contact hrs'
                self.cost_per_course[i] = self.contact_hrs[i]* salary_adjunct# course credit hrs * salary per credit hour
        self.total_cost = np.sum(self.cost_per_course) + department_budget[self.prefix] + sos_budget/6.
        self.cost_per_sch = self.total_cost/np.sum(self.credit_hrs*self.enrollment)
        major_weight = np.sum(self.contact_hrs[self.upperlevel]*self.enrollment[self.upperlevel])/np.sum(self.contact_hrs*self.enrollment)
        self.total_cost_major = np.sum(self.cost_per_course[self.upperlevel]) + department_budget[self.prefix]*major_weight
        self.cost_per_sch_major = self.total_cost_major/np.sum(self.credit_hrs[self.upperlevel]*self.enrollment[self.upperlevel])
    def calc_revenue(self):
        self.revenue_per_course = tuition_paid/30.*self.credit_hrs*self.enrollment + self.lab_fee*self.enrollment
        #print self.prefix
        #print 'revenue_per_course: ', self.revenue_per_course
        #print 'credit_hrs: ', self.credit_hrs
        #print 'enrollment: ', self.enrollment
        self.revenue_per_sch = self.revenue_per_course/(self.enrollment*self.credit_hrs)
        #print 'revenue_per_sch: ', self.revenue_per_sch
        self.total_revenue = np.sum(self.revenue_per_course)
        self.ave_revenue_per_sch = np.sum(self.revenue_per_course)/np.sum(self.enrollment*self.credit_hrs)
        self.revenue_per_sch_major = self.revenue_per_sch[self.upperlevel]
        self.total_revenue_major = np.sum(self.revenue_per_course[self.upperlevel])
        self.total_sch = np.sum(self.credit_hrs*self.enrollment)

    def calc_margin(self):
        self.margin_per_sch = self.revenue_per_sch - self.cost_per_sch
        self.margin_per_course = self.revenue_per_course - self.cost_per_course
        self.total_margin = self.total_revenue - self.total_cost
        self.ave_margin_per_sch = np.sum(self.revenue_per_course - self.cost_per_course)/np.sum(self.enrollment*self.credit_hrs)
        
        self.margin_per_sch_major = self.margin_per_sch[self.upperlevel]
        self.total_margin_major = np.sum(self.margin_per_course[self.upperlevel])

    def print_stats(self):
        print '\n%%%%%%%%%%%%%%%%%%%%%%%'
        print self.prefix
        print '%%%%%%%%%%%%%%%%%%%%%%%'
        print 'average cost per class    = %5.2f'%(np.mean(self.cost_per_course))
        print 'average revenue per class = %5.2f'%(np.mean(self.revenue_per_course))
        print 'average margin per class  = %5.2f'%(np.mean(self.margin_per_course))
        print 'average class size        = %3.1f'%(np.mean(self.enrollment))

    def print_stats_totals(self):
        print '\n%%%%%%%%%%%%%%%%%%%%%%%'
        print self.prefix
        print '%%%%%%%%%%%%%%%%%%%%%%%'
        print 'total revenue = %5.4e'%(self.total_revenue)
        print 'total cost = %5.4e'%(self.total_cost) 
        print 'total margin = %5.4e'%(self.total_margin)
        print 'total student credit hours        = ', self.total_sch
        print 'average class size        = %3.1f'%(np.mean(self.enrollment))

    def print_stats_alt(self):
        print 'dept cost/course rev/course margin/course enrollment'
        print '%s %5.2f %5.2f   %5.2f %3.1f'%(self.prefix,np.mean(self.cost_per_course), 
                                            np.mean(self.revenue_per_course), np.mean(self.margin_per_course),
                                            np.mean(self.enrollment))

    def print_stats_sch(self):
        print 'dept cost/sch rev/sch margin/sch enrollment'
        print '%s   %5.2f  %5.2f     %5.2f       %3.1f'%(self.prefix,np.mean(self.cost_per_sch),self.ave_revenue_per_sch, self.ave_margin_per_sch, np.mean(self.enrollment))

    def compare_austen_header(self):
        print '                     Ours    Austen'
    
    def print_dept(self):
        print '%s'%(self.prefix)

    def compare_austen(self):
        print '   revenue per SCH   %5.1f  %5.1f '%(self.ave_revenue_per_sch,self.austen_revenue_per_sch)
        print '   cost    per SCH   %5.1f  %5.1f '%(self.cost_per_sch,self.austen_cost_per_sch)
        print '   margin  per SCH   %5.1f  %5.1f '%(self.ave_margin_per_sch,self.austen_margin_per_sch)

    def compare_austen_header_total(self):
        print '                              Ours         Austen    Percent Diff'

    def compare_austen_total(self):
        print '   revenue total per 2 year   %5.4e  %5.4e %5.1f'%(self.total_revenue,self.austen_revenue_total,(self.total_revenue-self.austen_revenue_total)/(self.austen_revenue_total)*100)
        print '   cost    total per 2 year   %5.4e  %5.4e %5.1f'%(self.total_cost,self.austen_cost_total,(self.total_cost-self.austen_cost_total)/(self.austen_cost_total)*100)
        print '   margin  total per 2 year   %5.4e  %5.4e %5.1f'%(self.total_margin,self.austen_margin_total,(self.total_margin-self.austen_margin_total)/(self.austen_margin_total)*100)
        print '   margin  as percent of cost  %5.1f       %5.1f '%(self.total_margin/self.total_cost*100,100*self.austen_margin_total/self.austen_cost_total)
        
    def compare_austen_major(self):
        print '   revenue major per 2 year   %5.4e  %5.4e %5.1f'%(self.total_revenue_major,
                                                                  self.austen_revenue_major,
                                                                  (self.total_revenue-self.austen_revenue_major)/(self.total_revenue_major)*100)
        print '   cost    major per 2 year   %5.4e  %5.4e %5.1f'%(self.total_cost_major,
                                                                  self.austen_cost_major,
                                                                  (self.total_cost_major-self.austen_cost_major)/(self.total_cost_major)*100)
        print '   margin  major per 2 year   %5.4e  %5.4e %5.1f'%(self.total_margin_major,
                                                                  self.austen_margin_major,
                                                                  (self.total_margin-self.austen_margin_total)/(self.total_margin_major)*100)
        print '   margin  as percent of cost  %5.1f       %5.1f '%(self.total_margin_major/self.total_cost_major*100,
                                                                   self.austen_margin_major/self.austen_cost_major*100)
        print '   average class size          %5.1f' %(np.mean(self.enrollment[self.upperlevel]))
        
    def compare_austen_major_sch(self):
        print '   revenue per SCH   %5.1f  %5.1f '%(self.revenue_per_sch_major,self.austen_revenue_per_sch)
        print '   cost    per SCH   %5.1f  %5.1f '%(self.cost_per_sch_major,self.austen_cost_per_sch)
        print '   margin  per SCH   %5.1f  %5.1f '%(self.margin_per_sch_major,self.austen_margin_per_sch)

    def initOld(self,prefix,infile):
        self.prefix = prefix
        if prefix.find('PHYS') > -1: # read file twice to get PHYS and ASTR courses
            block,room,fac,credit,course,days,times,credit_hrs,contact_hrs,enrollment,lab_fee = readSchedule(infile,prefix)
            t = readSchedule(infile,'ASTR')
            self.faculty = np.array((fac + t[2]),'S16')
            self.course = np.array((course + t[4]),'S7')
            self.credit_hrs = np.array((credit_hrs + t[7]),'f')
            self.contact_hrs = np.array((contact_hrs + t[8]),'f')
            self.enrollment = np.array((enrollment + t[9]),'f')
            self.lab_fee = np.array((lab_fee + t[10]),'f')
        else:
            block,room,fac,credit,course,days,times,credit_hrs,contact_hrs,enrollment,lab_fee = readSchedule(infile,prefix)
            self.faculty = np.array((fac),'S16')
            self.course = np.array((course),'S7')
            self.credit_hrs = np.array((credit_hrs),'f')
            self.contact_hrs = np.array((contact_hrs),'f')
            self.enrollment = np.array((enrollment),'f')
            self.lab_fee = np.array((lab_fee),'f')
        self.calc_cost()
        self.calc_revenue()
        self.calc_margin()
        self.austen_cost_per_sch = austen_cost_per_sch[self.prefix]
        self.austen_revenue_per_sch = austen_revenue_per_sch[self.prefix]
        self.austen_margin_per_sch = austen_margin_per_sch[self.prefix]
        


infile = 'SD_Credits_r3_finn.xlsx' # had to change some blanks in student credit hrs for PHYS 470 & 472
phys = department('PHYS',infile)
bio = department('BIOL',infile)
chem = department('CHEM',infile)
math = department('MATH',infile)
cs = department('CSIS',infile)
enva = department('ENVA',infile)

depts = [phys, bio, chem, math, cs, enva]

for d in depts:
    print d.print_stats_alt()

for d in depts:
    print d.print_stats_totals()


# compare revenue, cost and margin per student credit hour
depts[0].compare_austen_header()
for d in depts:
    d.print_dept()
    d.compare_austen()


# compare revenue, cost and margin per student credit hour
depts[0].compare_austen_header_total()
for d in depts:
    d.print_dept()
    d.compare_austen_total()

