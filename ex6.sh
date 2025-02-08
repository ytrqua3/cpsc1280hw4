col_names=$2
file=$1

echo $col_names | tr " " "\n" | xargs -I{} echo {} {}.temp | xargs -n2 ./grap_col.sh $file
echo $col_names | tr " " "\n" | xargs -I{} echo {}.temp | xargs paste -d","
