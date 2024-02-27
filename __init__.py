try:
    from binaryninja import PluginCommand
    from .extractor import ExtractQResources

    def call_extract_qresources(bv):
        f = ExtractQResources(bv)
        f.start()

    PluginCommand.register(
        "Extract QResources", "Extract QResources", call_extract_qresources
    )
except ImportError:
    # unittests are executed without access to binaryninja api
    pass


