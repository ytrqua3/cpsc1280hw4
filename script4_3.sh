process_ids=$(mktemp)
info=$(mktemp)
fnames=$(mktemp)
ps -f --ppid $1 | tr -s ' ' >$info 

cut -d' ' -f2 <$info| tail -n +2 >$process_ids
cut -d' ' -f8,9,10 $info | tail -n +2 >$fnames

paste -d',' $process_ids $fnames

cat $process_ids | xargs -I{} kill {}

rm $process_ids
rm $info
rm $fnames
