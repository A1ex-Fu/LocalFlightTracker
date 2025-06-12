This is a beta version of RTL1090.
Functionality is experimental and partially incomplete yet.
Please use at your own risk.
Retain the release that is working for you as a copy.

============================================================================
Build 103 - 15/09/2013

Added a switch that will enable/disable the FEC function
By default FEC is disabled in this version!
You can enable FEC by either
- check a new box in the CONFIG dialog - or -
- open the app with command line entry "/fec"

Note that - as always with RTL1090 - command line entries are not reflected 
in the CONFIG dialog.
Also, you will note that switching off FEC will reduce the cycle time 
(ms in the lower left corner).

============================================================================
Build 102 - 29/06/2013

- Decoder improved by brute force 1-bit error correction and brute force (FEC)

 DF11 and DF17 override for unknown DFs. This may be tough stuff
for slow computers. If your computer slows down considerably return
to a previous version please.

- Tabs introduced - List/Table selection moved to Tabs.
- Stats tab added: this brings back the previous status bar info about USB
packets per second.

- II/SI tab added. This tab adds the ability to quickly scan the Mode-S
interrogator codes around. A "radar1090.txt" file can be added to the
rtl1090 folder that holds II/SI code decodings. A sample file is attached.
The II/SI collection can be reset by a right mouse click action.
The recently seen codes and the last aircraft responding with that
code are displayed in red onwhite.

- Context menu (right mouse click) for text window, "listhold" established
by menu selection, revoked by mouse click

============================================================================
Build 101 - 20/05/2013

- GUI completely refurbished. Program window height can be altered and switches
are hidden by default. This makes the GUI more space efficient (and it looks
better)

- In status line: USB packet indicator (packets/s) changed to queue cycle
time (ms). The queue cycle time must stay below 300 ms for
lossless processing.

- Packet rate LEDs show all red when it appears that a USB data frame
 was lost. This is in preparation for work on better MLAT accuracy.

- Avg. Signal Strength (SG) and Message count (MSGS) added to flight table.
Avg. Signal Strength is normalized to 100% (max 99%).
Color codes are yellow (you can hear it), orange (you can see it),
red (you can touch it).

- Default display order in flight table changed. Newest flights are at top
for compatibility with DUMP1090 (not completely working yet)

- CONFIG dialog: some commmand line options can be selected from the dialog.
Command line entries are still valid and do override any selections.
If overriding occurs entries are printed in bold, but boxes may not be checked,
so the override conditions will not be saved to the configuration file.

- Update alert: when a new version is available an update sign appears in the
caption bar - no further functions yet

============================================================================
