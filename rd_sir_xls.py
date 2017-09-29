import xlrd
import numpy as np
from datetime import datetime
from numpy import logical_and
import platform

def stereo_sir():

	"""Retrieve shock times from STEREO list"""

	if platform.platform()[0:3] == 'Dar':
		dd = '/Users/hazelbain/'
	elif platform.platform()[0:3] == 'Lin':
		dd = '/home/hbain/'

	filename = dd + 'Dropbox/sep_archive/STEREO_Level3_SIR.xls'

	wb = xlrd.open_workbook(filename)		#open
	sh = wb.sheet_by_index(0)				#get the first sheet
	col0 = np.asarray(sh.col_values(0))
	col2 = np.asarray(sh.col_values(2))
	col3 = np.asarray(sh.col_values(3))
	col4 = np.asarray(sh.col_values(4))

	#split data into years (only 2010 - 2012)
	yrrow = []
	#print col0
	for rw in range(len(col0)):
		if col0[rw][0:3] == '201':
			yrrow.append(rw)


	#loop through years and append year to time
	sta_row_ind = []
	stb_row_ind = []

	sta_st = []
	stb_st = []
	sta_et = []
	stb_et = []

	tsir_sta = []
	tsir_stb = []

	yrrow2 = yrrow
	yrrow2.append(423)		#hard coding end of file 
	for i in range(len(yrrow2)-1):
		#print i
		for j in range(yrrow[i]+2, yrrow[i+1]-2):
			#print j

			if col2[j] == 'A':

				#print 'A'
				sta_row_ind.append(j)

				#i = 0
				#j = 203

				#start time
				st_yr = int(col0[yrrow[i]][0:4])
				if len(col3[j].split(' ')) == 3:
					ind = 0
				elif len(col3[j].split(' ')) == 4:
					ind = 1
				else: 
					print j
				st_mnth = int(col3[j].split(' ')[1 + ind].split('/')[0])
				st_day = int(col3[j].split(' ')[1 + ind].split('/')[1])
				st_hr = int(col3[j].split(' ')[2 + ind].split(':')[0])
				st_mn = int(col3[j].split(' ')[2 + ind].split(':')[1].split('.')[0])
				st = datetime(st_yr, st_mnth, st_day, st_hr, st_mn)
				sta_st.append(st)

				#end time
				et_yr = int(col0[yrrow[i]][0:4])
				if len(col4[j].split(' ')) == 3:					#correct for rows that include prior yr
					ind = 0
				elif len(col4[j].split(' ')) == 4:
					ind = 1
				else: 
					pass
				et_mnth = int(col4[j].split(' ')[1 + ind].split('/')[0])
				et_day = int(col4[j].split(' ')[1 + ind].split('/')[1])
				et_hr = int(col4[j].split(' ')[2 + ind].split(':')[0])
				et_mn = int(col4[j].split(' ')[2 + ind].split(':')[1].split('.')[0])
				et = datetime(et_yr, et_mnth, et_day, et_hr, et_mn)
				sta_et.append(et)

				tsir_sta.append([st, et])
				
			elif col2[j] == 'B':
				#print 'B'

				stb_row_ind.append(j)

				#start time
				st_yr = int(col0[yrrow[i]][0:4])
				if len(col3[j].split(' ')) == 3:					#correct for rows that include prior yr
					ind = 0
				elif len(col3[j].split(' ')) == 4:
					ind = 1
				else: 
					pass
				st_mnth = int(col3[j].split(' ')[1 + ind].split('/')[0])
				st_day = int(col3[j].split(' ')[1 + ind].split('/')[1])
				st_hr = int(col3[j].split(' ')[2 + ind].split(':')[0])
				st_mn = int(col3[j].split(' ')[2 + ind].split(':')[1].split('.')[0])
				st = datetime(st_yr, st_mnth, st_day, st_hr, st_mn)
				stb_st.append(st)

				#end time
				et_yr = int(col0[yrrow[i]][0:4])
				if len(col4[j].split(' ')) == 3:					#correct for rows that include prior yr
					ind = 0
				elif len(col4[j].split(' ')) == 4:
					ind = 1
				else: 
					pass
				et_mnth = int(col4[j].split(' ')[1 + ind].split('/')[0])
				et_day = int(col4[j].split(' ')[1 + ind].split('/')[1])
				et_hr = int(col4[j].split(' ')[2 + ind].split(':')[0])
				et_mn = int(col4[j].split(' ')[2 + ind].split(':')[1].split('.')[0])
				et = datetime(et_yr, et_mnth, et_day, et_hr, et_mn)
				stb_et.append(et)

				tsir_stb.append([st, et])

			else:
				continue


	#sta_st = np.asarray(sta_st)
	#sta_et = np.asarray(sta_et)
	#stb_st = np.asarray(stb_st)
	#stb_et = np.asarray(stb_et)

	#tsir_sta = np.array([sta_st, sta_et])
	#tsir_stb = np.array([stb_st, stb_et])

	return tsir_sta, tsir_stb


def trange_in_trange(t1, t2, tr, dtfmt=0):
	"""Return true if array of time ranges tr is in the time range [t1, t2]"""

	dt1 = datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.strptime(t2, "%d-%b-%Y %H:%M")
	nt = len(tr)

	trange_to_plot = []

	for i in range(nt):

		#determing if any of magcloud timerange is in the range [t1,t2]
		st_in = time_in_range(t1, t2, [tr[i][0]], dtfmt=1)		#is the start of tr in the range [t1,t2]
		et_in = time_in_range(t1, t2, [tr[i][1]], dtfmt=1)		#is the end of tr in the range [t1,t2]

		#print st_in
		#print et_in

		#determine the resulting timerange to plot/shage on sep plots
		if logical_and((not not st_in), (not not et_in)):				#if magcloud trange completely enclosed by [t1,t2]
			trange_to_plot.append((st_in[0], et_in[0]))
		elif st_in:
			trange_to_plot.append((st_in[0], dt2))		#if magcloud trange[0] is in [t1,t2]
		elif et_in:
			trange_to_plot.append((dt1, et_in[0]))		#if magcloud trange[1] is in [t1,t2]
		else:
			continue										#if no magcloud in [t1,t2]


	return trange_to_plot



def time_in_range(t1, t2, x, dtfmt=0):
	"""Return true if array of times x is in the range [t1, t2]"""

	dt1 = datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.strptime(t2, "%d-%b-%Y %H:%M")
	nt = len(x)

	t_in = []
	for i in range(nt):
		if dt1 <= dt2:
			if dt1 <= x[i] <= dt2:

				if dtfmt == 1:
					t_in.append(x[i])

				else:
					t_in.append(datetime.strftime(x[i], "%d-%b-%Y %H:%M"))

		else:
			dt1<= x[i] or x[i] <= dt2

	return t_in












