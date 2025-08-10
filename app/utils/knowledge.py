from typing import List, Dict
from pathlib import Path

def build_metadatas(chunks: List[str], source: str) -> List[Dict]:
    metas = []
    for i, c in enumerate(chunks):
        metas.append({"text": c, "source": f"{source}#chunk-{i}"})
    return metas