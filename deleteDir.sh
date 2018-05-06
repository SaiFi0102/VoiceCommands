for i in "$@"
do 

p=$(find /home/r2d2 -name $i)
echo "helllllllllllllllooooooooooo   $p"
rmdir $p
done 