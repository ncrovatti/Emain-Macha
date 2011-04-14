#!/bin/sh

export LANG=C

lastShipping=$1
developperName=$2
customDir=$3



if [ -z $customDir ]; then 
	customDir='kewego';
fi

workDir=/home/nico/workspace/pulse3/$customDir/
forShipping=/home/nico/forShipping.log
logs=/tmp/commits.logs
total=0
i=1

date=`date +%Y-%m-%d`
#revisions=`svn log -r HEAD:{$lastShipping} $workDir | \
#			grep -i "$developperName" | \
#			sed -ne 's/.*\([r][0-9]\{3,\}\).*/\1/mgp' | \
#			tr -s '\n' ' '` 
revisions=`svn log --xml -r HEAD:{$lastShipping} $workDir |\
			grep -i "$developperName" | \
			grep revision= | awk -F"\"" '{print "r"$2}'` 
#echo "CMD: svn log -r HEAD:{$lastShipping} $workDir | grep -i '$developperName' | sed -e 's/^\([r0-9]*\).*/\1/g' | tr -s '\n' ' '"
truncate --size 0 $logs

# Processing
date
echo "Summary ($revisions)"
echo "Gathering, please wait ..."

for k in $(echo $revisions | tr ' ' '\n'); do total=$((total+1)); done;

for rev in $revisions; do
	missing="";
	error="";
	revisionFile=/tmp/revision.$rev
#	svn log -r $rev $workDir > $revisionFile
#	developperName=$(cat $revisionFile | sed -ne '/^[r\d+]/p' | cut -d '|' -f 2 | tr -d ' ')
#	comment=$(cat $revisionFile | \
#			sed -e 's/[\-]//gm' | \
#			tail -n +3 | \
#			sed -e '/^$/d' | \
#			sed -e 's/[ ]\{2,\}/ /g' | \
#			sed -e 'y/:/ /');

	
	
	svn log --xml -vr $rev $workDir > $revisionFile


	developperName=$(xmllint --xpath "/log/logentry/author" $revisionFile | html2text);
	comment=$(xmllint --xpath "/log/logentry/msg" $revisionFile | html2text | sed -e 's/"/\\"/g');
	date=$(xmllint --xpath "/log/logentry/date" $revisionFile | html2text)
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
    else 
    	dbRev=$(echo $record | awk -F"\"" '{print $8}')
    	method="PUT";
    	document=$rev;
	   	nodeTemplate="\"_rev\": \"$dbRev\",$(echo $nodeTemplate)"
    fi

    nodeTemplate="{$nodeTemplate}"

	#echo "$method'ing `cat /tmp/template.$rev` to http://tuscaran.iriscouch.com/node_commits/$document "

	echo "$nodeTemplate" > /tmp/template.$rev
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
echo 

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
