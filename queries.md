Arquivo de rascunho para as queries, ainda não finalizadas (falta fazer o 
filter em cada uma, com o que seria o parâmetro de entrada).

#Q1

O nome do filme deve ser substituído de <nome> em 

FILTER REGEX(?f, "^<nome>$") .

SELECT ?1x ?2x
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .
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
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
  FILTER REGEX(?1d, "^Wes?") .
  FILTER REGEX(?2d, "^Anderson?") .
}

#Q3

SELECT ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .
  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .
}

#Q4 actsIn

SELECT ?f
WHERE {
  ?x projeto:actsIn ?m .

  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .

  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .

  ?y projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .

  ?y foaf-modified:firstName ?1y .
  ?y foaf-modified:familyName ?2y .

  FILTER REGEX(?1y, "^Mark?") .
  FILTER REGEX(?2y, "^Webber?") .
}

#Q5

SELECT ?1d ?2d
WHERE {
  ?x projeto:actsIn ?m .

  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .

  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .

  ?y projeto:actsIn ?m .

  ?y foaf-modified:firstName ?1y .
  ?y foaf-modified:familyName ?2y .

  FILTER REGEX(?1y, "^Mark?") .
  FILTER REGEX(?2y, "^Webber?") .

  ?d projeto:directs ?m .
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q6

SELECT ?1d ?2d (MAX(?vezes) AS ?max)
WHERE {
  SELECT ?1d ?2d (COUNT(?d) AS ?vezes)
  WHERE {
    ?x projeto:actsIn ?m .

    ?x foaf-modified:firstName ?1x .
    ?x foaf-modified:familyName ?2x .

    FILTER REGEX(?1x, "^Uma?") .
    FILTER REGEX(?2x, "^Thurman?") .

    ?d projeto:directs ?m .
    ?d foaf-modified:firstName ?1d .
    ?d foaf-modified:familyName ?2d .
  } GROUP BY ?1d ?2d
} GROUP BY ?1d ?2d

#Q7

SELECT ?1a ?2a (MAX(?vezes) AS ?max)
WHERE {
  SELECT ?1a ?2a (COUNT(?a) AS ?vezes)
  WHERE {
    ?d projeto:directs ?m .

    ?d foaf-modified:firstName ?1d .
    ?d foaf-modified:familyName ?2d .

    FILTER REGEX(?1d, "^Quentin?") .
    FILTER REGEX(?2d, "^Tarantino?") .

    ?a projeto:actsIn ?m .

    ?a foaf-modified:firstName ?1a .
    ?a foaf-modified:familyName ?2a .
  } GROUP BY ?1a ?2a
} GROUP BY ?1a ?2a

#Q8

Filme testado no caso é Chelsea Walls (2001) dirigido por Ethan Hawke.

Se mudarmos o filter para 

FILTER (?year >= 1980 && ?year <= 2000) .

o filme deixa de aparecer.

SELECT ?1d ?2d
WHERE {
  ?x projeto:actsIn ?m .
  
  ?m projeto:releaseYear ?year .
  FILTER (?year >= 1980 && ?year <= 2001) .

  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .

  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .

  ?y projeto:actsIn ?m .

  ?y foaf-modified:firstName ?1y .
  ?y foaf-modified:familyName ?2y .

  FILTER REGEX(?1y, "^Mark?") .
  FILTER REGEX(?2y, "^Webber?") .

  ?d projeto:directs ?m .
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q9

SELECT ?1a ?2a ?1b ?2b
WHERE {{
  SELECT ?m
  WHERE {
    ?x projeto:actsIn ?m .
    
    ?m projeto:releaseYear ?year .
    FILTER (?year >= 1980 && ?year <= 2004) .

    ?x foaf-modified:firstName ?1x .
    ?x foaf-modified:familyName ?2x .

    FILTER REGEX(?1x, "^Uma?") .
    FILTER REGEX(?2x, "^Thurman?") .

    ?y projeto:actsIn ?m .

    ?y foaf-modified:firstName ?1y .
    ?y foaf-modified:familyName ?2y .

    FILTER REGEX(?1y, "^Lucy?") .
    FILTER REGEX(?2y, "^Liu?") .
  }}

  ?a projeto:actsIn ?m .
  ?b projeto:actsIn ?m .

  FILTER (?a != ?b) .

  ?a foaf-modified:firstName ?1a .
  ?a foaf-modified:familyName ?2a . 

  ?b foaf-modified:firstName ?1b .
  ?b foaf-modified:familyName ?2b .
} ORDER BY ?1a ?2a ?1b ?2b

#Q10

SELECT DISTINCT ?f
WHERE {
  {
    SELECT ?m
    WHERE {
      ?d projeto:directs ?m .
      ?d foaf-modified:firstName ?1d .
      ?d foaf-modified:familyName ?2d .
      FILTER REGEX(?1d, "^Quentin?") .
      FILTER REGEX(?2d, "^Tarantino?") .
    }
  }

  ?a projeto:actsIn ?m .
  ?a foaf-modified:firstName ?1a .
  ?a foaf-modified:familyName ?2a .
   
  ?m projeto:movieTitle ?f .

  FILTER ((REGEX(?1a, "^Clive?") && REGEX(?2a, "^Owen?")) || (REGEX(?1a, "^Jamie?") && REGEX(?2a, "^Dunno?"))) .

}