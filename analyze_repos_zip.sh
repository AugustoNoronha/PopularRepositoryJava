REPOS_LIST=${1:-java_repos_list.txt}
CK_JAR=${2:-tools/ck.jar}
OUT_DIR=${3:-ck_results}
CLONE_DIR=${4:-clones_zip}
GITHUB_TOKEN="xxxxx"

mkdir -p "$OUT_DIR"
mkdir -p "$CLONE_DIR"

while IFS= read -r repo; do
  [ -z "$repo" ] && continue
  repo_dir="$CLONE_DIR/$(echo "$repo" | tr '/' '_')"
  out_csv="$OUT_DIR/$(echo "$repo" | tr '/' '_')_ck.csv"

  echo "=== Processing $repo ==="
  mkdir -p "$repo_dir"

  echo "Consultando branch padrão para $repo..."
  default_branch=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r '.default_branch')

  if [ -z "$default_branch" ] || [ "$default_branch" == "null" ]; then
    echo " Não consegui obter a branch padrão de $repo"
    continue
  fi
  echo " Branch padrão: $default_branch"

  url="https://github.com/$repo/archive/refs/heads/$default_branch.zip"
  echo "Baixando $url..."
  wget --quiet --show-progress -O "$repo_dir/repo.zip" "$url"

  if [ ! -s "$repo_dir/repo.zip" ]; then
    echo "Falha no download de $repo"
    rm -f "$repo_dir/repo.zip"
    continue
  fi
  echo "Download concluído ($(du -h "$repo_dir/repo.zip" | cut -f1))"

  echo "Descompactando $repo..."
  unzip -q -o "$repo_dir/repo.zip" -d "$repo_dir" || {
    echo "Erro ao descompactar $repo"
    continue
  }
  echo "Descompactação concluída"

  folder=$(find "$repo_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)
  echo "Executando CK em $folder..."
  # CK 0.7.x espera <diretório> <profundidade>
  # Executa CK e gera CSVs (class.csv, method.csv, etc.) no diretório atual
  java -jar "$CK_JAR" "$folder" 0

  # Move os CSVs para a pasta de resultados, renomeando para incluir o repositório
  for f in class.csv method.csv variable.csv field.csv; do
    if [ -f "$f" ]; then
      mv "$f" "$OUT_DIR/$(echo "$repo" | tr '/' '_')_$f"
    fi
  done
  echo "CK finalizado para $repo -> resultados salvos em $OUT_DIR"

  rm "$repo_dir/repo.zip"
done < "$REPOS_LIST"
