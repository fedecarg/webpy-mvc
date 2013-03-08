#!/bin/bash
if [ "$1" == "" ] || [ "$2" == "" ]; then
  echo "Usage: $0 <source_file> <destination_file>"
  exit 0
fi

cat $1.sql |
grep -v ' KEY "' |
grep -v ' UNIQUE KEY "' |
grep -v ' PRIMARY KEY ' |
sed '/^SET/d' |
sed 's/ unsigned / /g' |
sed 's/ auto_increment/ primary key autoincrement/g' |
sed 's/ smallint([0-9]*) / integer /g' |
sed 's/ tinyint([0-9]*) / integer /g' |
sed 's/ int([0-9]*) / integer /g' |
sed 's/ character set [^ ]* / /g' |
sed 's/ enum([^)]*) / varchar(255) /g' |
sed 's/ set([^)]*) / varchar(255) /g' |
sed 's/ on update [^,]*//g' |
sed 's/\\r\\n/\\n/g' |
sed 's/\\"/"/g' |

perl -e 'local $/;$_=<>;s/,\n\)/\n\)/gs;print "begin;\n";print;print "commit;\n"' |
perl -pe '
if (/^(INSERT.+?)\(/) {
  $a=$1;
  s/\\'\''/'\'\''/g;
  s/\\n/\n/g;
  s/\),\(/\);\n$a\(/g;
}
' > $2.sql
cat $2.sql | sqlite3 $2.db > $2.err
ERRORS=`cat $2.err | wc -l`
if [ $ERRORS == 0 ]; then
  echo "Done! Output file: $2.db"
  rm $2.sql
  rm $2.err
else
  echo "There were errors during conversion. Please review $2.err and $2.sql for details."
fi
