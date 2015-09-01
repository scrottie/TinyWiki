#!/bin/bash

echo "Content-type: application/x-tar; name=\"perldesignpatterns.tar.gz\""
echo "Content-Disposition: inline; filename=\"perldesignpaterns.tar.gz\""
echo

(tar -czf - [A-Z][a-z][a-z]*[A-Za-z][A-Za-z]* *.cgi 2>/dev/null)
# (tar -czf - . 2>/dev/null)

