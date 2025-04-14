from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import os

app = Flask(__name__)

# Đảm bảo thư mục templates tồn tại
if not os.path.exists('templates'):
    os.makedirs('templates')

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        sparql = SPARQLWrapper("http://localhost:3030/test/query")
        query = f"""
            PREFIX : <http://example.org/ontology#>
            SELECT ?product ?name ?price WHERE {{
                    ?product a :Product ;
                :hasName ?name ;
                :hasPrice ?price ;
                :producedBy ?brand ;
                :belongsToCategory ?category .
            ?brand :hasName ?brandName .
            ?category :hasName ?categoryName .
                FILTER regex(?name, "{keyword}", "i")
            }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return render_template("results.html", 
                            results=results,
                            keyword=keyword)
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)