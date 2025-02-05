suspect=$1
processed=$2
temp=$(mktemp)
sid=$(mktemp)
grade=$(mktemp)
process_temp=$(mktemp)
tail -n +2 $suspect | cut -d"," -f1,5 | sort -t"," -k1 >$temp
tail -n +2 $processed | sort -t"," -k2 >$process_temp
cut -d"," -f1 $process_temp >$grade
cut -d"," -f2 $process_temp >$sid
paste -d"," $sid $grade >$process_temp

comm $process_temp $temp | cut -d"," -f1 | cut -f1 | grep -v "^$" | sort -r

rm $temp
rm $sid
rm $grade
rm $process_temp
