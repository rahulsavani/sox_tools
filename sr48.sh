bitdepth=24
#bitdepth=24
# loop through wav files in TMP
for i in `ls TMP/*.wav`; do
    sox $i -r 48000 -b $bitdepth `basename $i` 
done

for i in `ls TMP2/*.aif`; do
    sox $i -r 48000 -b $bitdepth `basename $i`.wav 
done
