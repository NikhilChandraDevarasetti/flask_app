from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es_client = Elasticsearch("http://elastic:zWyJXAMxgPIuVXBBYxpC@localhost:9200")
# es_client = Elasticsearch()

# body = {"size": 100, "query": {"match_all": {"name": 'q'}}}

@app.route('/', methods=["GET", "POST"])
def index():

	#q = request.args.get("q") #for GET method
	q = request.form.get("q") # for POST method

	if q is not None:

		res = es_client.search(index='movies', body= {"size": 2, "query": {"match": {"director_name": q}}}) # {"query": {"prefix": {"name": q}}}
		return render_template('index.html', q=q, response=res)

	return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=True)