# specter-bmad

Module BMAD custom Specter — skills et workflows au-dessus du framework BMAD.

## Prérequis

- Node.js >= 18
- BMAD >= 6.2.0 (`npx bmad-method`)

## Installation

```bash
# 1. Ajouter le module Specter au projet
npm install github:mqueval/specter-bmad#v1.0.0

# 2. Installer BMAD avec la surcouche Specter
npx bmad-method install --custom-content ./node_modules/specter-bmad
```

Si le projet n'a pas de `package.json`, initialiser d'abord :

```bash
npm init -y
```

## Mise a jour

```bash
npm install github:mqueval/specter-bmad#v1.1.0
npx bmad-method install --custom-content ./node_modules/specter-bmad
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
├── package.json
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
3. Bump la version dans `package.json`
4. Tag et push : `git tag vX.Y.Z && git push origin vX.Y.Z`
5. Dans les projets consommateurs : `npm install github:mqueval/specter-bmad#vX.Y.Z`

## Licence

MIT
