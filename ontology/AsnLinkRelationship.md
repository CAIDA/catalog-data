~~~metadata
{
    "@context":{
        "caida":"https://catalog.caida.org/ontology/",
        "schema":"https://schema.org"
    },
    "@type":"caida:Namespace",
    "@id":"caida:AsnLinkRelationshipNamespace",
    "schema:name":"ASN Link Relationship Namespace",
    "schema:URL":"https://www.caida.org/catalog/datasets/as-relationships/"
}
~~~
===schema:description
Although business agreements between ISPs can be complicated, the original model introduced by Gao 
abstracts business relationships into the following three most common types:
<b>Customer</b> ASN0 is a the customer of ASN1, <b>Provider</b> ASN1 is the provider of ASN1,
<b>Peer</b> ASN1 and ASN2 are peers, and <b>Silbing</b> ASN1 and ASN2 are siblings.