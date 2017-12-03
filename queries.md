Arquivo de rascunho para as queries, ainda não finalizadas (falta fazer o 
filter em cada uma, com o que seria o parâmetro de entrada).

#Q1

O nome do filme deve ser substituído de <nome> em 

FILTER REGEX(?f, "^<nome>$") .

SELECT ?1n ?2n
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?x foaf-modified:firstName ?1n .
  ?x foaf-modified:familyName ?2n .
  FILTER REGEX(?f, "^Isle of Dogs$") .
}

#Q2

O nome do diretor deve ser substituído de <nome> de modo que

FILTER REGEX(?1n, "^<primeironome>$") .
FILTER REGEX(?2n, "^<nomedefamilia>$") .

SELECT ?f
WHERE {
  ?d projeto:directs ?m .
  ?m projeto:movieTitle ?f .
  ?d foaf-modified:firstName ?1n .
  ?d foaf-modified:familyName ?2n .
  FILTER REGEX(?1n, "^Wes?") .
  FILTER REGEX(?2n, "^Anderson?") .
}

#Q3

SELECT ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?x foaf-modified:firstName ?1n .
  ?x foaf-modified:familyName ?2n .
  FILTER REGEX(?1n, "^Uma?") .
  FILTER REGEX(?2n, "^Thurman?") .
}

#Q4 actsIn

SELECT ?f
WHERE {
  ?x projeto:actsIn ?m .

  ?x foaf-modified:firstName ?1n .
  ?x foaf-modified:familyName ?2n .

  FILTER REGEX(?1n, "^Uma?") .
  FILTER REGEX(?2n, "^Thurman?") .

  ?y projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .

  ?y foaf-modified:firstName ?1m .
  ?y foaf-modified:familyName ?2m .

  FILTER REGEX(?1m, "^Mark?") .
  FILTER REGEX(?2m, "^Webber?") .
}

#Q5

SELECT ?1d ?2d
WHERE {
  ?x projeto:actsIn ?m .

  ?x foaf-modified:firstName ?1n .
  ?x foaf-modified:familyName ?2n .

  FILTER REGEX(?1n, "^Uma?") .
  FILTER REGEX(?2n, "^Thurman?") .

  ?y projeto:actsIn ?m .

  ?y foaf-modified:firstName ?1m .
  ?y foaf-modified:familyName ?2m .

  FILTER REGEX(?1m, "^Mark?") .
  FILTER REGEX(?2m, "^Webber?") .

  ?d projeto:directs ?m .
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q6