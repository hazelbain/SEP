from numpy import loadtxt
from numpy import logical_and
from datetime import datetime
import platform


def stereo_magcloud():

	if platform.platform()[0:3] == 'Dar':
		dd = '/Users/hazelbain/'
	elif platform.platform()[0:3] == 'Lin':
		dd = '/home/hbain/'

	file_a = dd + 'Dropbox/sep_archive/stereo_magcloud_sta.txt'
	file_b = dd + 'Dropbox/sep_archive/stereo_magcloud_stb.txt'

	data_a = loadtxt(file_a, dtype='str', delimiter=',') 
	data_b = loadtxt(file_b, dtype='str', delimiter=',') 

	nevents_a = len(data_a[:,0])
	nevents_b = len(data_b[:,0])

	tmagcloud_sta = []
	for i in range(nevents_a): 

		tr1_a = data_a[i][2].strip() +'-'+ data_a[i][1].strip() +'-'+ data_a[i][0] +' '+ data_a[i][3].strip()
		dt1_a = datetime.strptime(tr1_a, "%d-%b-%Y %H:%M")

		tr2_a = data_a[i][5].strip() +'-'+ data_a[i][4].strip() +'-'+ data_a[i][0] +' '+ data_a[i][6].strip()
		dt2_a = datetime.strptime(tr2_a, "%d-%b-%Y %H:%M")

		tmagcloud_sta.append([dt1_a, dt2_a])

	tmagcloud_stb = []
	for i in range(nevents_b): 

		tr1_b = data_b[i][2].strip() +'-'+ data_b[i][1].strip() +'-'+ data_b[i][0] +' '+ data_b[i][3].strip()
		dt1_b = datetime.strptime(tr1_b, "%d-%b-%Y %H:%M")

		tr2_b = data_b[i][5].strip() +'-'+ data_b[i][4].strip() +'-'+ data_b[i][0] +' '+ data_b[i][6].strip()
		dt2_b = datetime.strptime(tr2_b, "%d-%b-%Y %H:%M")

		tmagcloud_stb.append([dt1_b, dt2_b])


	return tmagcloud_sta, tmagcloud_stb



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

		#determine the resulting timerange to plot/shade on sep plots
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

				if dtfmt == 0:
					t_in.append(datetime.strftime(x[i], "%d-%b-%Y %H:%M"))
				else:
					t_in.append(x[i])


		else:
			#dt1<= x[i] or x[i] <= dt28
			continue

	return t_in



