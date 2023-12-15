from lean_dojo import *
repo = LeanGitRepo(
    #  mathlib的地址
    "https://github.com/leanprover-community/mathlib4",
    # 一个具体的版本
    "3ce43c18f614b76e161f911b75a3e1ef641620ff",
)
repo.get_config("lean-toolchain")
# A few minutes if the traced repo is in the cache; many hours otherwise.
traced_repo = trace(repo)