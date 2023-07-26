# The first 1 means "above-periods"
# audio is above 1% in volume for more than 0.1 seconds
sox $1 $1_burst_num.wav silence 1 0.1 0.5% 1 0.1 0.5% : newfile : restart
