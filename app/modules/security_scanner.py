class SecurityScanner:

    def __init__(self):

        # Demo vulnerability database
        self.vulnerable_packages = {

            "flask": {
                "0.9": "HIGH",
                "1.0": "MEDIUM"
            },

            "django": {
                "2.0": "HIGH"
            },

            "numpy": {
                "1.18.0": "LOW"
            }
        }

    def scan_dependencies(self, dependencies):

        results = []

        for package, version in dependencies.items():

            risk = "SAFE"

            if package in self.vulnerable_packages:

                vulnerable_versions = self.vulnerable_packages[package]

                if version in vulnerable_versions:

                    risk = vulnerable_versions[version]

            results.append({

                "Package": package,
                "Version": version,
                "Risk Level": risk
            })

        return results