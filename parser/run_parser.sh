#!/bin/bash

if [ "$1" == "-h" || "$1" == "--help" || "$#" -lt 2]; then
  echo "Usage: $0 user password [db] [install]"
  echo "  user     - DB user"
  echo "  password - DB password"
  echo "  db       - 'mysql' or 'postgres' (optional)"
  echo "  install  - 1 if install and download before, 0 otherwise (optional)"
  exit 0
fi

# PostgreSQL takes too long. MySQL is faster.
DB='mysql'

INSTALL=0

if [ "$#" -eq 3]; then
  DB="$3"
fi

if [ "$#" -eq 4]; then
  INSTALL="$4"
fi

# Assuming Arch Linux. Note that everything in /tmp will be deleted after system shutdown!
if [ "$INSTALL" -eq 1 ]; then
  if [ "$DB" == "mysql" ]; then
    sudo pacman -S mariadb imdbpy mysql-python
    echo "Follow https://wiki.archlinux.org/index.php/Mysql and configure DB.."
  else
    sudo pacman -S imdbpy python2-psycopg2 postgresql
    echo "Follow https://wiki.archlinux.org/index.php/PostgreSQL and configure DB."
  fi
  read -n1 -r -p "Press any key to continue after configuring..."

  echo "Downloading imdb.tar..."
  link='https://drive.google.com/uc?export=download&confirm=hqJf&id=15io6Ja9zFHmc0kFJ30oqyo_oTiy_xJRT'
  curl "$link" -o /tmp/imdb.tar
  pushd .
  echo "Extracting .tar..."
  cd /tmp
  tar -xvf imdb.tar
  cd imdb

  echo "Deleting irrelevant .list.gz..."
  exc=('actors' 'actresses' 'directors' 'movies')
  for f in *; do
    n=0
    for g in ${exc[@]}; do
      if [ "$g.list.gz" == "$f" ]; then
        let n=1
      fi
    done
    if [ "$n" -eq 0 ]; then
      rm "$f"
    fi
  done

  popd
fi

r=`mysqlshow --user="$1" --password="$2" imdb | grep -v Wildcard | grep -o imdb`

if [ "$DB" == "mysql" ]; then
  if [ "$r" != "imdb"]; then
    # Create DB with PostgreSQL.
    createdb -W imdb
  fi
  # Run imdbpy's imdbpy2sql.py, assuming its path is /usr/bin/ and the directory containing all
  # *.list.gz is located at /tmp/imdb.
  python2 /usr/bin/imdbpy2sql.py -d /tmp/imdb/ -u "postgresql://localhost/imdb"
else
  if [ "$r" != "imdb"]; then
    # Create DB with MySQL.
    mysqladmin -p create imdb
  fi
  # Run imdbpy2sql.
  python2 /usr/bin/imdbpy2sql.py -d /tmp/imdb/ -u "mysql://$1:$2@localhost/imdb"
fi
# Run parser.
python2 parser.py
