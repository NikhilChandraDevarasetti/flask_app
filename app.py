from flask import Flask, request
from elasticsearch import Elasticsearch
from flask_ngrok import run_with_ngrok
import json

app = Flask(__name__)
run_with_ngrok(app)

es_client = Elasticsearch("http://elastic:zWyJXAMxgPIuVXBBYxpC@localhost:9200")


@app.route('/' , methods=[ "GET" , "POST" ])
def index() :
    q = request.args.get("q")  # for GET method
    g = request.args.get("g")
    l = request.args.get("l")

    # q = request.form.get("q")  # for POST method

    one_or_more = [
                        {"multi_match" : {"query" : q , "fields" : "director_name", "fuzziness": 2}},
                        {"multi_match" : {"query" : g , "fields" : "genres" , "fuzziness" : 2}} ,
                        {"multi_match" : {"query" : l , "fields" : "language" , "fuzziness" : 2}}
                    ]

    if q is not None and g is None and l is None :

        body = {
            "_source" : ["director_name", "movie_title", "genres", "language"],
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : [one_or_more[0]],
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-1" : {
                    "text" : q ,
                    "term" : {
                        "field" : "director_name"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res['hits']['hits']
        resp = [each['_source'] for each in hits]
        return json.dumps(resp)

    elif q is None and g is not None and l is None:
        body = {
            "_source" : ["director_name", "genres", "language", "movie_title"],
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : [one_or_more[1]],
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-2" : {
                    "text" : g ,
                    "term" : {
                        "field" : "genres"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    elif q is None and g is None and l is not None :

        body = {
            "_source" : [ "director_name" , "genres" , "language" , "movie_title" ] ,
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : [ one_or_more[2] ] ,
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    elif q is not None and g is not None and l is None :

        body = {
            "_source" : [ "director_name" , "genres" , "language" , "movie_title" ] ,
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : one_or_more[0:2] ,
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-1" : {
                    "text" : q ,
                    "term" : {
                        "field" : "director_name"}
                } ,
                "my-suggest-2" : {
                    "text" : g ,
                    "term" : {
                        "field" : "genres"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    elif q is None and g is not None and l is not None :

        body = {
            "_source" : [ "director_name" , "genres" , "language" , "movie_title" ] ,
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : one_or_more[1:],
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-2" : {
                    "text" : g ,
                    "term" : {
                        "field" : "genres"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    elif q is not None and g is None and l is not None :

        body = {
            "_source" : [ "director_name" , "genres" , "language" , "movie_title" ] ,
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : [ one_or_more[0], one_or_more[2] ] ,
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-1" : {
                    "text" : q ,
                    "term" : {
                        "field" : "director_name"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    elif q is not None and g is not None and l is not None :

        body = {
            "_source" : [ "director_name" , "genres" , "language" , "movie_title" ] ,
            "size" : 10 ,
            "query" : {
                "bool" : {
                    "must" : one_or_more,
                    "filter" : [
                        {"range" : {"imdb_score" : {"gte" : "5.0"}}}
                    ] ,
                    "should" : [
                        {"match" : {"language" : "hindi"}} ,
                        # {"match" : {"genres" : "comedy"}},
                        {"match" : {"language" : "english"}}
                    ] ,
                    "must_not" : [ ]
                }
            } ,
            "suggest" : {
                "my-suggest-1" : {
                    "text" : q ,
                    "term" : {
                        "field" : "director_name"}
                } ,
                "my-suggest-2" : {
                    "text" : g ,
                    "term" : {
                        "field" : "genres"}
                }
            }
        }

        res = es_client.search(index='movies' , body=body)

        hits = res[ 'hits' ][ 'hits' ]
        resp = [ each[ '_source' ] for each in hits ]
        return json.dumps(resp)

    else: # return render_template('index.html')
        return "enter query"


if __name__ == "__main__" :
    app.run(debug=True)
