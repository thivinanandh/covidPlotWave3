#!/bin/bash

total=324
sum=0
val=0
for i in `ls *script_*.log`
do  

    val=`cat $i | wc -l`
    # echo $i $val
    
    sum=$(($sum + $val))
    nameOrg=$i
    filename="${nameOrg%.*}"
    tot=`cat $filename.sh | grep "XXXYYY" |  wc -l`
    sed -i "s/$filename .*/$filename : $val  \\/ $tot <\\/p> /g" index.html


done

totalrem=$(($total - $sum))
frac=$(($sum  * 100))
percent=$(($frac / $total))
echo "Total Remaining runs " $totalrem
echo "Percentage completed " $percent
sed -i "s/Total_Completed  : .*/Total_Completed  : $sum <\\/h2>/g" index.html
sed -i "s/Total_remaining  : .*/Total_remaining  : $totalrem <\\/h2>/g" index.html
sed -i "s/Percentage Completed   : .*/Percentage Completed   : $percent % <\\/h2>/g" index.html
