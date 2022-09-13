#!/bin/bash

sudo growpart /dev/sdb 1

sudo xfs_growfs -d /data
