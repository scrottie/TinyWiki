#!/usr/bin/perl

use CGI::Carp 'fatalsToBrowser';
use Digest::MD5 'md5_hex';

my $diag = $ENV{QUERY_STRING}; $diag =~ tr/+/ /; $diag =~ s/%(..)/chr hex $1/ge;
$diag eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>); exit 0; };

-d '/tmp/vcg/' or mkdir '/tmp/vcg/' or die $!;
open my $log, '>>', '/tmp/vcg/diagram.log' or die $!;
print $log "\n\n", scalar localtime, ":\n";

# print "Content-type: image/gif\r\n\r\n";
print "Content-type: text/plain\r\n\r\n";

my $pid = $$;

my $digest = md5_hex($diag);

if(-f "/tmp/vcg/$digest.gif" and -s "/tmp/vcg/$digest.gif") {
  # image is cached
  open my $f, '<', "/tmp/vcg/$digest.gif" or die $!;
  read $f, my $img, -s $f; # or die $!;
  close $f;
  print $log "using cached image for hash $digest\n";
  close $log;
  print $img;
  exit 0;
}

my $scale = ''; $diag =~ s/ scale: *([0-9]+)/$scale = " -scale $1 "; '';/e;

open my $f, '>', "/tmp/vcg/$pid.vcg" or die $!;
print $f $diag;
close $f;

system("/usr/local/bin/xvcg $scale -color -ppmoutput /tmp/vcg/$pid.ppm /tmp/vcg/$pid.vcg >/tmp/vcg/diagram.log 2>>/tmp/vcg/diagram.log") and die $!;
# perhaps encode xvcg's non-silent output as a comment in the image in the future?
unlink "/tmp/vcg/$pid.vcg";

system("/usr/local/netpbm/pnmcrop < /tmp/vcg/$pid.ppm 2>>/tmp/vcg/diagram.log | /usr/local/netpbm/ppmtogif > /tmp/vcg/$pid.gif 2>>/tmp/vcg/diagram.log") and die $!;
unlink "/tmp/vcg/$pid.ppm";

open $f, '<', "/tmp/vcg/$pid.gif" or die $!;
read $f, my $img, -s $f; # or die $!;
close $f;

close $log;

rename "/tmp/vcg/$pid.gif", "/tmp/vcg/$digest.gif"; # cache for next time

print $img;

__END__

Hi! This script takes VCG (Visualization for Compiler Graphs) markup URL encoded and returns it rendered as a GIF.
Home page is http://perldesignpatterns.com/?TinyWiki - this is GNU software. It is protected under the
GNU GPL, and may only be used under the terms of the GNU GPL license. See http://perldesignpatterns.com/?TinyWiki for
more information and a full copy of the license.

This script has some paths hardcoded in it: NetPBM is in /usr/local/bin, and so is VCG. 
NetPBM is available from http://www.acme.com (from the makers of thttpd and xscreensaver), and
VCG seems to be kind of homeless and unmaintained, but the latest version is archived at
ftp://freebsd.org/pub/FreeBSD/distfiles/vcg.1.30.r3.17.tgz 
http://perldesignpatterns.com/?VisualizationCompilerGraphs has some documentation, but the tutorials that
come with VCG are invaluable - VCG is very powerful, and multifasceted.

# junk...

#(my $width) = $diag =~ m/ width: *([0-9]+)/;
#(my $height) = $diag =~ m/ height: *([0-9]+)/;
# $scale = " pnmscale -width $width -height $height 2>>/tmp/vcg/diagram.log | " if $width and $height;

