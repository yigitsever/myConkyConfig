#!/usr/bin/env perl
use strict;
use warnings;

use Data::Dumper;

my $account = shift @ARGV;

$account || die "You should've supplied an account name, now I'm dying";

my $data = `ledger -f /home/yigit/Dropbox/ledger.dat bal $account`;

$data =~ s/,//g;    # I really don't want to handle 20,000.00

$data =~ /[-+]?([0-9]*\.?[0-9]+)/; # I stole this from the Internet

print $1;

### the below is conky's job
# print "Hi got $1 for money and $account for name\n";
#my $result = sprintf("\${offset 10}%s \${alignr}\${offset -10}%.2f\n", $account, $1);
#print '${color}' . "$1 \@$account\n";
#print $result;
