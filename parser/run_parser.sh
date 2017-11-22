#!/bin/bash

INSTALL=1

# Assuming Arch Linux. Note that everything in /tmp will be deleted after system shutsdown!
if [ "$INSTALL" -eq "1" ]; then
  sudo pacman -S imdbpy python2-psycopg2
  link='https://drive.google.com/uc?export=download&confirm=hqJf&id=15io6Ja9zFHmc0kFJ30oqyo_oTiy_xJRT'
  curl "$link" -o /tmp/imdb.tar
  pushd .
  cd /tmp
  tar -xvf imdb.tar
  cd imdb

  exc=('actors' 'actresses' 'directors' 'movies')
  for f in *; do
    n=0
    for g in ${exc[@]}; do
      if [ "$g.list.gz" == "$f" ]; then
        let n=1
      fi
    done
    if [ "$n" -eq "0" ]; then
      rm "$f"
    fi
  done

  popd
fi

# Create DB with PostgreSQL.
createdb -W imdb
# Run imdbpy's imdbpy2sql.py, assuming it's path is /usr/bin/ and the directory containing all
# *.list.gz are located at /tmp/imdb
python2 /usr/bin/imdbpy2sql.py -d /tmp/imdb/ -u "postgresql://localhost/imdb"
# Run parser.
python2 parser.py
