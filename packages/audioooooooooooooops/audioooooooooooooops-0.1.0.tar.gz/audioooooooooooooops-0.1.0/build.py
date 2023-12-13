from setuptools.extension import Extension


custom_extension = Extension(
    "audioop",
    sources=["audioop/audioop.c"],
)


def build(setup_kwargs):
    """
    This is a callback for poetry used to hook in our extensions.
    """

    setup_kwargs.update(
        {
            # declare the extension so that setuptools will compile it
            "ext_modules": [custom_extension],
        }
    )