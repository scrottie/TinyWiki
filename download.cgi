#!/bin/bash

echo "Content-type: application/x-tar; name=\"site.tar.gz\""
echo "Content-Disposition: inline; filename=\"site.tar.gz\""
echo

(tar -czf - [A-Z][a-z][a-z]*[A-Za-z][A-Za-z]* *.cgi 2>/dev/null)
# (tar -czf - . 2>/dev/null)

