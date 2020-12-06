#!/usr/bin/perl

my $in = $ENV{QUERY_STRING}; $in.='&'; read(STDIN, $in, $ENV{CONTENT_LENGTH}||0, length($in));
map { $nam='word';s{^([a-z]+)=}{$nam=$1;''}e; tr/+/ /; s/%(..)/pack('c',hex($1))/ge; $$nam=$_; } split/[&;]/, $in;
$word eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\n\n", <DATA>; exit 0; };

# assemble.cgi etc will link here incorrectly...?
# urls like:
# www.example.com/intermap.cgi?wiki=TinyCGI&word=reverse.cgi?CategoryBook
# $word =~ s/.*\?//; 
# no, that is exactly correct - for TinyCGI



# print qq{Content-type: text/plain\n\ndebug: word is '$word', wiki is '$wiki'\n};

open my $f, '<', 'intermap.txt' or die $!;
while(<$f>) {
  chomp;
  next unless substr($_, 0, length($wiki)) eq $wiki;
  substr($_, 0, length($wiki)+1) = undef;
  print qq{Location: $_$word\n\n};
  exit 0;
}

print qq{Content-type: text/plain\n\nSorry, Wiki moniker $word is unknown.\n};

__DATA__

