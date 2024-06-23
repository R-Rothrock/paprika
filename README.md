# Paprika

Simple command line tool designed to hide malware in Debian package
(`.deb`) files. Upon installation, it can:

1. Run your program as root.
2. Properly place and load your kernel module (`.ko`) file. Might not
   work, depending on kernel settings.
3. Properly place and enable your service (`.service`) file. Won't
   work if you don't use `systemd`.

This program is pretty bare-bones. It _should_ work, though. It'll
work with the first one I know for sure, but as for the other ones,
no guarantee; you might have to do some hacking to jank it into
fruition.
