from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://rdf.insee.fr/sparql")
sparql.setReturnFormat(JSON)


def liste_departements():
    query = """
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?dep ?nom ?codedep WHERE {
        ?dep rdf:type igeo:Departement .
        ?dep igeo:nom ?nom .
        ?dep igeo:codeDepartement ?codedep .
    }
    order by ?nom
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    return [{
        'label': result['nom']['value'],
        'value': result['codedep']['value']
        } for result in results["results"]["bindings"]]



def liste_communes(code_dep):
    query = f"""
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?commune ?nom ?codecom WHERE {{
        ?commune rdf:type igeo:Commune .
        ?commune igeo:nom ?nom .
        ?commune igeo:subdivisionDe ?dep .
        ?dep igeo:codeDepartement "{code_dep}"^^xsd:token .
        ?commune igeo:codeCommune ?codecom
    }}
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    return [{
        'label': result['nom']['value'],
        'value': result['codecom']['value']
        } for result in results["results"]["bindings"]]



def population(codecom):
    query = f"""
    PREFIX idemo:<http://rdf.insee.fr/def/demo#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?commune ?nom ?popTotale ?date WHERE {{
        ?commune igeo:codeCommune "{codecom}"^^xsd:token .
        ?commune igeo:nom ?nom .
        ?commune idemo:population ?popLeg .
        ?popLeg idemo:populationTotale ?popTotale ; idemo:date ?date .
        }}
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    return {'x': [result['date']['value'] for result in results["results"]["bindings"]],
        'y': [result['popTotale']['value'] for result in results["results"]["bindings"]],
        'type': 'bar', 
        'name': results["results"]["bindings"][0]['nom']['value']}


if __name__ == "__main__" :

#    print(liste_departements())

#    print(liste_communes('27'))

    print(population('70285'))
