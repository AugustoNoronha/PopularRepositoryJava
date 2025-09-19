import os
import pandas as pd
import requests
from datetime import datetime
import certifi

# Configurações
CK_RESULTS_DIR = "ck_results"
OUTPUT_FILE = "unified_metrics.csv"
REPO_LIST_FILE = "java_repos_list.txt"
GITHUB_TOKEN = "xxxxxxxx"

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repo_info(repo_fullname):
    """Busca estrelas, releases e idade do repositório via API do GitHub"""
    url = f"https://api.github.com/repos/{repo_fullname}"
    r = requests.get(url, headers=HEADERS, verify=False)
    if r.status_code != 200:
        print(f"⚠️ Falha ao buscar {repo_fullname}: {r.text}")
        return None

    data = r.json()
    stars = data.get("stargazers_count", 0)
    created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    idade = (datetime.utcnow() - created_at).days / 365.0

    # Releases
    rel_url = f"https://api.github.com/repos/{repo_fullname}/releases"
    r2 = requests.get(rel_url, headers=HEADERS, verify=False)
    releases = len(r2.json()) if r2.status_code == 200 else 0

    return stars, releases, round(idade, 2)

def process_ck_results():
    rows = []

    # Lê lista de repositórios e monta o mapeamento repo_name → nome_original
    with open(REPO_LIST_FILE, "r") as f:
        repos = [line.strip() for line in f if line.strip()]
    repo_map = {r.replace("/", "_"): r for r in repos}

    wanted = ["cbo", "dit", "lcom", "loc", "locComment"]

    for file in os.listdir(CK_RESULTS_DIR):
        if file.endswith("_class.csv"):
            repo_key = file.replace("_class.csv", "")
            repo_fullname = repo_map.get(repo_key)

            if not repo_fullname:
                print(f"⚠️ Não encontrei {repo_key} em {REPO_LIST_FILE}, pulando...")
                continue

            path = os.path.join(CK_RESULTS_DIR, file)
            df = pd.read_csv(path)

            # Seleciona apenas as métricas disponíveis
            available = [col for col in wanted if col in df.columns]
            metrics = df[available]
            mean_metrics = metrics.mean().to_dict()

            # Garante que todas as métricas existam
            for col in wanted:
                if col not in mean_metrics:
                    mean_metrics[col] = 0

            print(f"📊 {repo_fullname} → métricas extraídas: {mean_metrics}")

            # Buscar info do GitHub
            repo_info = get_repo_info(repo_fullname)
            if repo_info:
                stars, releases, idade = repo_info
            else:
                stars, releases, idade = 0, 0, 0

            rows.append({
                "repo": repo_fullname,
                "stars": stars,
                "releases": releases,
                "idade_anos": idade,
                "cbo": mean_metrics["cbo"],
                "dit": mean_metrics["dit"],
                "lcom": mean_metrics["lcom"],
                "loc": mean_metrics["loc"],
                "locComment": mean_metrics["locComment"],
            })

    df_final = pd.DataFrame(rows)
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ CSV unificado gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_ck_results()
