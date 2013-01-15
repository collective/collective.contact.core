from zope.interface import implements

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.fti import DexterityFTI
from plone.supermodel import loadString, loadFile
from plone.supermodel.model import Model


class DexterityConfigurablePolicyFTI(DexterityFTI):
    """A Configurable policy FTI
    """

    implements(IDexterityFTI)

    meta_type = "Dexterity configurable policy FTI"

    _properties = DexterityFTI._properties + (
        {'id': 'schema_policy',
         'type': 'string',
         'mode': 'w',
         'label': 'Schema policy',
         'description': 'Schema policy'
        },
    )

    schema_policy = u'dexterity'

    def lookupModel(self):
        if self.model_source:
            return loadString(self.model_source, policy=self.schema_policy)

        elif self.model_file:
            model_file = self._absModelFile()
            return loadFile(model_file, reload=True, policy=self.schema_policy)

        elif self.schema:
            schema = self.lookupSchema()
            return Model({u"": schema})

        raise ValueError("Neither model source, nor model file, nor schema is specified in FTI %s" % self.getId())

    #
    # Base class overrides
    #

    # Make sure we get an event when the FTI is modified
