#!/bin/sh

export PYTHONPATH=`pwd`/lib

#TC_LIST=`pwd`'/testsuits/5150_single_basic_list_8_2'
#TC_LIST=`pwd`'/testsuits/5150_single_basic_list_8_1_2'
TC_LIST=`pwd`'/testsuits/5340_multinode_basic_list_8_2'
#TC_LIST=`pwd`'/testsuits/5340_multinode_basic_list_8_1_2'

csv_file="/tmp/flex/Report-$(date '+%d-%b-%Y-%s').csv"

echo "TestCase,Result,Start_Time,End_Time,Time_Taken,LogFile" > $csv_file
flag=0
counter=0
for tc in `cat $TC_LIST`
do
        counter=$((counter+1))
        echo "`date` : Executing TC :" $tc
        TC=$(echo $tc | awk -F/ '{print $NF}' | tr '[:lower:]' '[:upper:]')
        TC=${TC::-3}
        startt=$(date +%s)
        START=`date '+%H:%M:%S'`
        LOG=$(echo $tc | awk -F/ '{print $NF}')
        log=${LOG::-3}.log

        if [ $flag -eq 0 ]
        then
            python $tc
            out1=$?
            endt=`date +%s`
            difftemp=`expr "${endt}" - "${startt}"`
            diff=`date +%H:%M:%S -ud @${difftemp}`
            END=`date '+%H:%M:%S'`
        else
            echo "`date` : Execution of TC :" $tc "is Skipped"
            END=`date '+%H:%M:%S'`
            endt=`date +%s`
            difftemp=`expr "${endt}" - "${startt}"`
            diff=`date +%H:%M:%S -ud @${difftemp}`
            echo "$TC,Skip,$START,$END,$diff,$log" >> $csv_file
            continue
        fi

        if [ $out1 -eq 0 ]
        then
               echo "`date` : Execution of TC :" $tc "is Successful"
               echo "$TC,Pass,$START,$END,$diff,$log" >> $csv_file
        else
               echo "`date` : Execution of TC :" $tc "is Failed"
               echo "$TC,Fail,$START,$END,$diff,$log">> $csv_file

               if [ $counter -lt 6 ]
               then
                       flag=1
               fi
        fi
done

### python lib/sendmail.py /tmp/flex/Report-05-Jan-2021-1609834204.csv
python `pwd`/lib/sendmail.py $csv_file
