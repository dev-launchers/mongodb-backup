#!/bin/bash
# Script to upload backup to Google drive
mkdir dump
mongodump --uri=$URI --username=$USERNAME --password=$PASSWORD --out=dump
