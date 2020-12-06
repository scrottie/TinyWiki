#!/usr/bin/perl

flock DATA, 2;  # one at a time access to this expensive page, please...

($word) = map { $_ =~ s/(?:[a-z]+=)||[^A-Za-z]//g; $_ } split /\&/, $ENV{QUERY_STRING};

$word eq 'self' and do {
  seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>);
  exit 0;
};

$sn = 'wiki.cgi';

print qq{Content-type: text/html\012\015\012\015
<html><head><title>Wiki: index</title></head>\n<body>
  <a href="$sn?HomePage"><img src="back1.png" border="0" height="64" width="64"></a>
  <font size="+2">TinyWiki</font><br>
};

sub readword { @ARGV = ($_[0]); return "\n" . join '', <>; }

opendir my $dir, '.' or print $!;
my @dirs = sort grep { $_ !~ m/\./ } (readdir $dir);
@dirs = grep { $_ ne 'cvslog' and $_ ne 'tmp' and $_ =~ m/^[A-Z][a-z]/} @dirs;
my $nodes;
my $xref;
foreach my $file (@dirs) {
  $nodes->{$file} = {};
}

foreach my $file (@dirs) {
  my $text = readword($file);
  my @matches = $text =~ m/([A-Z][a-z]+[A-Z][A-Za-z]+)/g;
  foreach my $match (@matches) {
    $nodes->{$file}->{$match} = 1;
    $xref->{$match}->{$file} = 1;
  }
}

my @sortednodes = sort { $a cmp $b } keys %{$xref->{$word}};

print '<table>', "\n";
foreach my $word (@sortednodes) {
  print '<td width="25%" valign="top">',
        qq{<a href="$sn?$word">$word</a>},
        '</td><td valign="top" width="75%">',
        '<small>Also references:</small><br>',
        '&#183;&nbsp;', (keys %{$nodes->{$word}} < 40 ? join(' &#183;&nbsp;', sort keys %{$nodes->{$word}}) : 'Many...'), '<br>',
        '<small>Also listed in:</small><br>',
        '&#183;&nbsp;', (keys %{$xref->{$word}} < 40 ? join(' &#183;&nbsp;', sort keys %{$xref->{$word}}) : 'Many...'), '<br>',
        '</td></tr>';
}
print '</table><br>', "\n";  

__DATA__

