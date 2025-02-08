file=$1
col_name=$2
fout=$3
\
col_num=$(head -n1 $file | tr "," "\n" | tr -d " " | grep -n "$col_name" | cut -d":" -f1)
cut -d"," -f$col_num $file | tr -d ' ' >$fout
