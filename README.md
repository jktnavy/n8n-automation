cat > README.md <<'EOF'

# n8n Automation

Repository untuk menyimpan workflow n8n, script pendukung, template, konfigurasi contoh, dan dokumentasi automation.

## Struktur

workflows/

- invoice-telegram
- seo-content-engine
- backup-monitoring

scripts/

- invoice
- seo
- backup-monitoring

templates/

- invoice
- prompts

config/

- contoh konfigurasi non-secret

docs/

- dokumentasi arsitektur dan deployment

tests/

- script dan data testing

## Prinsip

Workflow dibuat dan diedit melalui GUI n8n.

File workflow JSON di repository merupakan hasil export dari n8n untuk backup dan version control.

Credential, password, API key, token, dan database runtime tidak boleh disimpan di GitHub.
EOF
