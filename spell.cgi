#!/usr/bin/perl -w

if($ENV{HTTP_USER_AGENT} =~ m/Java/i) {
  print qq{Location: http://www.fuckoff.com\r\n\r\n}:
  exit 0;
}

if($ENV{HTTP_USER_AGENT} =~ m/Wget/i) {
  print qq{Location: http://www.example.com/You_fucking_asshole_-_By_ignoring_robots.txt_youre_using_huge_amounts_of_
_CPU_time_generating_custom_reports_that_dont_get_you_anything_not_already_in_normal_pages\n\n};
  exit 0;
}

sub readword { return '' unless -f $_[0]; @ARGV = ($_[0]); return "\n" . join '', <>; } 

$sn = $ENV{SCRIPT_NAME}; $sn =~ s/spell.cgi/wiki.cgi/g;
$word = $ENV{QUERY_STRING}; $word =~ s/[^a-zA-Z]//g;
$wiki = qr{[A-Z][a-z]+[A-Z][A-Za-z]+};

$word eq 'self' and do {
  seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>); exit 0;
};

$word ||= 'HomePage';

print qq{Content-type: text/html\n\n<html><head><title>Wiki Spell: $word</title></head>\n<body>
  <a href="$sn?HomePage"><img src="back1.png" border="0" height="64" width="64"></a>
  <font size="+2">TinyWiki Spell: $word</font><br>\n
};

my $parser = readword('wiki.cgi'); $parser =~ s/.*\nwhile/while/s;

my $state = 0;
my $text = readword($word);

my @typos = map { lc $_ } $text =~ m{\s+([A-Z]?[a-z]{3,})\s+}gs;

open my $dictwords, '<', '/usr/share/dict/words';

my $readword = <$dictwords>; chomp $readword;
my $lastword = '';
my $confirmedtypos;
foreach my $word (sort { $a cmp $b } @typos) {
  next if $word eq $lastword; $lastword = $word;
  # print "debug: looking for $word<br>\n";
  next if $word eq $readword;
  MATCH:
    $readword = <$dictwords>; chomp $readword; $readword = lc $readword;
    # print "debug: .... read word $readword<br>\n";
  goto MATCH if(($word cmp $readword) > 0);
  # print qq{[$word] vs [$readword]<br>\n};
  $confirmedtypos->{$word} = 1 unless $word eq $readword;
}

$text =~ s{(\s+)([a-z]{3,})(\s+)}{
  exists $confirmedtypos->{$2} ? 
    qq{$1<a href="http://www.dict.org/bin/Dict?Form=Dict1&Query=$2&Strategy=*&Database=*&submit=Submit%20Query"><font color="red">$2</font></a>$3} : 
    $1.$2.$3;
}ges;

eval $parser;
__DATA__

