from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bokeh.plotting import figure, output_file, show 
from bokeh.resources import CDN
from bokeh.embed import components

from .models import BloodPressure, statistics
from django.http import HttpResponseRedirect

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
def create_histgram (data, y_label):
	import numpy as np
	import scipy.special
	
	hist, edges = np.histogram(data, density=True, bins=50)
	x = np.array(data)
	mu, sigma = 0, 0.5
	pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
	cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2
	
	plot = figure(tools='', plot_width=1400, plot_height=400, background_fill_color="#fafafa")
	plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)
	plot.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")
	plot.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

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
			topNumber = request.POST["topNumber"] #titletitle = request.POST["description"] #title
			bottomNumber = request.POST["bottomNumber"] #bottomNumber
			puls = request.POST["puls"] #puls
			date = str(request.POST["DateTime"]) #date
			content = topNumber + bottomNumber + puls + " -- " + date #conten
			Item = BloodPressure(topNumber=topNumber, bottomNumber=bottomNumber, puls=puls, created=date)
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
		if "Data" in request.POST:
			#print ('wwwww')
			return redirect('/data')
		if "plotData" in request.POST:
			return redirect('/plots_bokeh')
			
	return render(request, "index.html", {"bp": bp})
def data (request):
	statistic = summary()
	bp = BloodPressure.objects.all()
	return render(request, "data.html", {"bp": bp, "statistic": statistic})
def plots_bokeh(request):
	bp = BloodPressure.pdobjects.all()
	df = bp.to_dataframe()
	TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
	plot = figure(tools=TOOLS, plot_width=400, plot_height=400, background_fill_color="#fafafa")
	plot.square(df['topNumber'], df['bottomNumber'], size=10)
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