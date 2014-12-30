# -*- coding: utf8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
'''Log changes to files in a folder. Requires Linux > 2.6.

Try it:
    TerminalA> python3 -m watch-directory
    TerminalB> echo bar > /tmp/foo; touch /tmp/foo
'''

from inotify import (
    watcher, Threshold, IN_ATTRIB, IN_MODIFY, in_constants as mask
)
import select  # Required to poll event queue more efficiently

w = watcher.AutoWatcher()
p = select.poll()  # Poll object

# Register to stat and content changes in /tmp/
w.add('/tmp/', IN_ATTRIB | IN_MODIFY)

# Respond to any change volume to the watcher's file descriptor
thresh = Threshold(w, 0)  # value in bytes

# Register to incoming events in watcher
p.register(w, select.POLLIN)

while True:
    # Wait for events in watcher
    events = p.poll(None)  # value in ms/wait forever

    # Reiterate if events where read but threshold was not met
    # However, proceed and flush watcher if timeout kicked in
    if not thresh() and len(events) > 0:
        continue

    for e in w.read():
        m = mask.decode_mask(e.mask)  # Don't use e.mask_list, see issue #9
        if 'IN_ISDIR' in m:
            continue

        print("{}, {}".format(e.fullpath, m))
