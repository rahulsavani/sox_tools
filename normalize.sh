#bitdepth=16
bitdepth=24
# loop through wav files in TMP
# return file, normalised to -0.1 db
for i in `ls TMP/*.wav`; do
    sox $i -r 44100 -b $bitdepth `basename $i` norm -0.1
done

for i in `ls TMP2/*.aif`; do
    sox $i -r 44100 -b $bitdepth `basename $i`.wav norm -0.1
done
