#!/usr/bin/perl
print qq{Content-type: text/html
\n<html><head><title>Wiki: index</title></head>\n<body>
  <a href="$sn?HomePage"><img src="back1.png" border="0" height="64" width="64"></a>
  <font size="+2">TinyWiki</font><br>
};

opendir my $dir, '.' or print $!;
my @dirs = sort grep { $_ !~ m/\./ } (readdir $dir);
foreach my $file (@dirs) {
  print qq{<a href="wiki.cgi?$file">$file</a><br>\n};
}

