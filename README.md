# HPLIP 3.20.3 Raspbian Edition

HPLIP installer fixed to work under raspbian.

I wanted to have fun with a Laserjet and found out I needed to edit the hplip installer to get it to work on a Raspberry Pi running Raspian (version 2020-02-13). The one in the raspbian repo did't seem to work. The original version of the HP driver package for linux can be found [here](https://sourceforge.net/projects/hplip/files/hplip/3.20.3/hplip-3.20.3.run/download?use_mirror=nchc).

The installer detected Raspbian as Debian 10.3, and there was no section for that in `installer/distros.dat`. Lel. Installing as Debian 10.2 did not work, so I added a section for 10.3 and fixed some of the package names so the installer doesn't trip and fall when calling the package manager. I also changed usage of `apt-get` to `apt`.

The installer should complete without issue (although it is still very, very bloaty, thanks HP!)

Disclaimer: I am not responsible, ever, at all, for anything you do with this repository. 

Oh and read COPYING. It contains the licensing information.