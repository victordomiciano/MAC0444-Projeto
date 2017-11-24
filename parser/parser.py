#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imdb import IMDb
import re
import sys
import unicodedata

if len(sys.argv) != 3:
  print("Usage: %s user password\n" % sys.argv[0])
  print("  user     - db user\n")
  print("  password - db password\n")
  exit(0)

user = sys.argv[1]
password = sys.argv[2]

# IMDb access.
I = IMDb('sql', uri=('mysql://%s:%s@localhost/imdb' % (user, password)))

# Initial list of people. (I) guarantees IMDbpy gets the most famous amongst them.
i_list = ['Uma Thurman (I)', 'Harvey Keitel (I)', 'Bill Murray (I)', 'Frances McDormand (I)', \
    'Quentin Tarantino (I)', 'Wes Anderson (I)']

q_movs = []

# Actors.
acts = {}
# Directors.
dirs = {}
# Movies.
movs = {}

# Agent (i.e. actor or director) movie references. Each entry is [role, movieID].
agt_refs = {}

def valid_movie(m):
  if (not m.get('episodes')) and m.get('director') and m.get('year') and m.get('cast') and \
      (m.get('kind') == 'movie'):
      return True
  return False

# Select only movies. Discard TV series.
def validate_movs(ai, r, m):
  I.update(m)
  i = m.movieID
  if valid_movie(m) and (not i in movs):
    movs[i] = m
    q_movs.append(m)
    if not ai in agt_refs:
      agt_refs[ai] = []
    agt_refs[ai].append([r, i])

# Adds person e's movies from l to dict d.
def add_to(l, d, e, r, m=None):
  i = e.personID
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

print("Retrieving initial actors and their movies...")
# Take roots defined by i_list.
retrieve_initial()

print("Retrieving secondary actors and directors...")
# Search through movies and add them to their respective dictionaries.
for m in q_movs:
  i = m.movieID
  # Take all actors and actresses from movie m.
  l_acts = m.get('cast')
  if l_acts:
    for a in l_acts:
      add_to(True, acts, a, 'a', i)
  # Take all directors from movie m.
  l_dirs = m.get('director')
  if l_dirs:
    for d in l_dirs:
      add_to(True, dirs, d, 'd', i)

q_movs = None

pattern = re.compile('[\W_]+', re.UNICODE)
def alphanumify(s):
  s = s.split()
  for i in range(0, len(s)):
    t = s[i]
    if type(s[i]) == unicode:
      t = unicodedata.normalize('NFKD', s[i]).encode('ascii', 'ignore')
    s[i] = pattern.sub('', t)
  u = ""
  for i in range(0, len(s)-1):
    u += s[i] + " "
  u += s[len(s)-1]
  return u

# Applies a camelCase format to string s.
def camelify(s):
  # Get rid of special characters.
  # Camelifies.
  tks = alphanumify(s).split()
  r = tks[0].lower()
  for i in range(1, len(tks)):
    r += tks[i].capitalize()
  return r

# Turns a complex name into a simple firstName, familyName. Returns first, family, first+family.
def namefy(s):
  tks = alphanumify(s).split()
  first, family = tks[0].capitalize(), tks[len(tks)-1].capitalize()
  return first, family, "%s %s" % (first, family)

inst_movs = {}
inst_agts = {}

# Initialize inst_* with camelified names/titles.
def get_inst_names():
  for k, e in movs.iteritems():
    inst_movs[camelify(e['title'])] = k
  for i in agt_refs.iterkeys():
    a = None
    if i in acts:
      a = acts[i]
    else:
      a = dirs[i]
    _, _, ff = namefy(a['name'])
    inst_agts[camelify(ff)] = i

print("Initializing instance names...")
get_inst_names()

# Prints different instances.
def print_diff_inst(t, d, f):
  T = []
  for k, _ in d.iteritems():
    if k != t:
      f.write("        projeto:%s\n" % k)

# Prints every movie's OWL representation.
def print_movies(f, cm, st):
  for _, m in movs.iteritems():
    t = alphanumify(m['title'])
    y = m['year']
    ct = camelify(t)
    f.write("Individual: projeto:%s\n\n" % ct)
    f.write("    Types:\n        projeto:Movie\n\n")
    f.write("    Facts:\n     projeto:movieTitle  \"%s\",\n" % t)
    f.write("     projeto:releaseYear  %d\n\n" % y)
    # f.write("    DifferentFrom:\n")
    # print_diff_inst(ct, inst_movs, f)
    # f.write("\n")
    cm -= 1
    if cm % st == 0:
      print("  Scanning movies... [%d/%d]" % (len(movs)-cm, len(movs)))

agents = {}

# Merges acts and dirs into a single dict agents.
def merge_ids():
  for k, v in acts.iteritems():
    if not k in agents:
      agents[k] = v
  for k, v in dirs.iteritems():
    if not k in agents:
      agents[k] = v

print("Merging IDs from agents (actors and directors)...")
merge_ids()

# ---- SQL ----

import MySQLdb

print("Connecting to DB...")
db = MySQLdb.connect(host="localhost", user=user, passwd=password, db="imdb")

def unfold_gender(c):
  if c == 'm':
    return "male"
  elif c == "f":
    return "female"
  else:
    return "nil"

# Gets the gender of agent of name "First Family".
def get_gender(first, family):
  # We assume the following:
  # If there exists a person p that has name "First Family", and let q be someone with the name
  # "First Middle Family", then p.gender == q.gender.
  # We first test for p. If there exists no p, then we obviously omitted Middle. If that is the
  # case, we search for the Middle name variant.
  db.query("SELECT gender FROM name N WHERE N.name LIKE '%s, %s';" % (family, first))
  r = db.store_result()
  t = r.fetch_row()
  # Another supposition (corollary to the above). If p and q are two people with the same name,
  # then we p.gender == q.gender.
  if len(t) != 0:
    return unfold_gender(t[0][0])

  # Case 1: "First Family1 Family2"
  db.query("SELECT gender FROM name N WHERE N.name LIKE '%% %s, %s';" % (family, first))
  r = db.store_result()
  t = r.fetch_row()
  if len(t) != 0:
    return unfold_gender(t[0][0])

  # Case 2: "First Middle Family"
  db.query("SELECT gender FROM name N WHERE N.name LIKE '%s, %s %%';" % (family, first))
  r = db.store_result()
  t = r.fetch_row()
  # There must exist a person with a name containing {first, family}.
  if len(t) != 0:
    return unfold_gender(t[0][0])
  else:
    return "nil"

# ---- SQL ----

# Prints every agent's OWL representation (i.e. actors or directors).
def print_agents(f, ca, st):
  for k, a in agents.iteritems():
    first, family, ff = namefy(a['name'])
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
      mov = camelify(movs[r[1]]['title'])
      if r[0] == 'd':
        f.write("     projeto:directs  projeto:%s,\n" % mov)
      else:
        f.write("     projeto:actsIn  projeto:%s,\n" % mov)
    f.write("     foaf-modified:familyName  \"%s\",\n" % family)
    f.write("     foaf-modified:firstName  \"%s\"\n" % first)
    f.write("     foaf-modified:gender  \"%s\"\n\n" % get_gender(first, family))
    # f.write("    DifferentFrom:\n")
    # print_diff_inst(cff, inst_agts, f)
    # f.write("\n\n")
    ca -= 1
    if ca % st == 0:
      print("  Scanning agents... [%d/%d]" % (len(agents)-ca, len(agents)))

step_cmpl = 100
movs_cmpl = len(movs)
agts_cmpl = len(agents)

print("Creating OWL file...")
with open('insts.owl', 'w') as owl_file:
  print("Exporting movies to OWL...")
  print_movies(owl_file, movs_cmpl, step_cmpl)
  print("Exporting agents to OWL...")
  print_agents(owl_file, agts_cmpl, step_cmpl)
  print("Closing OWL file...")
print("Bye.")
