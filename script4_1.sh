
lines=$2
lines=$((lines+1))
cut -d"," -f2,3,6 $1 | sort -t"," -k3 -r | head -n $lines
