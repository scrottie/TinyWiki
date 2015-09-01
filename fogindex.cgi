#!/usr/bin/perl

# this file is from http://www.stonehenge.com/merlyn/LinuxMag/col18.html originally,
# by Randal L. Schwartz. local copy is all hacked up.

if($ENV{QUERY_STRING}) {
  print qq{Content-type: text/plain\n\n};
  seek DATA, 0, 0;
  print <DATA>;
  exit 0;
}

use warnings;
$|++;

## config
my $DATAFILE = "/tmp/.manfog";
## end config

use Lingua::EN::Fathom;
# use Fcntl qw(O_CREAT O_RDWR);
# use MLDBM qw(DB_File Storable);
# use File::Find;
# use sigtrap qw(die normal-signals);

# tie my %DB, 'MLDBM', $DATAFILE, O_CREAT|O_RDWR, 0644 or die "Cannot tie: $!";


opendir my $dir, '.' or print $!;
my @files = grep { $_ =~ m/^[A-Z][a-z]+[A-Z][A-Za-z]+$/ } readdir $dir;
closedir $dir;

my @info;

my $fat = Lingua::EN::Fathom->new;

for my $name (@files) {
  print "$name ==> ";

  # my $text = `nroff -Tascii $name`;
  # (print "cannot deroff: exit status $?"), next if $?;

  open my $f, '<', $name or die;
  read $f, my $text, -s $f;
  close $f;

  $fat->analyse_block($text);

  push @info, [$name => $fat->fog()];

  printf "done - %10.3f\n", $fat->fog();
}

print "final report:\n\n";

foreach my $page (sort { $a->[1] <=> $b->[1] } @info) {
  printf "%10.3f %s\n", $page->[1], $page->[0];
}

__DATA__

