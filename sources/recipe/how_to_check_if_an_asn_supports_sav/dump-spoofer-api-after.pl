#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long;
use JSON::XS;

STDOUT->autoflush(1);
STDERR->autoflush(1);

my $date;
my $sessionid;
my $asn;
my $api = "https://api.spoofer.caida.org";
my $accept = "accept: application/ld+json";

my $rc = GetOptions(
    "asn=s" => \$asn,
    "date=s" => \$date,
    "sessionid=i" => \$sessionid);

if(!$rc || (!defined($date) && !defined($sessionid)) ||
   (defined($date) && defined($sessionid)))
{
    print STDERR
	"usage: dump-spoofer-api-after.pl\n" .
	"   [--asn \@ases]\n" .
	"   [--date \$date]\n" .
	"   [--sessionid \$id]\n";
    exit -1;
}

my $cmd = "curl -s -X GET \"$api/sessions?";

# need one of these two
if(defined($date))
{
    my $encoded = join("%20", split(/\s+/, $date));
    $cmd .= "timestamp%5Bafter%5D=$encoded";
}
elsif(defined($sessionid))
{
    $cmd .= "session%5Bgt%5D=$sessionid\"";
}
else
{
    exit -1;
}

# optional ASN parameter
if(defined($asn))
{
    my @ases = split(/\s+/, $asn);
    foreach my $i (0 .. $#ases)
    {
	my $oneas = $ases[$i];
	if(!($oneas =~ /^\d+$/))
	{
	    exit -1;
	}
	$cmd .= "&asn%5B%5D=$oneas";
    }
}

$cmd .= "\" -H \"$accept\"";

my $page = 1;

while(1)
{
    print STDERR "page $page\n";

    my $obj;
    open(CURL, "$cmd |") or die "could not curl";
    while(<CURL>)
    {
	chomp;
	$obj = decode_json($_);
    }
    close CURL;
    last if(!defined($obj));

    foreach my $member (@{$obj->{"hydra:member"}})
    {
	my $str = encode_json($member);
	print "$str\n";
    }

    if(defined($obj->{"hydra:view"}) &&
       defined($obj->{"hydra:view"}{"hydra:next"}))
    {
	my $next = $obj->{"hydra:view"}{"hydra:next"};
	$cmd = "curl -s -X GET \"$api$next\" -H \"$accept\"";
    }
    else
    {
	last;
    }

    $page++;
}

exit 0;
