import subprocess

# NOT WORKING

def run_dolt_command(args, cwd="."):
    result = subprocess.run(["dolt"] + args, cwd=cwd, text=True,
                            capture_output=True, check=True)
    return result.stdout.strip()

db_dir = "/db"

commit_hash = "5bco52coadmprgsg50e9hd71mcp54db2"
run_dolt_command(["checkout", commit_hash], cwd=db_dir)

branch_name = "detached-head-branch"
run_dolt_command(["checkout", "-b", branch_name], cwd=db_dir)

print(f"Checked out commit {commit_hash} and created branch '{branch_name}'")
