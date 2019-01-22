#!/usr/bin/env perl
use strict;
use warnings;

use Data::Dumper;

my $output = `task todoConky`;
my @lines = split /\n/, $output;


#first line empty
#second, third line gereksiz
my @pruned = @lines[3..scalar(@lines) - 3];

#print Dumper \@pruned;

foreach my $line (@pruned) {

	$line =~ /(.*?) (\d{2}-\d{2}-\d{2} \d{2}:\d{2} \((\w+)\))/;
	my $task = $1;
	my $hour = $2;

	print '${color2}' . $task . "\t" . '${alignr}${color2}' . $hour . "\n";
}

