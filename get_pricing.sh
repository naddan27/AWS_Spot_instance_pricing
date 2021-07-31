#!/bin/bash
regions=("us-east-1" "us-east-2")
instances=("p3.2xlarge" "c5.2xlarge" "c5.4xlarge")

#remove the api response directory if exists, and create a new one
API_DIR="./api_responses"
rm -rf $API_DIR
mkdir $API_DIR

#move previous summary to old folder
mv -v *.csv ./old_cost_summaries

#get the date range (current to two weeks ago)
CURRENTDATE=`date +"%Y-%m-%dT%T"`
PREVIOUSDATE=`date --date="$14 day ago" +"%Y-%m-%dT%T"`

#call the AWS cost api
echo Collecting Data from 2 weeks from now
regions=("us-east-1" "us-east-2" "us-west-2")
for INSTANCE in ${instances[@]}; do
echo "Looking at the instance: $INSTANCE"
for REGION in ${regions[@]}; do
echo "  in region $REGION"
aws ec2 describe-spot-price-history --instance-types $INSTANCE --start-time $PREVIOUSDATE --end-time $CURRENTDATE --product-description Linux/UNIX --output text --region $REGION >> ./${API_DIR}/${INSTANCE}_${REGION}.csv
done
done

#aggregate responses
python aggregate_api_responses.py
sleep 1


