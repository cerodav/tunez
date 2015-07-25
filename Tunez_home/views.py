from django.shortcuts import render
from django.http import HttpResponse
from .models import result,userquery
from .Tunez_inner import Tunez_inner
import re

def home(request):
	results=result.objects.all()
	t=Tunez_inner("nothingmuch")
	results=Tunez_inner.topsearches(t)
	context={'topsearch':results}
	return render(request,'Tunez_home/home.html',context)

def searchrequest(request):
	if request.POST['query']:
		search_tag=request.POST['query']
		t=Tunez_inner(search_tag)
		collection=Tunez_inner.search(t,search_tag)
	else:
		return render(request, 'Tunez_home/home.html', {
            'error_message': "No query entered",
        })

	q=userquery(query_content=search_tag)
	q.save()
	n=len(collection)
	for i in range(n):
		info=collection[i]['info']

		re_compile=re.compile('[0-9]* kbps')
		quality_string=re_compile.findall(info);
		re_compile=re.compile('\d+')
		if quality_string:
			quality_val=re_compile.findall(quality_string[0])
			quality_val=quality_val[0]
		else:
			quality_val=" "

		re2_compile=re.compile('[0-9]*:[0-9]*')
		duration_val=re2_compile.findall(info)
		if duration_val:
			duration_val=duration_val[0]
		else:
			duration_val=" "

		re3_compile=re.compile('[0-9]*.[0-9]* mb')
		size=re3_compile.findall(info)
		if size:
			size_val=size[0]
		else:
			size_val=" "

		q.result_set.create(title=collection[i]['title'],duration=duration_val,quality=quality_val,size=size_val,url=collection[i]['url'],downloaded=0)

	return render(request, 'Tunez_home/home.html', {
            'results': q.result_set.all(), 'search_tag_term':q.query_content
        })

def empty(value):
    try:
        value = float(value)
    except ValueError:
        pass
    return bool(value)

def albumart(request):
	if request.POST['title']:
		url=request.POST['url'];
		title=request.POST['title'];
		qlty=request.POST['qlty'];
		dura=request.POST['dura'];
		fsize=request.POST['fsize'];
		titlecopy=title
		pat1=re.compile('[0-9a-zA-z ]* -')
		pat2=re.compile('- [0-9a-zA-z ]* -')
		pat3=re.compile('[0-9a-zA-z ]* mp3')
		patmain=re.compile('[0-9a-zA-z ]*')

		pat1res=pat1.findall(titlecopy) #only one result
		pat2res=pat2.findall(titlecopy) #can have more than one result
		pat3res=pat3.findall(titlecopy) #only one result

		t=Tunez_inner("albumart");
		mainres=[]

		for tag in pat1res:
			tag=patmain.findall(tag);
			res1=Tunez_inner.albumart(t,tag[0])
			if res1:
				mainres.extend(res1)	

		for tag in pat2res:
			tag=patmain.findall(tag);
			res2=Tunez_inner.albumart(t,tag[0])
			if res2:
				mainres.extend(res2)

		for tag in pat3res:
			tag=patmain.findall(tag);
			tag=tag[0].replace(' mp3','')
			res3=Tunez_inner.albumart(t,tag)
			if res3:
				mainres.extend(res3)

		#Tunez_inner.download(t,url,title+".mp3")
		context={'albumart':mainres,'audiourl':url,'audiotitle':title,'audioquality':qlty,'audioduration':dura,'audiosize':fsize}
		return render(request,'Tunez_home/download.html',context)
	else:
		return render(request, 'Tunez_home/home.html', {
            'error_message': "No query entered",
        })
def artdownload(request):
	url=request.POST['url'];
	title=request.POST['title'];
	t=Tunez_inner("albumart");
	Tunez_inner.download(t,url,title+".jpeg")
	Tunez_inner.joinartmusic(t,title+".mp3",title+".jpeg")

	context={'successreport':"Successfuly downloaded the requested audio"}
	return render(request,'Tunez_home/home.html',context)












