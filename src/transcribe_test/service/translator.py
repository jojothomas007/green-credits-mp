import argostranslate.package
import argostranslate.translate

# Download and install Argos Translate package
from_code = "fr"
to_code = "en"
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
# for package in available_packages:
#     if package.from_code == "fr" and package.to_code == "en":
#         argostranslate.package.install_from_path(package.download())
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

class Translator:
    def translate(message)->str:
        # Translate
        translatedText = argostranslate.translate.translate(message, from_code, to_code)
        return translatedText
        # 'Bonjour Monde'