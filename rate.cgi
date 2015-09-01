#!/usr/bin/perl

if($ENV{HTTP_USER_AGENT} =~ m/Wget/i) {
  print qq{Location: http://www.perldesignpatterns.com/You_fucking_asshole_-_By_ignoring_robots.txt_youre_using_huge_amounts_of_
_CPU_time_generating_custom_reports_that_dont_get_you_anything_not_already_in_normal_pages\n\n};
  exit 0;
}


# bouncing off this page so we can exclude robots from voting (geesh)

my $in = $ENV{QUERY_STRING}; $in.='&'; read(STDIN, $in, $ENV{CONTENT_LENGTH}||0, length($in));
map { $nam='word';s{^([a-z]+)=}{$nam=$1;''}e; tr/+/ /; s/%(..)/pack('c',hex($1))/ge; $$nam=$_; } split/[&;]/, $in;
$word eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\r\n\r\n", <DATA>; exit 0; };
$sn = $ENV{SCRIPT_NAME}; $rip = $ENV{REMOTE_ADDR}; $wiki = qr{[A-Z][a-z]+[A-Z][A-Za-z]+};

if($ENV{HTTP_USER_AGENT} =~ m/Wget/i) {
  print qq{Location: http://www.perldesignpatterns.com/Hey_Dillweed_-_Dont_Use_Wget_on_a_Wiki_-_It_will_run_forever_-_get_pdp.wiki.tgz_instead\n\n};
  exit 0;
}

print qq{Location: http://perldesignpatterns.com/?RateThisPage&voteword=$voteword&vote=$vote\n\n};

__DATA__


