x= $1
y= $2

z=$(find /home/r2d2 -name "$1")
q=$(find /home/r2d2 -name "$2")
echo "heeeeeeeeeeeeelo    $z"
echo "keek $q"
cp $z $q 