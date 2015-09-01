#!/usr/bin/perl

$sn = 'wiki.cgi';

$ENV{'QUERY_STRING'} eq 'self' and do {
  seek(DATA, 0, 0); print qq{Content-type: text/plain\n\n}, <DATA>; exit 0;
};

print qq{Content-type: text/html\r\n\r\n
<html><head><title>Wiki: Recently Changed Files</title></head>\n<body>
  <a href="$sn?HomePage"><img src="back1.png" border="0" height="64" width="64"></a>
  <font size="+2">TinyWiki</font><br>
};


opendir my $dir, '.' or print $!;
my @files = 
  sort { $b->[0] <=> $a->[0] }
  map { [(stat $_)[9], $_]; } grep { $_ =~ m/^[A-Z][a-z]+[A-Z][A-Za-z]+$/ } readdir $dir;

my $lastdate;

foreach my $i (@files) {
  # $spam++; last if $spam > 100;
  my $p = $i->[1]; $p =~ s{.*/}{};
  my @date = (localtime($i->[0]))[5,4,3]; $date[1]++; $date[0]+=1900; 
  my $date = join '/', map { length($_) == 1 ? "0$_" : $_ }  @date;
  if($date ne $lastdate) {
    $lastdate = $date;
    print qq{<b>$date</b><br>\n};
  }
  my $hour = (localtime($i->[0]))[2]; $hour ||= 12; 
  my $am = 'am'; $hour > 12 and do { $hour -= 12; $am = 'pm' };
  printf qq{<a href="$sn?$p">%s:%s:%s %s -- %s</a><br>\n},
    $hour,
    map({ length($_) == 1 ? '0'.$_ : $_ } (localtime($i->[0]))[1,0]),
    $am,
    $p;
}

__DATA__

