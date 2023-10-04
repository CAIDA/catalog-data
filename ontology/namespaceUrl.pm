{
  "@context": {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "schema": "https://schema.org/",
    "caida": "http://catalog.caida.org/ontology/"
  },
  "@graph": [
    {
      "@id": "caida:namespaceUrl",
      "@type": "rdf:Property",
      "rdfs:comment": "A URL to the PropertyMap's namespace.",
      "rdfs:label": "namespaceUrl",
      "schema:domainIncludes": {
        "@id": "caida:PropertyMap"
      },
      "schema:rangeIncludes": {
        "@id": "schema:URL"
      }
    }
  ]
}
