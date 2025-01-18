#diff -y -r pyspread6/ pyspread7/　


#find pyspread6 pyspread7 -type f -name "*.py"  \
#| sed -e "s/^dir_1//g" | sed -e "s/^dir_2//g" | sort 

DIRA=pyspread9
DIRB=pyspread10

#cd $DIRA; ls -1 *.py |xargs -i diff -u ../$DIRA/{} ../$DIRB/{}
#cd $DIRA; ls -1 *.py |xargs -i diff -Bb -y --suppress-common-lines	../$DIRA/{} ../$DIRB/{}

#diff -Bb -y --suppress-common-lines $DIRA $DIRB
#diff -Bb -y  $DIRA $DIRB
diff -Bb -6 -u  $DIRA $DIRB

