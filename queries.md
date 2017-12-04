Arquivo de rascunho para as queries, ainda não finalizadas (falta fazer o 
filter em cada uma, com o que seria o parâmetro de entrada).

#Q1 - Quais atores participaram do filme F?

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

#Q2 - Quais filmes foram dirigidos pelo diretor D?

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

#Q3 - Em quais filmes o ator X atuou?

SELECT ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .
  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .
}

#Q4 actsIn - Em quais filmes o ator X atuou junto com Y?

SELECT DISTINCT ?f
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

  FILTER REGEX(?1y, "^Samuel?") .
  FILTER REGEX(?2y, "^Jackson?") .
}

#Q5 - Quem foram os diretores dos filmes nos quais os atores X e Y atuam juntos?

SELECT DISTINCT ?1d ?2d
WHERE {
  ?x projeto:actsIn ?m .

  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .

  FILTER REGEX(?1x, "^Uma?") .
  FILTER REGEX(?2x, "^Thurman?") .

  ?y projeto:actsIn ?m .

  ?y foaf-modified:firstName ?1y .
  ?y foaf-modified:familyName ?2y .

  FILTER REGEX(?1y, "^Samuel?") .
  FILTER REGEX(?2y, "^Jackson?") .

  ?d projeto:directs ?m .
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q6 - Qual o diretor que mais dirigiu filmes do ator X?

SELECT ?1d ?2d WHERE {
  {
    SELECT ?d (COUNT(?d) AS ?count)
    WHERE {
      ?x projeto:actsIn ?m .

      ?x foaf-modified:firstName ?1x .
      ?x foaf-modified:familyName ?2x .

      FILTER REGEX(?1x, "^Frances?") .
      FILTER REGEX(?2x, "^Mcdormand?") .

      ?d projeto:directs ?m .
    } GROUP BY ?d
  }

  {
    SELECT (MAX(?count) AS ?max)
    WHERE {
      {
        SELECT ?d (COUNT(?d) AS ?count)
        WHERE {
          ?x projeto:actsIn ?m .

          ?x foaf-modified:firstName ?1x .
          ?x foaf-modified:familyName ?2x .

          FILTER REGEX(?1x, "^Frances?") .
          FILTER REGEX(?2x, "^Mcdormand?") .

          ?d projeto:directs ?m .

        } GROUP BY ?d
      }
    } 
  }

  FILTER (?count = ?max)

  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q7 - Qual o ator que mais aparece nos filmes do diretor D?

SELECT ?1x ?2x WHERE {
  {
    SELECT ?x (COUNT(?x) AS ?count)
    WHERE {
      ?d projeto:directs ?m .

      ?d foaf-modified:firstName ?1d .
      ?d foaf-modified:familyName ?2d .

      FILTER REGEX(?1d, "^Wes?") .
      FILTER REGEX(?2d, "^Anderson?") .

      ?x projeto:actsIn ?m .
    } GROUP BY ?x

  }
  {
    SELECT (MAX(?count) AS ?max)
    WHERE {
      {
        SELECT ?x (COUNT(?x) AS ?count)
        WHERE {
          ?d projeto:directs ?m .

          ?d foaf-modified:firstName ?1d .
          ?d foaf-modified:familyName ?2d .

          FILTER REGEX(?1d, "^Wes?") .
          FILTER REGEX(?2d, "^Anderson?") .

          ?x projeto:actsIn ?m .
        } GROUP BY ?x
      }
    }
  }

  FILTER (?count = ?max) .

  ?x foaf-modified:firstName ?1x .
  ?x foaf-modified:familyName ?2x .
}

#Q8 - Entre os anos N1 e N2, quais diretores dirigiram filmes onde X e Y aparecem?

SELECT DISTINCT ?1d ?2d
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

  FILTER REGEX(?1y, "^Samuel?") .
  FILTER REGEX(?2y, "^Jackson?") .

  ?d projeto:directs ?m .
  ?d foaf-modified:firstName ?1d .
  ?d foaf-modified:familyName ?2d .
}

#Q9 - Entre os anos N1 e N2, quais atores atuaram juntos nos filmes onde X e Y aparecem?

SELECT DISTINCT ?1a ?2a ?1b ?2b
WHERE {
  {
    SELECT ?m
    WHERE {
      ?x projeto:actsIn ?m .
      
      ?m projeto:releaseYear ?year .
      FILTER (?year >= 1980 && ?year <= 2004) .

      ?x foaf-modified:firstName ?1x .
      ?x foaf-modified:familyName ?2x .

      FILTER REGEX(?1x, "^Bill?") .
      FILTER REGEX(?2x, "^Murray?") .

      ?y projeto:actsIn ?m .

      ?y foaf-modified:firstName ?1y .
      ?y foaf-modified:familyName ?2y .

      FILTER REGEX(?1y, "^Frank?") .
      FILTER REGEX(?2y, "^Pellegrino?") .
    }
  }

  ?a projeto:actsIn ?m .
  ?b projeto:actsIn ?m .

  FILTER (?a != ?b) .

  ?a foaf-modified:firstName ?1a .
  ?a foaf-modified:familyName ?2a . 

  ?b foaf-modified:firstName ?1b .
  ?b foaf-modified:familyName ?2b .
} ORDER BY ?1a ?2a ?1b ?2b
#Q10 - Quais filmes do diretor do filme F possuem X ou Y como atores?

SELECT DISTINCT ?f
WHERE {
  {
    SELECT ?d
    WHERE {
      ?m projeto:movieTitle ?f .
      FILTER REGEX(?f, "^Pulp Fiction?") .
      ?d projeto:directs ?m .
    }
  }

  ?d projeto:directs ?m .
  ?a projeto:actsIn ?m .

  ?a foaf-modified:firstName ?1a .
  ?a foaf-modified:familyName ?2a .
   
  ?m projeto:movieTitle ?f .

  FILTER ((REGEX(?1a, "(^Clive$)") && REGEX(?2a, "Owen")) 
    || (REGEX(?1a, "(^Jamie$)") && REGEX(?2a, "(^Dunno$)"))) .
}