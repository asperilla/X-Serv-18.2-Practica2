from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .models import Urls

def devuelve_urls(urls_guardadas):
	urls = "<ul>"
	for key in urls_guardadas:
		url_acortada = '<a href=' + "http://localhost:8000" + key.url_acortada + '>' + key.url_acortada + '</a>'
		url_larga = '<a href=' + key.url_completa + '>' + key.url_completa + '</a>'
		urls += (url_acortada + " --> " + url_larga + "<br>")
	return urls

@csrf_exempt
def urls(request, recurso):

	recurso = request.path
	urls_guardadas = Urls.objects.all()

	formulario = """
		<form action="" method="POST">
		Url:<br>
		<input type="text" name="url" value=""><br>
		<input type="submit" value="Acortar">
		</form>
		"""
	
	if request.method == "GET":
		if recurso == "/":
	
			respuesta = devuelve_urls(urls_guardadas)
			return HttpResponse("<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + "<br>" + 								 									respuesta + '</html>')
		else:
			try:
				identificador = recurso.split('/')[1]
				objeto = Urls.objects.get(id=int(identificador))
				url_to_redirect = objeto.url_completa
				return HttpResponseRedirect(url_to_redirect)
			except Urls.DoesNotExist:
				return HttpResponse("No existe esta url")


	if request.method == "POST":
		request_body = request.body.decode('utf-8')
		url_a_acortar = request_body.split('=')[1]
		
		if url_a_acortar == "":
			respuesta = "ERROR. Introduce una url"
			return HttpResponse("<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + "<br>" + 								  	respuesta + '</html>')
	
		if (url_a_acortar.find("http%3A%2F%2F") == 0) or (url_a_acortar.find("https%3A%2F%2F") == 0):
			url = url_a_acortar.split("%3A%2F%2F")[0] + "://" + url_a_acortar.split("%3A%2F%2F")[1]

		else:
			url = "http://" + url_a_acortar
	

		if Urls.objects.filter(url_completa=url):
			respuesta = devuelve_urls(urls_guardadas)
			return HttpResponse("<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + "<br>" + 									respuesta + '</html>')

		else:
			num_url_acortada = Urls.objects.count() + 1
			num_str = str(num_url_acortada)
			url_corta = "/" + num_str

			b = Urls(url_acortada = url_corta, url_completa = url)
			b.save()
			respuesta = devuelve_urls(urls_guardadas)
			return HttpResponse("<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + "<br>" + 									respuesta + '</html>')
		
	
