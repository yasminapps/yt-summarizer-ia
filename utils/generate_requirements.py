# Re-génération après réinitialisation de l'état
import pkg_resources

# Dépendances principales basées sur les fichiers mentionnés dans le projet
packages_used = [
    "flask",
    "requests",
    "python-dotenv",
    "youtube-transcript-api",
    "pytest"
]

# Récupérer les versions installées localement
installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
requirements = [f"{pkg}=={installed[pkg]}" for pkg in packages_used if pkg in installed]

# Sauvegarder dans requirements.txt
with open("requirements.txt", "w") as f:
    f.write("\n".join(requirements))

"requirements.txt"