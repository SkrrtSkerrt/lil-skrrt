# BOOTSTRAP

Follow this sequence exactly.

```bash
git clone https://github.com/SkrrtSkerrt/hermes-agent-clean-v0.14.0.git
cd hermes-agent-clean-v0.14.0
git checkout v0.14.0-clean
bash scripts/install.sh
```

If you need a starter config:

```bash
cp cli-config.yaml.example ~/.hermes/config.yaml
cp .env.example ~/.hermes/.env
```

DIRECTIVE:
- Stay on v0.14.0-clean unless a later version is proven stable.
- Do not import your secrets, chat sessions, or personal customizations into this baseline.
