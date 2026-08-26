# n8n Automation

Repository untuk menyimpan workflow n8n, script pendukung, template, konfigurasi contoh, dan dokumentasi automation.

## Environment

Lokasi project:

```bash
/home/heden/projects/n8n-automation
```

n8n dijalankan menggunakan:

- WSL Ubuntu
- Node.js
- npm
- n8n

Cek versi:

```bash
node -v
npm -v
n8n --version
```

---

## Menjalankan n8n

Masuk ke folder project:

```bash
cd /home/heden/projects/n8n-automation
```

Jalankan:

```bash
./scripts/start-n8n.sh
```

Script tersebut akan:

1. Membaca konfigurasi dari `.env`
2. Memasukkan environment variable
3. Menjalankan `n8n start`

Setelah n8n aktif, buka browser:

```text
http://localhost:5678
```

---

## Konfigurasi Environment

Konfigurasi lokal disimpan di:

```text
.env
```

Contoh:

```env
N8N_INSTANCE_AI_MODEL_URL=https://api.deepseek.com
N8N_INSTANCE_AI_MODEL=deepseek-v4-flash
N8N_INSTANCE_AI_MODEL_API_KEY=
```

Jangan memasukkan file `.env` ke GitHub.

Gunakan `.env.example` sebagai template konfigurasi tanpa secret.

---

## Script Startup

File:

```text
scripts/start-n8n.sh
```

Isi:

```bash
#!/bin/bash

set -a
source /home/heden/projects/n8n-automation/.env
set +a

exec n8n start
```

Pastikan executable:

```bash
chmod +x scripts/start-n8n.sh
```

---

## Struktur Repository

```text
n8n-automation/
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── workflows/
│   ├── invoice-telegram/
│   ├── seo-content-engine/
│   └── backup-monitoring/
│
├── scripts/
│   ├── start-n8n.sh
│   ├── invoice/
│   ├── seo/
│   └── backup-monitoring/
│
├── templates/
│   ├── invoice/
│   └── prompts/
│
├── config/
├── docs/
└── tests/
```

---

## Workflow

Workflow dibuat dan diedit melalui GUI n8n:

```text
http://localhost:5678
```

Repository GitHub digunakan untuk menyimpan:

- Workflow export
- Script pendukung
- Template
- Dokumentasi
- Konfigurasi contoh
- History perubahan melalui Git

Credential, password, API key, token, dan database runtime tidak boleh disimpan di GitHub.

---

## Git Workflow

Cek perubahan:

```bash
git status
```

Commit:

```bash
git add .
git commit -m "deskripsi perubahan"
```

Push:

```bash
git push
```

Contoh:

```bash
git add README.md scripts/start-n8n.sh
git commit -m "docs: add n8n startup instructions"
git push
```

---

## Stop n8n

Jika n8n sedang berjalan di terminal:

```text
Ctrl+C
```

---

## Quick Start

Setelah WSL dibuka:

```bash
cd ~/projects/n8n-automation
./scripts/start-n8n.sh
```

Kemudian buka:

```text
http://localhost:5678
```
