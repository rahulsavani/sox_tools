# loop through wav files in TMP
# return mono file, normalised to -0.1 db
for i in `ls TMP/*.wav`; do
    # use left channel (remix 1 as opposed to remix 2) 
    # since that will work even if the wav is already mono
    sox $i -r 44100 -b 16 `basename $i` remix 1 norm -0.1
done
