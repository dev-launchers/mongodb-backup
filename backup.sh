#!/bin/bash
# Script to upload backup to Google drive
mkdir dump
mongodump --host=$HOST --username=$USERNAME --password=$PASSWORD --out=dump
