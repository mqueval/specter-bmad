# specter-bmad

Module BMAD custom Specter — skills et workflows au-dessus du framework BMAD.

## Prerequis

- Node.js >= 18
- BMAD >= 6.2.0 (`npx bmad-method`)

## Installation

```bash
# 1. Cloner le module Specter dans le projet
git clone --depth 1 --branch v1.0.0 https://github.com/mqueval/specter-bmad.git .specter-bmad

# 2. Installer BMAD avec la surcouche Specter
npx bmad-method install --custom-content ./.specter-bmad
```

Ajouter `.specter-bmad/` au `.gitignore` du projet consommateur.

## Mise a jour

```bash
cd .specter-bmad && git fetch && git checkout v1.1.0 && cd ..
npx bmad-method install --custom-content ./.specter-bmad
```

Pour un quick-update (utilise le cache `_bmad/_config/custom/`) :

```bash
npx bmad-method install --action quick-update
```

## Skills

| Skill | Menu | Description |
|-------|------|-------------|
| `specter-spec-engineer` | SE | Spec engineering structure en 5 etapes (diverge-then-converge). Produit des specifications AI-ready. |

## Structure

```
specter-bmad/
├── README.md
├── module.yaml          # code: specter
├── module-help.csv      # registre des skills
├── LICENSE
└── skills/
    └── specter-spec-engineer/
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/
```

## Version BMAD minimum

Ce module est teste avec BMAD >= 6.2.0. Les skills utilisent les variables BMAD suivantes :

- `{implementation_artifacts}` — dossier de sortie des specs
- `{planning_artifacts}` — dossier des artifacts de planning
- `{communication_language}` — langue de communication
- `{document_output_language}` — langue des documents
- `{user_name}` — nom de l'utilisateur
- `{project_knowledge}` — dossier de documentation projet

## Creer un nouveau skill

1. Creer un dossier dans `skills/` avec un `SKILL.md` (frontmatter `name` + `description`)
2. Ajouter une entree dans `module-help.csv`
3. Tag et push : `git tag vX.Y.Z && git push origin vX.Y.Z`
4. Dans les projets consommateurs : `cd .specter-bmad && git fetch && git checkout vX.Y.Z && cd ..`

## Licence

MIT
