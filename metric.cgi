#!/usr/bin/perl

if($ENV{HTTP_USER_AGENT} =~ m/Java/i) {
  print qq{Location: http://www.fuckoff.com\r\n\r\n};
  exit 0;
}

($start, $search, @dis) = 
  map { $_ =~ s/(?:[a-z]+=)||[^A-Za-z]//g; $_ } split /\&/, $ENV{QUERY_STRING};

$start eq 'self' and do {
  seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>);
  exit 0;
};

$sn = 'wiki.cgi';

print qq{Content-type: text/html
\n<html><head><title>Wiki: index</title></head>\n<body>
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

my @queue = ($start);
my $route = { $start => [$start] };
my $trust = { };

my $validroutes = 0;

# learn which words occur on which pages

my $found = sub { 
  my @route = @_;
  my $word = $route[-1];
  my $trustmetric = 1024;

  $validroutes++;

  return if @route > 1 and $route[-1] eq $route[-2];
  return if @route >= 10;
  return if $search and !$nodes->{$word}->{$search};

  # foreach my $i (@route) { print qq{<li><a href="$sn?$i">$i</a><br>}; } print qq{<hr>\n};

  # increment confidence interval

  foreach my $i (@route) { $trustmetric>>=1; }
  $trust->{$word} += $trustmetric;
};

# establish each nodes relationship with the root node

while(my $node = shift @queue) {
  # print "inspecting $node<br>\n";
  foreach my $i (keys %{$nodes->{$node}}) {
    unless($route->{$i}) {
      $route->{$i} = [@{$route->{$node}}, $i];
      push @queue, $i;
    }
    $found->(@{$route->{$node}}, $i); 
  }
}

# print accumluted score for each page

#my $numwords = scalar keys %$nodes;
#print qq{A total of $validroutes valid routes were found given $numwords pages.<br><br>\n};

# we don't want to play favorites
#my @sortednodes = sort { $trust->{$b} <=> $trust->{$a} } keys %$nodes;
my @sortednodes = sort { $a cmp $b } keys %$nodes;

my %dis = map { $_=>1 } @dis;

print '<table>', "\n";
foreach my $word (@sortednodes) {
  next unless $trust->{$word};
  next if $word eq $start;
  next if exists $dis{$word};
  print qq{<tr><td colspan="2"><br><b><a href="$sn?$word">$word</a></b></td></tr>}, 
        '<td width="25%" valign="top">',
        '<small>Search rating:</small><br>',
        $trust->{$word}, "<br>",
        '</td><td valign="top" width="75%">',
        '<small>Listed in:</small><br>',
        '&#183;&nbsp;', join(' &#183;&nbsp;', sort keys %{$xref->{$word}}),
        '</td></tr>';
}
print '</table><br>', "\n";

__DATA__

