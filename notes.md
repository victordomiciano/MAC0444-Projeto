# Hipóteses assumidas ao construir o dataset do IMDb

- Um filme sempre possui diretores, ano de lançamento, elenco de atores,
  não possui "episódios" e tem tipo `movie`.
- Da lista inicial de pessoas, assumiu-se apenas os primeiros resultados da
  pesquisa "Nome (I)", onde Nome é o nome da pessoa.

# Protégé

Argumentos modificados de linha de comando:

``
-Xmx10G -Xms2G
``

Foram usados os seguintes prefixos no SPARQL:

``
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf-modified: <http://www.ime.usp.br/~renata/FOAF-modified>
PREFIX projeto: <http://www.semanticweb.org/renatogeh/ontologies/2017/10/projeto#>
``
