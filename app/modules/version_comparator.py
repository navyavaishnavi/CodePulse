from packaging import version


class VersionComparator:

    def compare_versions(self, old_ver, new_ver):

        v1 = version.parse(old_ver)
        v2 = version.parse(new_ver)

        if v2.major > v1.major:
            return "Major Update"

        elif v2.minor > v1.minor:
            return "Minor Update"

        elif v2.micro > v1.micro:
            return "Patch Update"

        return "No Change"

    def read_requirements(self, file):

        packages = {}

        for line in file.getvalue().decode("utf-8").splitlines():

            if "==" in line:

                pkg, ver = line.strip().split("==")

                packages[pkg] = ver

        return packages

    def compare_dependencies(self, old_deps, new_deps):

        changes = []

        for pkg in old_deps:

            if pkg in new_deps:

                if old_deps[pkg] != new_deps[pkg]:

                    update_type = self.compare_versions(
                        old_deps[pkg],
                        new_deps[pkg]
                    )

                    changes.append({
                        "Package": pkg,
                        "Old Version": old_deps[pkg],
                        "New Version": new_deps[pkg],
                        "Update Type": update_type
                    })

        return changes