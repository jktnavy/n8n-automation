#!/bin/bash

set -a
source "$(cd "$(dirname "$0")/.." && pwd)/.env"
set +a

exec n8n start
