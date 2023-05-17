
for f in `ls portraits`;do
    if [[ $f == *.html ]];then
        OUT=`echo "${f%%.*}"`
        webkit2png -F --filename "portraits/${OUT}_ascii.jpeg" portraits/$f 
    fi

done
