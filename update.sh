#!/bin/bash

echo 'Updating...'
git pull origin master
echo 'Finished. Starting bot...'
systemctl restart SmolBot