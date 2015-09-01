#!/usr/bin/perl

use strict;
use warnings;

if($ENV{QUERY_STRING} eq 'self') {
    seek DATA, 0, 0;
    print qq{Content-type: text/plain\n\n}, <DATA>;
    exit;
}

print <<TEXT;
Content-type: text/xml

<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN"
  "http://my.netscape.com/publish/formats/rss-0.91.dtd">

<rss version="0.92">

<channel>

  <title>Perl Design Patterns - Software Engineering Meets Perl</title>

  <link>http://www.perldesignpatterns.com</link>

  <description>Most Perl is written to do a quickie job but sometimes these
hacks grow, and sometimes Perl is even selected for large projects.
When this happens, Perl programmers can learn a lot from industry, academia,
and the culture surrounding other languages.
Perl Design Patterns maintains Perl's philosophy rather than directly translating
ideas. As it turns out, Perl is especially well suited to building large systems as well
as small.
</description>

TEXT

my $origwiki = qr{[A-Z][a-z]+[A-Z][A-Za-z]+};

sub sb_listall { opendir my $dir, '.' or die $!; sort grep m/^$origwiki$/o, (readdir $dir) }

sub sb_recent {
    sort { $b->[1] <=> $a->[1] } 
        map [ $_, ( stat $_ )[9] ], 
        sb_listall();
}

*sb_datetime = sub {
    my $timestamp = shift;
    my @local = localtime($timestamp);
    my @date = @local[5,4,3]; $date[1] ++; $date[0] += 1900;
    my $date = join '/', map { length($_) == 1 ? "0$_" : $_ }  @date;
    my $hour = $local[2]; $hour ||= 12;
    my $am = 'am'; $hour > 12 and do { $hour -= 12; $am = 'pm' };
    my $time = sprintf("%s:%s:%s %s", $hour,
      map({ length($_) == 1 ? '0'.$_ : $_ } @local[1,0]),
      $am,
    );
    return $date, $time
};

my @files = sb_recent();
my $lastdate;
my $count = 20;
foreach(sb_recent()) {
    last unless $count--;
    (my $word, my $timestamp) = @$_;
    my ($date, $time) = sb_datetime( $timestamp );
  
    print <<TEXT;

      <item>
        <title>$word</title>
        <link>http://www.perldesignpatterns.com/?$word</link>
        <description>$word edited on $date at $time</description>
      </item>

TEXT

}

print qq{</channel></rss>\n};

__DATA__





