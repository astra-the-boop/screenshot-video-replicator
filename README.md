# screenshot-video-replicator
idfk i'm not good at naming things

---

recreate video using screenshots of your desktop!

# how to use

download the `cli` file

run in terminal:

```bash
/path/to/cli [parameters]
```

# parameters:


|flag|short|default| description                  |
|----|-----|-------|------------------------------|
|--inputdir|-i|| path to input video (required)|
|--recordtime|-t|30| recording duration in secs   |
|--x|-x|22| number of columns            |
|--y|-y|10| number of rows|
|--scale|-s|10|output sharpness multiplier|
|--fps|-f|10|fps|
|--norecord|-rc||skip recording|
|--norender|-rn||skip frame rendering step|
|--nocomp|-nc||skip final video comp step|
|--nodelprev|-nd||keep previous screenshots instead of deleting them|

please be patient it takes a while