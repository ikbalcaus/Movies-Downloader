from flask import *
import os, waitress, requests, bs4, webbrowser


app = Flask(__name__)


@app.route("/")
def indexRoute():
	if request.args.get("movie"):
		url = "https://www.1377x.to/search/" + request.args.get("movie") + "/1/"
	else:
		url = "https://www.1377x.to/popular-movies"
	doc = bs4.BeautifulSoup(requests.get(url).text, "html.parser")

	name = []
	href = []
	seeds = []
	leeches = []
	size = []
	uploader = []

	for tr in doc.find("table", class_="table-list table table-responsive table-striped").tbody.find_all("tr")[:20]:
		name.append(tr.find_all("a")[1].string)
		href.append(tr.find_all("a")[1]["href"])
		seeds.append(tr.find_all("td")[1].string)
		leeches.append(tr.find_all("td")[2].string)
		size.append(tr.find_all("td")[4].string)
		uploader.append(tr.find_all("td")[5].a.string)
	zipped = zip(name, href, seeds, leeches, size, uploader)
	return render_template("index.html",
		zipped = zipped
	)


@app.route("/movie/<link>")
def movieRoute(link):
	url = "https://www.1377x.to/" + link.replace("~~~", "/")
	doc = bs4.BeautifulSoup(requests.get(url).text, "html.parser")
	magnet_link = doc.find("a", class_="l3426749b3b895e9356348e295596e5f2634c98d8 la1038a02a9e0ee51f6e4be8730ec3edea40279a2 l0d669aa8b23687a65b2981747a14a1be1174ba2c")["href"]
	webbrowser.open_new_tab(magnet_link)
	return redirect("/")


@app.errorhandler(404)
def error(error):
	return redirect("/")


@app.errorhandler(500)
def error(error):
	return redirect("/")


if __name__ == "__main__":
	waitress.serve(app, host="0.0.0.0", port=80)