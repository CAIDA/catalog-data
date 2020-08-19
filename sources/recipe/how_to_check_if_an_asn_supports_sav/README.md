# How to check if an ASN supports SAV

~~~json
{
    "id" : "how_to_check_if_an_asn_supports_sav",
    "name" : "How to check if an ASN supports SAV",
    "description" : "Instructions and an example script to demonstrate the Spoofer Data API",
    "links": [
        {"to":"group:spoofer"},
        {"to":"software:spoofer_api"}
    ],
    "tags" : [
        "security"
    ]
}
~~~

The included [Perl script](dump-spoofer-api-after.pl) gives an example of how to programmatically retrieve results from the Spoofer Data API.  It assumes the local system has [curl](https://curl.haxx.se/) installed as well as the JSON::XS and Getopt::Long PERL packages.

This command-line returns all public Spoofer measurement sessions after May 1, 2020 for ASN 3356:

~~~bash
perl dump-spoofer-api-after.pl --date "1 May 2020" --asn 3356
~~~

It will return a single JSON record for each session found.  The relevant fields for determining that a session detected spoofability are `privatespoof`, `privatespoof6`, `routedspoof`, and `routedspoof6`

A status of `received` indicates that a packet with a spoofed source address was received by CAIDA's servers and indicates that SAV is not deployed for that client's network.

~~~json
{"@id":"/sessions/891176","@type":"Session","asn4":"3356","asn6":null,"client4":"4.30.179.0/24","client6":null,"country":"usa","nat4":true,"nat6":null,"privatespoof":"blocked","privatespoof6":null,"routedspoof":"blocked","routedspoof6":null,"session":891176,"timestamp":"2020-05-07T14:34:59+00:00"}
{"@id":"/sessions/894351","@type":"Session","asn4":"3356","asn6":null,"client4":"8.9.89.0/24","client6":null,"country":"usa","nat4":true,"nat6":null,"privatespoof":"blocked","privatespoof6":null,"routedspoof":"blocked","routedspoof6":null,"session":894351,"timestamp":"2020-05-13T11:12:51+00:00"}
~~~

## Background

The CAIDA Spoofer Data API provides a public data interface to the publicly shareable data collected by the Spoofer project.  It is found at <https://api.spoofer.caida.org/>

### Endpoints

GET /sessions
: Retrieves the collection of Session resources

GET /sessions/{id}
: Retrieves a specific Session resource.

### Rules of Usage

CAIDA places no limit on the amount of requests, however, we ask that you send a message to spoofer-info at caida dot org if you plan to regularly do more than 1000 requests/day.  The [CAIDA Master Acceptable Use Agreement (AUA)](https://www.caida.org/home/legal/aua/) terms and conditions apply.

### Data Model

The data model contains a unique integer identifier for each session with a timestamp and parameters for read access, the IPv4 client address, the IPv6 client address, the country, NAT4 address, NAT6 address, and information about private and routed addresses. The API allows the user to query based on date, sessionid, or by Autonomous System Number (ASN).  The API returns a paginated list of measurement sessions.

The Spoofer Data API provides native support for [pagination]( https://api-platform.com/docs/core/pagination/) in the collection results it returns. Each page contains 30 items per page by default. The code chunk below displays the heart of the `dump-spoofer-api-after.pl` script: a while loop that handles the paginated results returned by the API.

~~~perl
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
~~~

### Documentation (auto-generated)

At <https://api.spoofer.caida.org/> you will see the Spoofer API 1.0.0 documentation. To expand the documentation for each endpoint, click the GET buttons. Once expanded, each endpoint displays the example parameters with buttons to "Try it out." The try it out button provides a graphical interface that allows the user to build and execute queries to the Spoofer API and see the example responses.
