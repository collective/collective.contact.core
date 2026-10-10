# pkgutil, not pkg_resources: Plone 6.2 (zc.buildout 5) installs the other collective.* as native namespace portions
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
