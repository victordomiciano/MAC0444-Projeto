#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imdb import IMDb
import re

# IMDb access.
I = IMDb('sql', uri='postgres://localhost/imdb')

# Initial list of people.
i_list = ['Uma Thurman', 'Harvey Keitel', 'Bill Murray', 'Frances McDormand', 'Quentin Tarantino',\
    'Wes Anderson']

q_movs = []

# Actors.
acts = {}
# Directors.
dirs = {}
# Movies.
movs = {}

# Agent (i.e. actor or director) movie references. Each entry is [role, movieID].
agt_refs = {}

# Select only movies. Discard TV series.
def validate_movs(ai, r, m):
  I.update(m)
  i = m['movieID']
  if (not 'episodes' in m) and (not i in movs):
    movs[i] = m
    q_movs.append(m)
    if not ai in agt_refs:
      agt_refs[ai] = []
    agt_refs[ai].append([r, i])

# Adds person e's movies from l to dict d.
def add_to(l, d, e, r, m=None):
  i = e['personID']
  if l and (not i in d):
    d[i] = e
    if m is None:
      for t in l:
        validate_movs(i, r, t)
    else:
      if not i in agt_refs:
        agt_refs[i] = []
      agt_refs[i].append([r, m])

# Retrieve initial list of movies from initial list of people.
def retrieve_initial():
  for p in i_list:
    agt = I.search_person(p)[0]
    I.update(agt)
    d = agt.get('director')
    a = agt.get('actor')
    if not a:
      a = agt.get('actress')
    add_to(d, dirs, agt, 'd')
    add_to(a, acts, agt, 'a')

# Take roots defined by i_list.
retrieve_initial()

# Search through movies and add them to their respective dictionaries.
for m in q_movs:
  i = m['movieID']
  # Take all actors and actresses from movie m.
  l_acts = m['cast']
  for a in l_acts:
    add_to(True, acts, a, 'a', i)
  # Take all directors from movie m.
  l_dirs = m['director']
  for d in l_dirs:
    add_to(True, dirs, d, 'd', i)

q_movs = None

# Applies a camelCase format to string s.
def camelify(s):
  # Get rid of special characters.
  p = re.compile('[\W_]+')
  s = p.sub('', s)
  # Camelifies.
  tks = s.split()
  r = tks[0].lower()
  for i in range(1, len(tks)):
    r += tks[i].capitalize()
  return r

insts_movs = {}
insts_agts = {}

# Initialize inst_* with camelified names/titles.
def get_inst_names():
  for k, e in movs.iteritems():
    inst_movs[camelify(str(e['title']))] = k
  for i in agt_refs.iterkeys():
    a = None
    if i in acts:
      a = acts[i]
    else:
      a = dirs[i]
    _, _, ff = namefy(str(a['name']))
    inst_agts[camelify(ff)] = i

get_inst_names()

# Prints different instances.
def print_diff_inst(t, d, f):
  T = []
  for k, _ in d.iteritems():
    if k != t:
      f.write("        projeto:%s\n" % v)

# Prints every movie's OWL representation.
def print_movies(f):
  for _, m in movs.iteritems():
    t = str(m['title'])
    y = m['year']
    ct = camelify(t)
    f.write("Individual: projeto:%s\n\n" % ct)
    f.write("    Types:\n        projeto:Movie\n\n")
    f.write("    Facts:\n     projeto:movieTitle  \"%s\",\n" % t)
    f.write("     projeto:releaseYear  %d\n\n" % y)
    f.write("    DifferentFrom:\n")
    print_diff_inst(ct, inst_movs, f)

agents = {}

# Merges acts and dirs into a single dict agents.
def merge_ids():
  for k, v in acts.iteritems():
    if not k in agents:
      agents[k] = v
  for k, v in dirs.iteritems():
    if not k in agents:
      agents[k] = v

merge_ids()

# Turns a complex name into a simple firstName, familyName. Returns first, family, first+family.
def namefy(s):
  tks = s.split()
  first, family = tks[0].capitalize(), tks[len(tks)-1].capitalize()
  return first, family, "%s %s" % (first, family)

# Prints every agent's OWL representation (i.e. actors or directors).
def print_agents(f):
  for k, a in agents.iteritems():
    first, family, ff = namefy(str(a['name']))
    cff = camelify(ff)
    is_d, is_a = k in dirs, k in acts
    f.write("Individual: projeto:%s\n\n" % cff)
    f.write("    Types:\n")
    if is_d:
      f.write("        projeto:Director\n")
    if is_a:
      f.write("        projeto:Actor\n")
    f.write("\n    Facts:\n")
    roles = agt_refs[k]
    for r in roles:
      mov = camelify(str(movs[r[1]]['title']))
      if r[0] == 'd':
        f.write("     projeto:directs  projeto:%s,\n" % mov)
      else:
        f.write("     projeto:actsIn  projeto:%s,\n" % mov)
    f.write("     foaf-modified:familyName  \"%s\",\n" % family)
    f.write("     foaf-modified:firstName  \"%s\"\n\n" % first)
    f.write("    DifferentFrom:\n")
    print_diff_inst(cff, inst_movs, f)

with open('insts.owl', 'r') as owl_file:
  print_movies(owl_file)
  print_agents(owl_file)
owl_file.closed()
