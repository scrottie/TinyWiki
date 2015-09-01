#!/usr/bin/perl

$ENV{QUERY_STRING} eq 'self' and do {
  seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>);
  exit 0;
};

$sn = '';

print qq{Content-type: text/html\015\012\015\012<html><head><title>Wiki: index</title></head>\n<body>
  <a href="$sn?HomePage"><img src="back1.png" border="0" height="64" width="64"></a>
  <font size="+2">TinyWiki</font><br>
};

sub readword { @ARGV = ($_[0]); return "\n" . join '', <>; }

opendir my $dir, '.' or print $!;
my @dirs = sort grep { $_ !~ m/\./ and $_ =~ m/^[A-Z][a-z]/} (readdir $dir);
my @undefined;
my %keywords;
my %names;
foreach my $file (@dirs) {
  $keywords{$file} = 1;
  map { $keywords{$_} = 1 } $text =~ m/([A-Z][a-z]+[A-Z][A-Za-z]+)/g;
}
foreach my $file (keys %keywords) {
  my $text = readword($file);
  if($text =~ m/Describe '.*?' here/ or length($text) < 160) {
    push @undefined, $file;
    next;
  }
  my @matches = $text =~ m/([A-Z][a-z]+[A-Z][A-Za-z]+)/g;
  if(@matches < 100) {
    # watch out for generated pages that are meta indices
    foreach my $i (@matches) {
      $names{$i}++;
    }
  }
}

print qq{<h3>Referenced but undefined words:</h3>\n};
foreach my $word (sort @undefined) {
  print qq{<a href="wiki.cgi?$word&edit">$word</a><br>\n};
}
my %numrefs = map { ($_ => 1) } values %names; my @numrefs = sort { $a <=> $b } keys %numrefs;
foreach my $refs (@numrefs) {
  print qq{<h3>$refs references:</h3>\n};
  foreach my $word (keys %names) {
    next unless $names{$word} == $refs;
    print qq{<a href="wiki.cgi?$word">$word</a><br>\n};
  }
}
__DATA__

