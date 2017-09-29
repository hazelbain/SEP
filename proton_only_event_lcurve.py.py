import protons_range as pr
import protons_range_epam as pre
import let_sector_protons_range as ls
#import let_sector_protons_spec_range as ls_spec
#import let_pitch_protons_spec_range as ls_pitch
import mag_range as mg
#import plastic_range as pl

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import LogLocator
import matplotlib.pylab as pylab
from matplotlib.colors import LogNorm
from matplotlib.font_manager import FontProperties
from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator
from matplotlib.dates import HourLocator
from matplotlib.dates import WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib.dates as mdates
import matplotlib.transforms as transforms
import cPickle as pickle
from brewer2mpl import qualitative

import numpy as np
from datetime import datetime
from copy import copy

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/7.3/lib/python2.7/site-packages/')
import rd_shocks_xls as shks
import rd_magclouds_txt as magcld
import rd_sir_xls as sir
import rd_ace_shocks as ashks



def proton_lcurve_month_plot(plotsmc = 1, res = 'coarse'):

	res = 'coarse'
	plotb=1
	plotsmc=1

	#-------------import the data
	t1 = '4-sep-2017 00:00'
	t2 =  '18-sep-2017 00:00'
	#stereo = 'a'
	tres = 1

	#st = mg.date2doy_decimal(t1)
	#et = mg.date2doy_decimal(t2)
	st = datetime.strptime(t1, "%d-%b-%Y %H:%M")
	et = datetime.strptime(t2, "%d-%b-%Y %H:%M")

	stt, ett = mdates.datestr2num([t1, t2])		# for the imshow plots - convert to value understood by matplotlib
	

	year = datetime.strptime(t1, "%d-%b-%Y %H:%M").year
	month = datetime.strptime(t1, "%d-%b-%Y %H:%M").strftime('%m')

	##time tickmarks to DOY
	# if tick1 != 'None':
	# 	tick1_doy = ls.date2doy_decimal(tick1)
	# if tick2 != 'None':
	# 	tick2_doy = ls.date2doy_decimal(tick2)
	


	if res == 'coarse':
		let_pr_tres = '10'
		het_pr_tres = '15'
		#pla_tres = 10
		#pad_tres = 1
	elif res == 'fine':
		let_pr_tres = '1'
		het_pr_tres = '15'
		#pla_tres = 1
		#pad_tres = 1
	else:
		"Need to define a temporal resoultion (coarse or fine) for the plots"


	####get summed proton lighcurves
	print " "
	print "Getting proton lightcurve data..."
	#LET 1.8 - 10 MeV protons
	let_sum_dates0_a, let_sum_lcurve_a = pr.parse_let_proton_range(t1, t2, 'a', let_pr_tres)
	let_sum_doy0_a = []							#convert dates to doy
	for i in range(len(let_sum_dates0_a)):
		let_sum_doy0_a.append(ls.date2doy_decimal(datetime.strftime(let_sum_dates0_a[i], "%d-%b-%Y %H:%M")))
	mxlet_a = np.max(let_sum_lcurve_a)
	mnlet_a = np.min(let_sum_lcurve_a)
	#HET 14 - 100 MeV protons
	het_sum_dates0_a, het_sum_lcurve_a = pr.het_proton_lcurve_range(t1, t2, 'a', het_pr_tres)
	het_sum_doy0_a = []							#convert dates to doy
	for i in range(len(het_sum_dates0_a)):
		het_sum_doy0_a.append(ls.date2doy_decimal(datetime.strftime(het_sum_dates0_a[i], "%d-%b-%Y %H:%M")))
	mxhet_a = np.max(het_sum_lcurve_a)
	mnhet_a = np.min(het_sum_lcurve_a)
	mxp_a = np.max([mxlet_a, mxhet_a]) 
	mnp_a = np.min([mnlet_a, mnhet_a]) 


	let_sum_dates0_b, let_sum_lcurve_b = pr.parse_let_proton_range(t1, t2, 'b', let_pr_tres)
	let_sum_doy0_b = []							#convert dates to doy
	for i in range(len(let_sum_dates0_b)):
		let_sum_doy0_b.append(ls.date2doy_decimal(datetime.strftime(let_sum_dates0_b[i], "%d-%b-%Y %H:%M")))
	mxlet_b = np.max(let_sum_lcurve_b)
	mnlet_b = np.min(let_sum_lcurve_b)
	#HET 14 - 100 MeV protons
	het_sum_dates0_b, het_sum_lcurve_b = pr.het_proton_lcurve_range(t1, t2, 'b', het_pr_tres)
	het_sum_doy0_b = []							#convert dates to doy
	for i in range(len(het_sum_dates0_b)):
		het_sum_doy0_b.append(ls.date2doy_decimal(datetime.strftime(het_sum_dates0_b[i], "%d-%b-%Y %H:%M")))
	mxhet_b = np.max(het_sum_lcurve_b)
	mnhet_b = np.min(het_sum_lcurve_b)
	mxp_b = np.max([mxlet_b, mxhet_b]) 
	mnp_b = np.max([mnlet_b, mnhet_b]) 

	##epam protons
	epam_dates0, epam_lcurve = pre.parse_epam_proton_range(t1, t2)
	mxepam = np.amax(epam_lcurve)


	###check for shocks observed by STEREO (from the official list)

	tshock_sta, tshock_stb = shks.stereo_shock()			#read in list of shocks
	
	tsa = shks.time_in_range(t1, t2, tshock_sta, dtfmt=1) 
	tsb = shks.time_in_range(t1, t2, tshock_stb, dtfmt=1) 

	

	# tsa_doy = []
	# for i in range(len(tsa)): tsa_doy.append(mg.date2doy_decimal(tsa[i]))
	# tsb_doy = []
	# for i in range(len(tsb)): tsb_doy.append(mg.date2doy_decimal(tsb[i]))

	###check for magnetic clouds
	tmagcloud_sta, tmagcloud_stb = magcld.stereo_magcloud()

	tmca = magcld.trange_in_trange(t1, t2, tmagcloud_sta)
	tmcb = magcld.trange_in_trange(t1, t2, tmagcloud_stb)

	# tmca_doy = []
	# for i in range(len(tmca)): 
	# 	tmca_doy.append( (mg.date2doy_decimal(tmca[i][0]), mg.date2doy_decimal(tmca[i][1]) ))
	# tmcb_doy = []
	# for i in range(len(tmcb)): 
	# 	tmcb_doy.append( (mg.date2doy_decimal(tmcb[i][0]), mg.date2doy_decimal(tmcb[i][1]) ))


	#cfa ace shock list
	ash = ashks.rd_ace_shocks()
	tse = ashks.time_in_range(t1, t2, ash, dtfmt=1)
	tse.append( datetime(2012, 7, 20, 4, 30))

	##ACE magcloud
	#tmce = [(datetime(2010, 8, 3, 3, 0), datetime(2010,8,3,16,0)), (datetime(2010,8,4,4,34), datetime(2010,8,4,10,07)), (datetime(2010,8,4,10,07), datetime(2010,8,5,0,0))]


	##ENLIL shock arrivals
	f = '/Users/hazelbain/Dropbox/sep_archive/enlil/091817_SH_2/22jan12_shock_times.p'
	sha, she, shb = pickle.load( open(f, "rb"))



	
	#------------set up 1x3 figure
	#f, (ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(9, 1, figsize=(7.5,10))
	f, (ax7, ax0, ax77) = plt.subplots(3, figsize=(10,7))

	plt.subplots_adjust(hspace = .25)		# no vertical space between subplots
	#minorLocator   = MultipleLocator(1)	# minor tick mark every 1 of a day
	#labelx = -0.1  							# yaxes label x-coords for alignment
	fontP = FontProperties()				#legend
	fontP.set_size('x-small')

	dateFmt = DateFormatter('%d')
	daysLoc = DayLocator()
	hoursLoc = HourLocator()
	weekLoc = WeekdayLocator(byweekday=SU)


	#---------------------------------------STA-------------------------

	#----LET summed protons - STA

	nl = 10
	xc = 255/nl
	ax7.plot(let_sum_dates0_a, let_sum_lcurve_a[:,0], c = cm.rainbow(1 * xc + 1) ,label='LET 1.8 - 3.6 MeV')
	ax7.plot(let_sum_dates0_a, let_sum_lcurve_a[:,1], c = cm.rainbow(3 * xc + 1) ,label='LET 4 - 6 MeV')
	ax7.plot(let_sum_dates0_a, let_sum_lcurve_a[:,2], c = cm.rainbow(5 * xc + 1) ,label='LET 6 - 10 MeV')
	ax7.plot(het_sum_dates0_a, het_sum_lcurve_a[:,0], c = cm.rainbow(6 * xc + 1) ,label='HET 15 - 24 MeV')
	ax7.plot(het_sum_dates0_a, het_sum_lcurve_a[:,1], c = cm.rainbow(8 * xc + 1) ,label='HET 24 - 40 MeV')
	ax7.plot(het_sum_dates0_a, het_sum_lcurve_a[:,2], c = cm.rainbow(10 * xc + 1) ,label='HET 40 - 60 MeV')
	ax7.xaxis.set_major_formatter(dateFmt)
	ax7.xaxis.set_major_locator(weekLoc)
	ax7.xaxis.set_minor_locator(daysLoc)
	#ax7.set_xticklabels(' ')
	ax7.set_title('STEREO A', loc='Left')
	ax7.set_xlim([st, et])
	ax7.set_yscale('log')
	topa = 5.e4
	ax7.set_ylim(top = topa)
	ax7.set_ylim(bottom = 1.e-4)
	ax7.set_ylabel('H Intensity \n $\mathrm{(cm^{2}\,sr\,s\,MeV)^{-1}}$')
	#ax7.set_xlabel("Start Time "+t1+" (UTC)")
	#ax7.yaxis.set_label_coords(labelx, 0.5)	
	#ax7.yaxis.set_major_locator(LogLocator(numticks = 3)) 
	#ax7.set_xlabel("Start Time "+t1+" (UTC)")
	leg7 = ax7.legend(loc='upper rights', prop = fontP, fancybox=True, bbox_to_anchor=(0.8, 1.35) )
	leg7.get_frame().set_alpha(1.0)
	if plotsmc == 1:
		for i in range(len(tsa)): 
			ax7.axvline(x=tsa[i], linewidth=2, linestyle='solid', color='black')
			ax7.annotate("S"+str(i), xy=(tsa[i], topa), xycoords='data', color='black')
		for i in range(len(tmca)): 
			#ax7.axvline(x=tmca[i][0], linewidth=2, linestyle='--', color='orange')
			#ax7.axvline(x=tmca[i][1], linewidth=2, linestyle='--', color='orange')
			ax7.axvspan(tmca[i][0], tmca[i][1], facecolor='orange', alpha=0.25)
	# if tick1 != 'None':
	# 	ax7.axvline(x=tick1_doy, linewidth=2, linestyle='-', color='red')
	# if tick2 != 'None':
	# 	ax7.axvline(x=tick2_doy, linewidth=2, linestyle='-', color='red')
		
	#plot enlil shock arrival times
	for i in range(len(sha)):
		if isinstance(sha[i]['t1'].item(), float) == False:
			ax7.axvline(x=sha[i]['t1'].item() , linewidth=2, linestyle='--', color='green')
			ax7.annotate("S"+str(i), xy=(sha[i]['t1'].item(), topa), xycoords='data', color='green')

	for i in range(len(sha)):
		if isinstance(sha[i]['ts'].item(), float) == False:
			ax7.axvline(x=sha[i]['ts'].item() , linewidth=2, linestyle='--', color='red')
			# ax7.text( sha[i]['ts'].item() - timedelta(hours=9), 1.05, "S"+str(i+1), transform=trans7, color='red', fontsize=12)
			ax7.annotate("S"+str(i), xy=(sha[i]['ts'].item(), topa), xycoords='data', color='red')



	#----EPAM protons

	nl = 3
	xc = 255/3/nl

	we0 = np.where(epam_lcurve[:,0] != min(epam_lcurve[:,0]))
	we1 = np.where(epam_lcurve[:,1] != min(epam_lcurve[:,1]))
	we2 = np.where(epam_lcurve[:,2] != min(epam_lcurve[:,2]))

	ax0.plot(epam_dates0[we0[0]], epam_lcurve[we0[0],0], c = cm.rainbow(1 * xc + 1) ,label='EPAM 0.540 - 0.765 MeV')
	ax0.plot(epam_dates0[we1[0]], epam_lcurve[we1[0],1], c = cm.rainbow(2 * xc + 1) ,label='EPAM 0.765 - 1.22 MeV')
	ax0.plot(epam_dates0[we2[0]], epam_lcurve[we2[0],2], c = cm.rainbow(3 * xc + 1) ,label='EPAM 1.22 - 4.94 MeV')
	ax0.xaxis.set_major_formatter(dateFmt)
	ax0.xaxis.set_major_locator(weekLoc)
	ax0.xaxis.set_minor_locator(daysLoc)
	#ax0.set_xticklabels(' ')
	ax0.set_title('ACE', loc='Right')
	ax0.set_xlim([st, et])
	ax0.set_yscale('log')
	tope = 1.e5
	ax0.set_ylim(top = tope)
	ax0.set_ylim(bottom = 1.e-2)
	ax0.set_ylabel('H Intensity \n $\mathrm{(cm^{2}\,sr\,s\,MeV)^{-1}}$')
	#ax7.set_xlabel("Start Time "+t1+" (UTC)")
	#ax7.yaxis.set_label_coords(labelx, 0.5)	
	#ax0.yaxis.set_major_locator(LogLocator(numticks = 3)) 
	#ax7.set_xlabel("Start Time "+t1+" (UTC)")
	leg0 = ax0.legend(loc='upper center', prop = fontP, fancybox=True, bbox_to_anchor=(0.8, 1.1) )
	leg0.get_frame().set_alpha(1.0)
	if plotsmc == 1:
	# 	for i in range(len(tmce)): 
	# 		ax0.axvline(x=tmce[i][0], linewidth=2, color='orange')
	# 		ax0.axvline(x=tmce[i][1], linewidth=2, color='orange')
	# 		ax0.axvspan(tmce[i][0], tmce[i][1], facecolor='orange', alpha=0.25)
	 	for i in range(len(tse)): 
	 		ax0.axvline(x=tse[i], linewidth=2, linestyle='solid', color='black')
	 		ax0.annotate("S"+str(i), xy=(tse[i], tope), xycoords='data', color='black')
		
		
	# #plot enlil shock arrival times
	for i in range(len(she)):
		if isinstance(she[i]['t1'].item(), float) == False:
			ax0.axvline(x=she[i]['t1'].item(), linewidth=2, linestyle='--', color='green')
			ax0.annotate("S"+str(i), xy=(she[i]['t1'].item(), tope), xycoords='data', color='green')


	for i in range(len(she)):
		if isinstance(she[i]['ts'].item(), float) == False:
			ax0.axvline(x=she[i]['ts'].item(), linewidth=2, linestyle='--', color='red')
			ax0.annotate("S"+str(i), xy=(she[i]['ts'].item(), tope), xycoords='data', color='red')


	#----LET summed protons - STB

	nl = 10
	xc = 255/nl
	ax77.plot(let_sum_dates0_b, let_sum_lcurve_b[:,0], c = cm.rainbow(1 * xc + 1) ,label='LET 1.8 - 3.6 MeV')
	ax77.plot(let_sum_dates0_b, let_sum_lcurve_b[:,1], c = cm.rainbow(3 * xc + 1) ,label='LET 4 - 6 MeV')
	ax77.plot(let_sum_dates0_b, let_sum_lcurve_b[:,2], c = cm.rainbow(5 * xc + 1) ,label='LET 6 - 10 MeV')
	ax77.plot(het_sum_dates0_b, het_sum_lcurve_b[:,0], c = cm.rainbow(6 * xc + 1) ,label='HET 15 - 24 MeV')
	ax77.plot(het_sum_dates0_b, het_sum_lcurve_b[:,1], c = cm.rainbow(8 * xc + 1) ,label='HET 24 - 40 MeV')
	ax77.plot(het_sum_dates0_b, het_sum_lcurve_b[:,2], c = cm.rainbow(10 * xc + 1) ,label='HET 40 - 60 MeV')
	ax77.xaxis.set_major_formatter(dateFmt)
	ax77.xaxis.set_major_locator(weekLoc)
	ax77.xaxis.set_minor_locator(daysLoc)
	#ax77.set_xticklabels(' ')
	ax77.set_title('STEREO B', loc='Right')
	ax77.set_xlim([st, et])
	ax77.set_yscale('log')
	topb = topa
	ax77.set_ylim(top = topb)
	ax77.set_ylim(bottom = 1.e-4)
	ax77.set_ylabel('H Intensity \n $\mathrm{(cm^{2}\,sr\,s\,MeV)^{-1}}$')
	ax77.set_xlabel("Start Time "+t1+" (UTC)")
	#ax77.yaxis.set_label_coords(labelx, 0.5)	
	#ax77.yaxis.set_major_locator(LogLocator(numticks = 3)) 
	#ax7.set_xlabel("Start Time "+t1+" (UTC)")
	#leg77 = ax77.legend(loc='best', prop = fontP, fancybox=True )
	#leg77.get_frame().set_alpha(0.5)
	if plotsmc == 1:
		for i in range(len(tsb)): 
			ax77.axvline(x=tsb[i], linewidth=2, linestyle='solid', color='black')
			ax77.annotate("S"+str(i), xy=(tsb[i], topb), xycoords='data', color='black')
		for i in range(len(tmcb)): 
			#ax77.axvline(x=tmcb[i][0], linewidth=2, linestyle='--', color='orange')
			#ax77.axvline(x=tmcb[i][1], linewidth=2, linestyle='--', color='orange')
			ax77.axvspan(tmcb[i][0], tmcb[i][1], facecolor='orange', alpha=0.25)

	#plot enlil shock arrival times
	for i in range(len(shb)):
		if isinstance(shb[i]['t1'].item(), float) == False:
			ax77.axvline(x=shb[i]['t1'].item(), linewidth=2, linestyle='--', color='green')
			#ax77.text( shb[i]['t1'].item() - timedelta(hours=6), 1.05, "S"+str(i+1), transform=trans77, color='green', fontsize=12)
			ax77.annotate("S"+str(i), xy=(shb[i]['t1'].item(), topb), xycoords='data', color='green')


	for i in range(len(shb)):
		if isinstance(shb[i]['ts'].item(), float) == False:
			ax77.axvline(x=shb[i]['ts'].item(), linewidth=2, linestyle='--', color='red')
			#ax77.text( shb[i]['ts'].item() - timedelta(hours=6), 1.05, "S"+str(i+1), transform=trans77, color='red', fontsize=12)
			ax77.annotate("S"+str(i), xy=(shb[i]['ts'].item(), topb), xycoords='data', color='red')


	#plt.show()
	plt.savefig('proton_lcurve_22jan12.pdf', format='pdf')



	return None

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    #parser.add_argument('t1', type = str,  help='Starting time for plots')
    #parser.add_argument('t2', type = str,  help='Ending time for plots')
    #parser.add_argument('tick1', type = str, default = 'None',  help='temporal tickmark for plot')
    #parser.add_argument('tick2', type = str, default = 'None', help='temporal tickmark for plot')
    #parser.add_argument('-s', action = 'store_false', default = True, dest = 'plotbkey',  help='Keyword for plotting B')
    #parser.add_argument('res', type = str,  help='fine or coarse temporal resolution')
    #parser.add_argument('stereo', type = str,  help='Which STEREO Spacecraft')
    args = parser.parse_args()

    #if args.plotbkey == False: 
 	#	plotsmc = 1
    #elif args.plotbkey == True:  
	#	plotsmc = 1

    #result = proton_lcurve_month_plot(args.t1, args.t2, plotb = plotsmc, res = arg.res)
    result = proton_lcurve_month_plot()

   








