# ELB-Replayer
Replays ELB Access Logs

# Usage

To replay `elb_access.log` against our Development server `dev.example.com`

    replayer.py --host dev.example.com elb_access.log

Or, simply output paths found, using the timing from the `elb_access.log`

    replayer.py --dry-run elb_access.log
