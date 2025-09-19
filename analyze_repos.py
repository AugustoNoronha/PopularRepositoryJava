import os
import subprocess
import shutil
import sys
import stat

GITHUB_TOKEN = "xxxxxxxxxxxxx"

def read_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def write_progress(progress_file, index):
    with open(progress_file, "w") as f:
        f.write(str(index))

def handle_remove_readonly(func, path, exc):
    """Força a exclusão de arquivos somente leitura no Windows"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def analyze_repos(repo_list_file, ck_jar, out_dir, clone_dir="clones", progress_file="progress.txt"):
    if not os.path.exists(ck_jar):
        print(f"Arquivo JAR do CK não encontrado: {ck_jar}")
        sys.exit(1)

    try:
        subprocess.run(["java", "-version"], check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("O Java não está instalado ou não está no PATH.")
        print("   Instale o Java 17 e tente novamente.")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(clone_dir, exist_ok=True)

    with open(repo_list_file, "r") as f:
        repos = [line.strip() for line in f if line.strip()]

    start_index = read_progress(progress_file)
    print(f"Retomando do índice {start_index} de {len(repos)} repositórios")

    for i, repo in enumerate(repos[start_index:], start=start_index):
        print(f"\n=== [{i+1}/{len(repos)}] Processing {repo} ===")
        repo_name = repo.replace("/", "_")
        repo_dir = os.path.join(clone_dir, repo_name)

        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir, onerror=handle_remove_readonly)

        clone_url = f"https://{GITHUB_TOKEN}@github.com/{repo}.git"
        cmd_clone = ["git", "clone", "--depth", "1", clone_url, repo_dir]
        result = subprocess.run(cmd_clone, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Clone failed: {repo}")
            print(result.stderr)
            continue

        print(f"Executando CK em {repo_dir}...")
        subprocess.run(["java", "-jar", ck_jar, repo_dir, "0"])

        for csv in ["class.csv", "method.csv", "variable.csv", "field.csv"]:
            if os.path.exists(csv):
                new_name = os.path.join(out_dir, f"{repo_name}_{csv}")
                shutil.move(csv, new_name)
                print(f"{csv} salvo como {new_name}")

        # força remoção no Windows (sem PermissionError)
        shutil.rmtree(repo_dir, onerror=handle_remove_readonly)
        print(f"Repositório {repo} deletado")

        # salva progresso
        write_progress(progress_file, i + 1)

if __name__ == "__main__":
    analyze_repos(
        repo_list_file="java_repos_list.txt",
        ck_jar=r"D:\ck\target\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar",
        out_dir="ck_results"
    )
