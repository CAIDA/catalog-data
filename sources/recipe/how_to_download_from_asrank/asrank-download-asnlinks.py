#!  /usr/bin/env perl
# written 2018
# Bradley Huffaker <bhuffaker@ucsd.edu>
use strict;
use warnings;
use Getopt::Std;
use FindBin qw($Bin);
use lib "$Bin/lib";
use JSON;
use Data::Dumper;
use Utils;

use LWP::UserAgent;
use HTTP::Request;
my $user_agent = LWP::UserAgent->new(timeout=>10);

my ($exe) = ($0 =~ /([^\/]+)$/);
my $usage = "usage:$exe [-h] config";

my %opts;
if ((!getopts("",\%opts) || $#ARGV != 0) && !defined $opts{h}) {
    print STDERR $usage,"\n";
    print STDERR "load the links and compare with url";
    exit -1;
}
if (defined $opts{h}) {
    Help();
    exit;
}

my $config_file = $ARGV[0];
my $url = $ARGV[1];
my %asn;
my @files;
my ($org_date, $org_url, $org_file) = ParseConfig($config_file, qw(asn_org_date asn_org_url asn_org_file));

my %type_objects;
Download();
PrintFile($org_file);

sub Download {
    foreach my $type ("asns","orgs") {
        my $hasNextPage = 1;
        my $first = 5000;
        my $offset = 0;
        while ($hasNextPage) {
            my $url = "$org_url/$type/?dateStart=$org_date&dateEnd=$org_date&offset=$offset&first=$first";
            #print ("url:$url\n");
            my $req = HTTP::Request->new(GET => $url);
            my $res= $user_agent->request($req);
            if ($res->is_success) {
                my $info = decode_json($res->content);
                #print (Dumper($info));
                $hasNextPage = $info->{pageInfo}{hasNextPage};
                $first= $info->{pageInfo}{first};
                $offset = $info->{"pageInfo"}{offset} + $first;
                print ("$type $offset $info->{totalCount}\n");
                #print ("$type total:$info->{totalCount} offset:$pageOffset page:$info->{pageInfo}{pageSize}\n");
                if ($info->{"data"}) {
                    foreach my $object (@{$info->{"data"}}) {
                        if (defined $object->{orgId} and $object->{orgId} ne "null") {
                            #print ("$type $object->{orgName}\n");
                            push @{$type_objects{$type}}, $object;
                        }
                    }
                }
                #print (Dumper($info->{pageInfo}));
            } else {
                print $res->status_line, "\n";
                $hasNextPage = 0;
            }
        }
    }
}

sub PrintFile {
    my ($filename) = @_;
    print ("writing $filename\n");
    open(OUT, ">$filename") || die("Unable to open $filename:$!");
    print OUT ("# exe:$exe $ARGV[0]\n");
    foreach my $type_keys (
        [qw(orgs org_id changed org_name country source)],
        [qw(asns aut changed aut_name org_id opaque_id source)]) {
        my ($type, @keys) = @{$type_keys};
        my $keys_string = join("|",@keys);
        print OUT ("# format:$keys_string\n");
        foreach my $object (@{$type_objects{$type}}) {
            print OUT (encode_json($object)."\n");
=cut
            if ($type eq "orgs" || ($type eq "asns" && defined $object->{"org"} && $object->{"org"} ne "null")) {
                my @values;
                foreach my $key (@keys) {
                    my $k = $key;
                    $k = $key_key{$type}{$key} if ($key_key{$type}{$key});
                    my $v = "";
                    if ($k eq "changed" and $object->{$k}) {
                        my ($year,$mon,$day) = ($object->{$k} =~ /(\d\d\d\d)-(\d\d)-(\d\d)/);
                        $v = "$year$mon$day";
                    } else {
                        $v = $object->{$k} if ($object->{$k});
                    }
                    push @values, $v;
                }
                print OUT (join("|",@values),"\n");
            }
=cut
        }
    }
    close OUT;
}
