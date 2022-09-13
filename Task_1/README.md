# Bash Script To Extend The Linux Partition

## Background
The script is responsible to automatically extend the linux partition on every reboot to maximum available block device volume;


## How To Setup?
Follow the following step to step this script for any VM:

- Copy `resize.sh` to the linux machine in `/etc/resize.sh`.
    - If you are using ext4 volume type then perform following additional step
    - Replace `sudo xfs_growfs -d /data` with `sudo resize2fs /dev/sdb`
- Copy `init.sh` to the linux machine in directory of your choice.
- Run `init.sh` using following command `source init.sh`
- Done ;)