#script to start long lived processes.
#Process id is printed to the console if you start the script in the backgroud.
#Example invocation. 1st line is the invocation, 2nd line is the process id
#./start_process_tree.sh &
#[1] 12225
#
#Use that process ID as the parent process ID for your script

cat > /tmp/test_script_1280.sh << TEST
sleep \${1}h
TEST

chmod u+x /tmp/test_script_1280.sh


#start children
bash /tmp/test_script_1280.sh 10 &
bash /tmp/test_script_1280.sh 21 &
bash /tmp/test_script_1280.sh 22 &

#keeps process alive even when scripts have been terminated
while [ 1 ]
do
   sleep 5h
done
