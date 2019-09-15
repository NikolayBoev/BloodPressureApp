from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bokeh.plotting import figure, output_file, show 
from bokeh.resources import CDN
from bokeh.embed import components

from .models import BloodPressure, statistics
from django.http import HttpResponseRedirect
import datetime

def summary ():
	import pandas as pd
	bp = BloodPressure.pdobjects.all()
	df = bp.to_dataframe()
	describe = df.describe()
	statistics.objects.all().delete()
	ii = 0
	while ii < describe.shape[0]:
		Item = statistics(name=describe.index[ii],topNumber=describe.topNumber[ii], bottomNumber=describe.bottomNumber[ii], puls=describe.puls[ii])
		Item.save()
		ii += 1
	return statistics.objects.all()
# Creating histogram of the measured data
def create_histgram (data, y_label):
	import numpy as np
	import scipy.special
	TOOLS="hover"
	hist, edges = np.histogram(data, density=True, bins=50)
	x = np.array(data)
	mu, sigma = 0, 0.5
	pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
	cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2
	
	plot = figure(tools=TOOLS, plot_width=1400, plot_height=400, background_fill_color="#fafafa")
	plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)
	#plot.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")
	#plot.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

	plot.y_range.start = 0
	plot.legend.location = "center_right"
	plot.legend.background_fill_color = "#fefefe"
	plot.xaxis.axis_label = 'x'
	plot.yaxis.axis_label = y_label
	plot.grid.grid_line_color="white"
	return components(plot, CDN)
def index(request): #the index view
	bp = BloodPressure.objects.all() #quering all items with the object manager
	if request.method == "POST": #checking if the request method is a POST
		if "itemAdd" in request.POST: #checking if there is a request to add a item
			topNumber = int(request.POST["topNumber"]) #titletitle = request.POST["description"] #title
			if topNumber > 180 or topNumber < 90:
				pass
			bottomNumber = int(request.POST["bottomNumber"]) #bottomNumber
			if bottomNumber > 110 or bottomNumber < 50:
				pass
			puls = int(request.POST["puls"]) #puls
			if puls > 150 or puls < 50:
				pass
			date = str(request.POST["DateTime"]) #date
			# Validating the date, if the user doesnt define a date, the now will be taken
			if date == '':
				now = datetime.datetime.now()
				date = str(now)[:10]
				print ('date:', date)
			created_time = str(request.POST["Time"]) #time
			# Validating the time, if the user doesnt define a tme, the now will be taken
			if created_time == '17:00':
				now = datetime.datetime.now()
				created_time = str(now)[11:16]
				print ('created_time:', created_time)
			content = str(topNumber) + str(bottomNumber) + str(puls) + " -- " + str(date) #conten
			Item = BloodPressure(topNumber=topNumber, bottomNumber=bottomNumber, puls=puls, created=date, created_time=created_time)
			Item.save() #saving the Item 
			return redirect("/") #reloading the page
		if "itemDelete" in request.POST: #checking if there is a request to delete a item
			checkedlist = request.POST.getlist('checkedbox')
			for GroceryList_id in checkedlist:
				try:
					item = BloodPressure.objects.get(id=int(GroceryList_id)) #getting item id
					item.delete() #deleting item
				except BloodPressure.DoesNotExist:
					item = None
		if "Data" in request.POST: # redirecting to Data
			#print ('wwwww')
			return redirect('/data')
		if "plotData" in request.POST:# redirecting Plot Data
			return redirect('/plots_bokeh')
			
	return render(request, "index.html", {"bp": bp})
# The requst of Data button
def data (request):
	import pandas as pd
	statistic = summary()
	bp = BloodPressure.objects.all()
	if request.method == "POST":
		if "ExportToCsv" in request.POST:
			bp = BloodPressure.pdobjects.all()
			df = bp.to_dataframe()
			df.to_csv(path_or_buf='data.csv', index=False)
		if "ExportToExcel" in request.POST:
			bp = BloodPressure.pdobjects.all()
			df = bp.to_dataframe()
			df.to_excel('data.xlsx', sheet_name='dataBlutPressure', index = False)
	return render(request, "data.html", {"bp": bp, "statistic": statistic})
# The requst of Plot Data button
def plots_bokeh(request):
	bp = BloodPressure.pdobjects.all()
	df = bp.to_dataframe()
	TOOLS="hover"
	plot = figure(tools=TOOLS, plot_width=400, plot_height=400, background_fill_color="#fafafa")
	plot.xaxis.axis_label = "DIA [mmHg]"
	plot.yaxis.axis_label = "SYS [mmHg]"
	plot.circle(df['bottomNumber'], df['topNumber'], color='red', fill_alpha=0.2, size=10)
	script, div = components(plot, CDN)
	
	import pandas as pd
	bp = BloodPressure.pdobjects.all()
	df = bp.to_dataframe()
	script_histogram_topNumber, div_histogram_topNumber = create_histgram(df['topNumber'], 'SYS [mmHg]')
	script_histogram_buttomNumber, div_histogram_buttomNumber = create_histgram(df['bottomNumber'], 'DIA [mmHg]')
	script_histogram_Puls, div_histogram_Puls = create_histgram(df['puls'], 'Puls [1/min]')
	statistic = summary()
	return render(request, "plots_bokeh.html", {"the_script": script, "the_div": div, 
		"statistic": statistic, "script_histogram_topNumber":script_histogram_topNumber, "div_histogram_topNumber":div_histogram_topNumber,
		"script_histogram_buttomNumber":script_histogram_buttomNumber, "div_histogram_buttomNumber":div_histogram_buttomNumber, 
		"script_histogram_Puls":script_histogram_Puls, "div_histogram_Puls":div_histogram_Puls})
def validate_even(value):
	if value % 2 != 0:
		raise ValidationError(_('%(value)s is not an even number'),params={'value': value},)