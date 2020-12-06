#!/usr/bin/perl

# bouncing off this page so we can exclude robots from voting (geesh)

my $in = $ENV{QUERY_STRING}; $in.='&'; read(STDIN, $in, $ENV{CONTENT_LENGTH}||0, length($in));
map { $nam='word';s{^([a-z]+)=}{$nam=$1;''}e; tr/+/ /; s/%(..)/pack('c',hex($1))/ge; $$nam=$_; } split/[&;]/, $in;
$word eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\r\n\r\n", <DATA>; exit 0; };
$sn = $ENV{SCRIPT_NAME}; $rip = $ENV{REMOTE_ADDR}; $wiki = qr{[A-Z][a-z]+[A-Z][A-Za-z]+};

print qq{Location: http://example.com/?RateThisPage&voteword=$voteword&vote=$vote\n\n};

__DATA__


