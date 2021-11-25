from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET', 'POST'))
def search():
    search_type = "keyword"
    search_terms = ""
    films = ""
    awards = ""
    roles = []
    results = []
    spell_suggestion = ""
    show = ""
    es = Elasticsearch('http://localhost:9200')
    if request.method == 'POST':
        search_type = request.form["search-type"]
        search_terms = request.form["search-terms"]
        films = request.form["films"]
        awards = request.form["awards"]
        roles = request.form["roles[]"].split(",")

        if search_type == "phrase" or len(films) or len(awards) or len(roles):
            show = "show"
        
        body = {}
        must = []
        if search_terms and "*" not in search_terms:
            if search_type == "keyword":
                query = {
                    "multi_match" : {
                        "query" : search_terms,
                        "fields" : ["name^2", "real_name^2", "bio", "films.title", "awards.title", "awards.instituition"]
                    }
                }
            elif search_type == "phrase":
                query = {
                    "multi_match" : {
                        "query" : search_terms,
                        "type" : "phrase",
                        "fields" : ["name^2", "real_name^2", "bio", "films.title", "awards.title", "awards.instituition"]
                    }
                }
            must.append(query)
        elif search_terms and "*" in search_terms:
            query = {
                "dis_max": {
                    "queries": [
                        {"wildcard" : { "name" : {"value" : search_terms}}},
                        {"wildcard" : { "real_name" : {"value" : search_terms}}},
                        {"wildcard" : { "bio" : {"value" : search_terms}}},
                        {"wildcard" : { "films.title" : {"value" : search_terms}}},
                        {"wildcard" : { "awards.title" : {"value" : search_terms}}},
                        {"wildcard" : { "awards.instituition" : {"value" : search_terms}}}
                    ]
                }
            }
            must.append(query)
        if films and "*" not in films:
            query = {
                "match" : {
                    "films.title.keyword": films
                }
            }
            must.append(query)
        elif films and "*" in  films:
            query = {
                "dis_max": {
                    "queries": [
                        {"wildcard" : { "films.title" : {"value" : films}}},
                    ]
                }
            }
            must.append(query)
        if awards and "*" not in awards:
            query = {
                "multi_match" : {
                    "query" : awards,
                    "fields" : ["awards.title", "awards.instituition"]
                }
            }
            must.append(query)
        elif awards and "*" in awards:
            query = {
                "dis_max": {
                    "queries": [
                        {"wildcard" : { "awards.title" : {"value" : awards}}},
                        {"wildcard" : { "awards.instituition" : {"value" : awards}}}
                    ]
                }
            }
            must.append(query)

        filter = {}

        if roles[0] != "":
            filter = {
                "terms" : {
                    "films.role": roles
                }
            }
        bool = {}
        bool["must"] = must
        if filter != {}:
            bool["filter"] = filter
        query = {}
        query["bool"] = bool
        body["query"] = query
        response = es.search(index="artists", body=body)

        try:
            results = response["hits"]["hits"]
        except:
            results = []

        if len(results) == 0:
            body = {}
            suggest = {
                "spell_check" : {
                    "text" : search_terms,
                    "term" : [
                        {"field" : "name"},
                        {"field" : "real_name"},
                        {"field" : "bio"},
                        {"field" : "films.title"},
                        {"field" : "awards.title"},
                        {"field" : "awards.instituition"},
                    ]
                        
                }
            }
            body["suggest"] = suggest
            spell_checks = es.search(index="artists", body=body)
            try:
                suggest_text = spell_checks["suggest"]["spell_check"][0]["options"][0]["text"]
                orig_text = spell_checks["suggest"]["spell_check"][0]["text"]
                spell_suggestion = search_terms
                spell_suggestion = spell_suggestion.replace(orig_text, suggest_text)
            except:
                spell_suggestion = ""


    all_roles = []
    body = {}
    agg = {
        "by_role" : {
            "terms" : {
                "field" : "films.role.keyword"
            }
        }
    }
    body["aggregations"] = agg
    all_roles = es.search(index="artists", body=body)["aggregations"]["by_role"]["buckets"]

    return render_template(
        '/search.html', 
        results = results, 
        search_type = search_type, 
        search_terms = search_terms,
        films = films,
        awards = awards,
        roles = roles,
        show = show,
        all_roles = all_roles,
        spell_suggestion = spell_suggestion
    )