#!/bin/bash

export LANG=C

usage()
{
cat << EOF
usage: $0 options

This script parse and save svn logs into a couchDB instance.

OPTIONS:
   -h      Show this message
   -f      Shipping start date
   -l      Shipping last date
   -d      Developer Name
   -c      Custom dir (kewego, pj ...)
EOF
}

if [ -z $1 ]; then 
	usage;
	exit;
fi

#!/bin/bash
until [ -z "$1" ]; do
  case $1 in
    "-c")
      shift
      if [ "${1:1:0}" != "-" ]; then
		customDir=$1; shift
      fi;;
    "-d")
      shift
      if [ "${1:1:0}" != "-" ]; then
		developperName=$1;shift
      fi;;
    "-l")
      shift
      if [ "${1:1:0}" != "-" ]; then
		lastShipping=$1;shift
      fi;;
    "-f")
      shift
      if [ "${1:1:0}" != "-" ]; then
		firstShipping=$1;shift
      fi;;
    "-h")
		usage; exit;;
	*) shift;;

  esac
done

if [ -z $customDir ]; then 
	customDir='kewego';
fi

if [ -z $firstShipping ]; then
	firstShipping="HEAD"
else
	firstShipping="{$firstShipping}"
fi

workDir=/home/nico/workspace/pulse3/$customDir/
forShipping=/home/nico/forShipping.log
logs=/tmp/commits.logs
total=0
i=1

date=`date +%Y-%m-%d`
logsData=$(svn log --xml -v -r $firstShipping:{$lastShipping} $workDir | sed -e 's/\*/_/g')
truncate --size 0 /tmp/logs
echo $logsData > /tmp/logs
logsData=$(xmllint -xpath "/log" /tmp/logs | sed -e 's@</logentry>@</logentry>\n@g')

revisions=$(echo "$logsData" |\
			grep -i "$developperName" | \
			grep revision= | awk -F"\"" '{print "r"$2}')
truncate --size 0 $logs

logsData=$(cat /tmp/logs | sed -e 's@<msg>@<msg><![CDATA[@g' |  sed -e 's@</msg>@]]></msg>@g' )
echo $logsData > /tmp/logs

# Processing
date
echo "Summary ($revisions)"
echo "Gathering, please wait ..."

for k in $(echo $revisions | tr ' ' '\n'); do total=$((total+1)); done;

for rev in $revisions; do
	intRev=$(echo $rev | sed -e 's/r//g');
	revisionData="<log>$(echo "$logsData" | xmllint -xpath "logentry[@revision = '$intRev']" - )</log>";
	missing="";
	error="";
	revisionFile=/tmp/revision.$rev
	echo $revisionData > $revisionFile
	#svn log --xml -vr $rev $workDir > $revisionFile
	developperName=$(xmllint --xpath "/log/logentry/author" $revisionFile | html2text);
	comment=$(xmllint --nocdata --xpath "/log/logentry/msg" $revisionFile | html2text | sed -e 's@\\@\\\\@g' | sed -e 's/"/\\"/g' );
	date=$(xmllint --xpath "/log/logentry/date" $revisionFile | html2text);
	paths=$(xmllint --xpath "/log/logentry/paths/*" $revisionFile |\
		sed -e 's@">@">"@g' |\
		sed -e 's@</path>@"</path>\n@g' |\
		awk -F"\"" '{print "{\"path\":\""$6"\", \"action\":\""$4"\", \"kind\":\""$2"\"},"}')
	paths="[$paths]";
	paths=$(echo $paths | sed -e 's/,]/]/');
	line=$(echo "$comment ($rev $developperName)\n")
	
	nodeTemplate="
	   \"_id\"     : \"$rev\",
	   \"name\"    : \"$developperName\",
	   \"comment\" : \"$comment\",
	   \"date\"    : \"$date\",
	   \"paths\"   : $paths
	";
	
	record=`curl -s http://tuscaran.iriscouch.com/node_commits/$rev`
	missing=$(echo $record | grep "missing" | grep -v "_rev");

    if [ "$missing" != "" ]; then
    	method="POST";
    	document="";

    	# Rajout au wiki
    else 
    	dbRev=$(echo $record | awk -F"\"" '{print $8}')
    	method="PUT";
    	document=$rev;
	   	nodeTemplate="\"_rev\": \"$dbRev\",$(echo $nodeTemplate)"
    fi

    nodeTemplate="{$nodeTemplate}"

	echo "$nodeTemplate" > /tmp/template.$rev
	#echo "$method'ing `cat /tmp/template.$rev` to http://tuscaran.iriscouch.com/node_commits/$document "

	result=$(echo "$nodeTemplate" | curl -s -X $method http://tuscaran.iriscouch.com/node_commits/$document -d @/tmp/template.$rev -H "Content-Type: application/json");
	error=$(echo $result | grep "error")

    if [ "$error" != "" ]; then
    	echo "$nodeTemplate";
    	echo "$result";
    	exit;
    fi
	rm /tmp/template.$rev 

	# Progress bar
	percent=$((($i*1000/$total*1000)/10000))
	for cursor in $(seq $percent); do echo -n '#'; done
	for cursor in $(seq $percent 100); do echo -n ' '; done
	echo -n $percent
	echo -n "% [$i/$total] [$rev])\r"

	i=$((i+1)) 
	echo $line >> $logs
done;

cat $logs | sort > /tmp/sorted.logs
cp /tmp/sorted.logs $logs

echo "Grouping view ..."
cat $logs | sed -e '/^$/d' | sed -e 'y/ \. /   /' | sed -e 's/[ ]\{2,\}/ /g' > $forShipping 
cat $forShipping | sed -e 's/.*/\L&/' | sort | sed -e 's/(r.*$//g' | uniq > /tmp/forShipping; 

# Grouping
while read item ; do
	echo -n "- "
	echo -n $(cat $forShipping | grep -i "$item" | head -n 1 | sed -e 's/(r.*$//g')
	echo -n " ("
	echo -n $(cat $forShipping | grep -i "$item" | sed -e 's/^.*(\([r0-9]*\).*)/\1,/' | sed -e 's/,$//g')
	echo ") ($developperName)"
done < /tmp/forShipping

exit;

#rm -rf /tmp/forShipping
#rm -rf /tmp/revision.r*
#rm -rf /tmp/logs
