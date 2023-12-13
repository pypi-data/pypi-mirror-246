# pylint: disable=W0622
"""cubicweb-seda application packaging information"""

modname = "seda"
distname = "cubicweb-seda"

numversion = (2, 2, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Data Exchange Standard for Archival"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 3.38.0, < 3.39.0",
    "cubicweb-eac": ">= 0.8.3, < 0.9.0",
    "cubicweb-skos": ">= 2.0.0",
    "cubicweb-compound": ">= 0.7",
    "cubicweb-relationwidget": ">= 0.4",
    "cubicweb-squareui": None,
    "cubicweb-geocoding": "< 0.4",
    "pyxst": ">= 0.3.2",
    "rdflib": ">= 4.1",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
