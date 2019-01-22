#!/usr/bin/env perl
use strict;
use warnings;

use Data::Dumper;

my $inc = `task +in +PENDING count`;
$inc =~ s/^\s+|\s+$//g;
print "\${color0}$inc in tray\$stippled_hr\${color}\n";

my $output = `task inConky`;
my @lines = split /\n/, $output;

my @pruned = @lines[3..scalar(@lines) - 3];

my $cutoff = 50;

foreach my $line (@pruned) {
	if ( length $line > $cutoff ) {
		$line = substr($line, 0, ($cutoff - 3));
		$line .= "...";
	}

	print '${color}' . $line . "\n";
}

