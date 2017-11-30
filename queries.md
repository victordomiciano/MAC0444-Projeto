#Q1

SELECT ?p ?f
WHERE {
  ?p projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
} ORDER BY ?f

#Q2

SELECT ?d ?f
WHERE {
  ?d projeto:directs ?m .
  ?m projeto:movieTitle ?f .
} ORDER BY ?d

#Q3

SELECT ?x ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
} ORDER BY ?x

#Q4 com maker (não correto)

SELECT ?x ?y ?f
WHERE {
  ?a1 a projeto:Actor .
  ?a2 a projeto:Actor .
  ?m foaf-modified:maker ?a1 .
  ?m foaf-modified:maker ?a2 .
  ?m projeto:movieTitle ?f .
  FILTER (?x != ?y)
}

#Q4 actsIn

SELECT ?x ?y ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?y projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  FILTER (?x != ?y)
}

#Q5

SELECT ?d ?x ?y ?f
WHERE {
  ?x projeto:actsIn ?m .
  ?y projeto:actsIn ?m .
  ?m projeto:movieTitle ?f .
  ?d projeto:directs ?m .
  FILTER (?x != ?y)
}