#!/usr/bin/env perl
#
###########################
#			  #
# author yigit sever	  #
###########################
use strict;
use warnings;

use Getopt::Long;
use XML::Feed;
use Text::Wrap;
use utf8;

$Text::Wrap::columns = 37; ## Depends on your 

GetOptions (
	'type=s'	=> \my $type,
	'number=i'	=> \(my $number = 5),
	'repo=s'	=> \my $repo,
) or die "Invalid options passed to $0\n";


my $feed = XML::Feed->parse(URI->new('https://github.com/' . $repo . '/commits/master.atom')) or die XML::Feed->errstr;

if ($type eq "title") {
	print $feed->title;
} elsif ($type eq "items") {
	my @entries = $feed->entries;

	for (1 .. $number) {
		my $item = shift @entries;
		my $title = $item->title;
		my $author = $item->author;
		$title =~ s/^\s+|\s+$//g;
		print '${color1}' . $author . ' $stippled_hr' . "\n";
		my $lines = fill('', '', $title);
		print '${color}' . $lines . "\n";
	}
}
