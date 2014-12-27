# Motivation

If you need to watch files don't poll the file system. Linux and Windows 
notify user-land processes by events. Subscribe to INotify on either platform.

Implementations may be platform specific, though (like python-inotify).
