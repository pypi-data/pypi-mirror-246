from collections import namedtuple

import dns.resolver
from dns.rdatatype import RdataType

Domain = namedtuple("DomainRow", "domain value")


def monochecker(domain: str, type_: str) -> list:
    answers: dns.resolver.Answer = dns.resolver.resolve(domain, type_)
    out: list = []
    for rdata in answers:
        if rdata.rdtype == RdataType.MX:
            out.append(Domain(str(rdata.exchange), str(rdata.preference)))
        if rdata.rdtype in [RdataType.A, RdataType.NS]:
            out.append(Domain(str(rdata), None))
    return out
