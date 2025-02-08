open_pat="<[[:alnum:]]*\b"
close_pat="</[[:alnum:]]*>"
file=$1
tag_names=$(mktemp)
tags=$(mktemp)
open_count=$(mktemp)
close_count=$(mktemp)

grep -E -o "($open_pat|$close_pat)" $file | tr -d "</>" | sort | uniq >$tag_names
grep -E -o "($open_pat|$close_pat)" $file | tr -d "<>" >$tags
cat $tag_names | xargs -I{} grep -c -E "^{}" $tags >$open_count
cat $tag_names | xargs -I{} grep -c -E "^/{}" $tags >$close_count
paste $tag_names $open_count $close_count

rm $tag_names $tags $open_count $close_count

