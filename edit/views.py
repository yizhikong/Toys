from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def edit(request):
    if request.method == 'GET':
        return render_to_response('edit.html', {})
    return HttpResponse(request.POST['editContent'])

def upload(request):
    if request.method == 'POST':
        pics = request.FILES.getlist('pictures')
        picUrlList = '<p>success to upload! The urls of the pictures are as follow:</p>'
        for pic in pics:
            saveFile = open('/savePath/' + pic.name,'wb+')
            picUrlList += '<p>localhost:8000/' + pic.name + '</p>'
            for chunk in pic.chunks():
                saveFile.write(chunk)
            saveFile.close()
        picUrlList += ''
        return HttpResponse('<script>window.parent.urls("%s");</script>' % picUrlList)
