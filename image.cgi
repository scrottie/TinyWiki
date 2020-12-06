#!/usr/bin/perl

($word, $image) = map { $_ =~ s/(?:[a-z]+=)||[^A-Za-z0-9_.-]//g; $_ } split /\&/, $ENV{QUERY_STRING} || '';
$word eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\n\n", (<DATA>); exit 0; };
@ARGV=($word); $text = "\n" . join '', <>;

my $ref = $ENV{HTTP_REFERER};
#unless(
#  $ref =~ m{^http://(?:www\.)?example\.com/}i or
#  ! $ref
#) {
#  print qq{Content-type: text/plain\r\n\r\nI prefer not to provide anonymous housing for images for other sites.\n};
#  foreach my $i (keys %ENV) { print $i, ' ', $ENV{$i}, "\n" };
#  exit 0;
#}

my $imagefn; my $uudata = ''; my $state = 0; my $setstate = sub { $state = shift; 1; };
while(1) {
  $state == 3 && $text =~ m/\G(?<=\n)end.*?\n/icgs && $setstate->(0) or
  $state == 3 && $text =~ m/\G(?<=\n).(.*?)\n/icgs && ($uudata .= $1) or
  $state == 0 && $text =~ m/\G(?<=\n)begin [0-9]+ ([\w.-]+)\n/icgs && $image eq $1 && $setstate->(3) or
  $text =~ m/\G.*?\n/cgs or last;
}

my $a; my $pos = 0; my $out = ''; while($pos < length $uudata) {
  $a = 0; map { $a<<=6; $a |= ((ord(substr($uudata, $pos++, 1)) - 32) & 0x03f) } (0..3);
  $out .= chr(($a>>16)&0xff) . chr(($a>>8)&0xff) . chr($a&0xff);
}

if($out =~ m/JFIF/) {
    print "Content-type: image/jpeg\r\n\r\n";
} elsif($out =~ m/GIF/) {
    print "Content-type: image/gif\r\n\r\n" 
} else {
    print "Content-type: image/png\r\n\r\n";
}

print $out;

__END__

  # $out .= sprintf "%c%c%c", map { ($a>>$_) & 0x0ff; } (16, 8, 0);  # slower?

