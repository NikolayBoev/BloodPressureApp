from django.shortcuts import render, redirect, render_to_response

from bokeh.plotting import figure, output_file, show 
from bokeh.resources import CDN
from bokeh.embed import components

from .models import BloodPressure
from django.http import HttpResponseRedirect

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
			print (bottomNumber, bottomNumber)
			Item.save() #saving the Item 
			return redirect("/") #reloading the page

		if "itemDelete" in request.POST: #checking if there is a request to delete a item
			checkedlist = request.POST.getlist('checkedbox')
			print (checkedlist)
			#checkedlist.append(request.POST["checkedbox"]) #checked items to be deleted
			for GroceryList_id in checkedlist:
				try:
					item = BloodPressure.objects.get(id=int(GroceryList_id)) #getting item id
					item.delete() #deleting item
				except BloodPressure.DoesNotExist:
					item = None
		if "Data" in request.POST:
			print ('wwwww')
			return redirect('/data')
		if "plotData" in request.POST:
			return redirect('/plots_bokeh')
			
	return render(request, "index.html", {"bp": bp})
def data (request):
	bp = BloodPressure.objects.all()
	return render(request, "data.html", {"bp": bp})
	
def plots_bokeh(request):
	bp = BloodPressure
	i = 0
	x,y = [], []
	while i < 20:
		try:
			item = BloodPressure.objects.get(id=i) #getting item id
			print (item.topNumber)
			y.append (item.topNumber)
			x.append (item.bottomNumber)
		except BloodPressure.DoesNotExist:
			item = None
		i += 1
	TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
	plot = figure(tools=TOOLS)
	plot.scatter(x, y)
	script, div = components(plot, CDN)
	return render(request, "plots_bokeh.html", {"the_script": script, "the_div": div})
	
	
	
	
	
	
	
	
	
	