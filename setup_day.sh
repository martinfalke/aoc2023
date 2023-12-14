#!/bin/bash
DAY=$1
DATE=$(printf %02d $DAY)

mkdir $DATE
mv -v input $DATE/input$DATE.txt
sed -e "6s/$/DAY = $DAY/" dayX.py > $DATE/day$DATE.py
