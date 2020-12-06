#!/usr/bin/perl

# flock DATA, 2;  # one at a time access to this expensive page, please...

# originally by Doug Miles of Phoenix Perl Mongers, http://phoenix.pm.org
# bastardized by Scott Walters, scott@illogics.org, also of Phoenix Perl Mongers

$| = 1;

($word, $rev, $action) = map { $_ =~ s/(?:[a-z]+=)||[^A-Za-z0-9]//g; $_ } split /\&|\?/, $ENV{QUERY_STRING};

$word eq 'self' and do { seek DATA, 0, 0; print "Content-type: text/plain\n\n", <DATA>; exit 0; };

sub readword { @ARGV = ($_[0]); my $t = join '', <>; $t =~ s/\$([a-z]+)/$$1/ges; $t; }

# header

$sn = 'wiki.cgi';
print readword('header.html'), "-->\n";
my $navfooter = readword('footer.html');

# output formatting

%bc = ('+' => '#D0FFD0', '-' => '#FFD0D0', '!' => '#D0D0FF', ' ' => '#FFFFFF', '#' => '#E0E0E0');
$header = '<table border="0"><tr><td colspan="3">%s</td><td colspan="3">%s</td></tr>';
$row = '<tr><td bgcolor="%s">%s</td><td bgcolor="%s">%s</td><td bgcolor="%s"><pre>%s</pre></td><td bgcolor="%s">%s</td><td bgcolor="%s">%s</td><td bgcolor="%s"><pre>%s</pre></td></tr>';
$footer = '</table>';

# detect current version of file
# XXX - this should extract all known previous versions from the log rather than infer them

@ARGV = ($word); my $text = join '', <>;
my $cvslogstr = `cvs log $word`;
(my $currevmajor, my $currevminor) = $cvslogstr =~ m{\nhead: ([0-9]+)\.([0-9]+)}s; # head: 1.19
my $prevrevminor = $rev ? $rev : $currevminor - 1; $prevrevminor =~ s/[^0-9]//g;
die "$prevrevminor >= $currevminor - version silliness" if $prevrevminor >= $currevminor;

# clean up spooge

foreach my $i ($prevrevminor, $currevminor, $currevmajor) {
  $i =~ s/[^0-9]//g;
} 
$word =~ s/[^A-Za-z]//g;

# learn where repository is located

open my $rep, 'CVS/Root' or print __LINE__, ': ', $!;
read $rep, $cvsroot, -s $rep or print __LINE__, ': ', $!;
close $rep;
chomp $cvsroot;
-d $cvsroot or die __LINE__ . ": sanity-security check failed: $cvsroot"; 

# offer glimpse of previous versions

my $versionoptions = join "\n", map { 
  my $sel = defined $rev && $_ == $rev ? ' selected' : '';
  qq{  <option value="$_" $sel>$currevmajor.$_} 
} reverse (1 .. $currevminor-1);

print qq{
  <form method="get" action="diff.cgi">
    <input type="hidden" name="word" value="$word">
    <select name="rev">
      $versionoptions
    </select>
    <input type="submit" value="View">
  </form>
  <br>
  <a href="index.cgi?$word">Back to $word</a>
  <br>
};

# regress if that is what was requred

if($action eq 'regress') {
  die if $prevrevminor >= $currevminor;
  die if $currrevmajor >= $currevmajor;
  system 'cvs', split / /, "-d $cvsroot update -j $currevmajor.$currevminor -j $currevmajor.$prevrevminor $word";
  system 'cvs', 'commit', '-m', $ENV{REMOTE_ADDR}, $word;
  print qq{Regression attempted. Click <a href="diff.cgi?$word">here</a> for the results.};
  exit 0;
}

# build table of differences

open my $difffh, '-|', "cvs diff -r $currevmajor.$currevminor -r $currevmajor.$prevrevminor $word" or 
  print __LINE__, ': ', $!;

my %to_diff;
my %to_symbol;
my %from_diff;
my %from_symbol;

while(<$difffh>) {

  # Code adapted from patch.fuzzy Copyright (c) 1999 Moogle Stuffy Software.

  if($_ =~ /^(\s*)((\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?)/) {

    my ($space, $range, $from_start, $from_end, $command, $to_start, $to_end) =
       ($1,     $2,     $3,          $4 || $3,  $5,       $6,        $7 || $6);

    # print "debug: range: $range  fromstart: $from_start  fromend: $from_end  fromcommand: $command  tostart: $to_start  toend: $to_end <br>\n";

    my @to_pad;
    my @from_pad;
    my $from_count = $from_end - $from_start + 1;
    my $to_count   = $to_end - $to_start + 1;

    if($command eq 'a') {
      # Add.

      push @from_pad,
        ([$bc{'#'}, ' ', ' ', ' ']) x $from_count;

      $from_diff{$from_end} = [@from_pad];

      foreach my $line_number ($to_start..$to_end) {
        $to_symbol{$line_number} = '+';
      }


    } elsif($command eq 'd') {
      # Delete.

      push @to_pad,
        ([$bc{'-'}, ' ', ' ', ' ']) x $from_count;

      $to_diff{$to_end} = [@to_pad];

      foreach my $line_number ($from_start..$from_end) {
        $from_symbol{$line_number} = '-';
      }

    } elsif($command eq 'c') {
      # Change.

      my $count_delta = $from_count - $to_count;

      if($count_delta < 0) {

        push @from_pad,
          ([$bc{'#'}, ' ', '!', ' ']) x abs($count_delta);

        $from_diff{$from_end} = [@from_pad];

      } elsif($count_delta > 0) {

        push @to_pad,
          ([$bc{'!'}, ' ', '!', ' ']) x $count_delta;

        $to_diff{$to_end} = [@to_pad];

      }

      # Set up the change symbols.

      foreach my $line_number ($from_start..$from_end) {
        $from_symbol{$line_number} = '!';
      }

      foreach my $line_number ($to_start..$to_end) {
        $to_symbol{$line_number} = '!';
      }

    }

  }

}

# from file

my @from_file;
-f $word or print "$word does not exist<br>\n";
open my $ffh, $word;

while(<$ffh>) {

  chomp $_;

  my $background_color = exists($from_symbol{$.}) ? '#' : ' ';

  # Get the line number and the line contents.
  push @from_file,
    [$bc{$background_color}, $., $from_symbol{$.} || ' ', $_];

  # Append blank lines to the FROM file to compensate for additions to the TO
  # file.
  push @from_file, @{$from_diff{$.}} if exists $from_diff{$.};

}
close $ffh;

# to file

if(! -d '/tmp/wikidiff') {
  mkdir '/tmp/wikidiff' or print __LINE__, ': ', $!;
  chdir '/tmp/wikidiff' or die $!;
} else {
  chdir '/tmp/wikidiff' or die $!;
}
unlink $word; # or print __LINE__, ': ', $!;
system 'cvs', split / /, "-d $cvsroot checkout -r $currevmajor.$prevrevminor $word"; print "<br><br>\n";

my @to_file;
open my $tfh, $word or print __LINE__, ': ', $!;

while(<$tfh>) {

  chomp($_);

  # Get the line number and the line contents.
  push @to_file, [$bc{exists $to_symbol{$.} ? $to_symbol{$.} : ' '}, $., $to_symbol{$.} || ' ', $_];

  # Append blank lines to the TO file to compensate for deletions to the FROM file.
  push @to_file, @{$to_diff{$.}} if exists $to_diff{$.};

}
close $tfh;

my $diff_table = sprintf $header, 
   qq{<font size="+2">v$currevmajor.$prevrevminor - Previous Version</font>},
   qq{<font size="+2">v$currevmajor.$currevminor - Current Version</font>};

my $largest_line_count = $#from_file > $#to_file ? $#from_file : $#to_file;

for my $line_number (0..$largest_line_count) {

  $diff_table .= sprintf $row, map { s/&/&amp;/g; s/\</\&lt;/g; s/ /\&nbsp;/; $_ }
      map({ $to_file[$line_number]->[$_] }   (0, 1, 0, 2, 0, 3)),
      map({ $from_file[$line_number]->[$_] } (0, 1, 0, 2, 0, 3))
  ;

}

$diff_table .= $footer;

print $diff_table;

# footer

print qq{
<br><br>
<table>
  <tr><td>Legend:<br></td></tr>
  <tr><td bgcolor="$bc{'+'}">Added Text</td></tr>
  <tr><td bgcolor="$bc{'-'}">Removed Text</td></tr>
  <tr><td bgcolor="$bc{'!'}">Changed Text - After</td></tr>
  <tr><td bgcolor="$bc{'#'}">Changed Text - Before</td></tr>
  <tr><td bgcolor="$bc{' '}">No Change</td></tr>
</table>
<br>
};

print qq{
  <form method="get" action="diff.cgi">
    <input type="hidden" name="word" value="$word">
    <input type="hidden" name="rev" value="$prevrevminor">
    <input type="hidden" name="action" value="regress">
    <input type="submit" value="Regress to Version $currevmajor.$prevrevminor">
  </form>
  <br>
  Use this feature to recover a previous version that has since been overwritten.
  Ideally, this would never be needed, but sometimes edits go wrong, or someone
  disagrees by deleting. 
};

print $navfooter;

__DATA__


