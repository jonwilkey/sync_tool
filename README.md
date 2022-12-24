## Introduction

This package is intended as a method to sync local files to/from an S3 bucket.
Key features are:

* Syncs local and remote files (user specifies whether to push up or pull down changes)
* All files are tagged with metadata containing the file's SHA1 hash
* In upload mode
  * If a file doesn't exist in S3, it is added
  * If the S3 bucket has a file that isn't present locally, it's deleted
  * If the file exists both locally and in S3, it is only uploaded if the SHA1 hash of the local file is different (it's assumed that the local file with differing content is more recent and the desired copy to keep)
* Download mode has identical logic but in opposite direction
* File transfers are made using threading
