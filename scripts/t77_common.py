"""t77 common helpers: paths, hashing, JSON IO, ledger claim digests.

No payload/EXE decoding here: v11 is a merge of accepted artifacts only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
OTHER_JSON = ROOT / "reports" / "other_tables_schema.json"
DENOM_JSON = ROOT / "reports" / "xml_denominator_coverage.json"
LEDGER = ROOT / "scratch" / "t01" / "LEDGER.json"
OUT = ROOT / "scratch" / "t77" / "out"

# Pinned v10 baseline (public file == scratch/t70/out/...v10.json, verified 2026-11-21).
BASE_JSON_SHA256 = "7c35160827875c5ce295701950747482c61dd0c9862658459e6a3765e0882515"
BASE_MD_SHA256 = "b9ba0bb3efc2d43baac697bdec76d548243ef9c5da094377eacfc46799b5c051"

# Accepted source artifacts: path -> (sha256, bytes). Recomputed at --verify time.
SOURCE_SHA256: dict[str, tuple[str, int]] = {
    "scratch/t71/out/field_map_r3.json": ("5e5a869acbb4a545ff1f27ef346952547b3d92ce052db6a51ce7390b552dfe75", 154039),
    "scratch/t71/out/rows_extra3.json": ("df809f45cdd7329f005144d3a90ec316c4ee1ebd7f16e751f9d082d68914ca38", 43252),
    "scratch/t71/out/chain.json": ("c001f0d22db79b144760d614c69f21c3812a66de714e3ebeee0f3e35acd09534", 1091684),
    "scratch/t71/out/REPORT.md": ("950cb77cca017b591ae823b35a5398aeab8cfd44f290844b9c9b2219df683375", 9761),
    "scratch/t71/out/DONE.md": ("f9e060351ab246b15fdda132dffebd2d91db229e9ee7078a855bf6e954049765", 1138),
    "scratch/t71/out/verify.py": ("65295f3305716f46687059be3aa815490750eb12d98b491fa6c833642ca26ff5", 28719),
    "scratch/t72/out/inventory.json": ("fa9a637de37a772e9858edda369a8aeb82b4e877baadcf5328202df5f76ead16", 82465),
    "scratch/t72/out/fingerprints.json": ("0bf505a5fb256bf9e49f2cd7139aa3cd7a345145ebd1e255c56f5938396eb48b", 470891),
    "scratch/t72/out/REPORT.md": ("0f404ee03b903d3ab179ec5a1b8b9fe82c169a082e4b7439481d631aa5ec203a", 2223),
    "scratch/t72/out/DONE.md": ("dff0f1d8f511085c30a24359ff2a325495ab361ebc1583e883f1c91c3464b7a9", 192),
    "scratch/t73/out/frames.json": ("113b0d7aa4063274d115f6e8dba6ec054cf2e1526843761e8795c0aae46a0443", 4991),
    "scratch/t73/out/slots_client_2.json": ("025e2f0c85817e4392da40cb40232bc5f607d09e61e66715ecfcf66520ce26e4", 35674),
    "scratch/t73/out/slots_client_5.json": ("f7926d7ddfbab1de0ce304a63e6b4ca17821cbc42d7bcb0568bdcf4c938c1d9b", 17328),
    "scratch/t73/out/slots_client_19.json": ("87418ded7cec5ff66efd7a070e33e829e649910bb5a6cd31b5fa428d7837f72c", 25892),
    "scratch/t73/out/slots_client_41.json": ("2e85a55e41351cb9692fc5688545d04a10c88dace9220bc350158a22a1446dda", 4872),
    "scratch/t73/out/slots_server_2.json": ("ef1b07f684acb550e0180c36322747e7bfa1580e02d56f880d017037de327ef4", 36415),
    "scratch/t73/out/slots_server_5.json": ("5f3be91de41251635d3e3b6be4cb8e44940ef4267f3d6ba46aa5dee5337edaa9", 20469),
    "scratch/t73/out/slots_server_19.json": ("c2df07f49c915f632a4ff03270e308af9cb7c0ac80fac3f5dce4c8dc3602d708", 25241),
    "scratch/t73/out/slots_server_41.json": ("0f05b4d28e3e8c7be3dc0774e00fc544bf400bce202214151de2989165d02af3", 4872),
    "scratch/t73/out/REPORT.md": ("68161f81410a56ab5beac7044972d44f798131a2b7ca4233e200297988b324ab", 8947),
    "scratch/t73/out/DONE.md": ("c8e13b8072ed8504b41b52004776fef09dbaee54be561140acdc9a9179982d72", 2115),
    "scratch/t73/out/verify.py": ("70b79eb4771b83e1306b6cbb8c6867053e100128e14be81b7e481f1ad56b7ad4", 7410),
    "scratch/t74/out/frames.json": ("02a39cc6be58894e226453828aa0f151df27cd9e9dc409f8897522853aaa7535", 23120),
    "scratch/t74/out/sensitivity.json": ("13c151a10947650a4eeea2d2fbba263f56d8c7a3408378e643ed63027e606717", 4026),
    "scratch/t74/out/REPORT.md": ("061daa594d5d5f7a69c7172f0d847549f316aeb333e9236f3a3ab5aa31921165", 6183),
    "scratch/t74/out/DONE.md": ("fc3c5ed57a44d47c56a53103c17cc62516ec680726d7e1d2e7caaf7493b71881", 1751),
    "scratch/t74/out/verify.py": ("a20e6fbc8062b212b690149f3439128bc4b85173d4985c76be391cc04b099951", 11328),
    "scratch/t75/out/field_map_r3.json": ("5ea3b351f26c325d8a275f267670bf36f3b3fbafc4822065b4b930c0764aa9f5", 77453),
    "scratch/t75/out/xref_reverse.json": ("6c0cb868484d7cae7cbd8fe315fd66c96b1f3048ac3791958223d5cc1a4f4987", 1332142),
    "scratch/t75/out/REPORT.md": ("200cbde763e1801d838864381b06ea161cfc33bd8130651dc6fbc58c118511ed", 8737),
    "scratch/t75/out/DONE.md": ("eb1bb39cb99f4bf376d309b27ac0c38e95c1d345878e9a687b3b8dea39962bcd", 526),
    "scratch/t75/out/verify.py": ("56f7fbb5ffeb6dc0982d2651bbabdd1d9f625ce47b98ef0380cec7ea967f6734", 27810),
    "scratch/t76a/out/slots_client_21.json": ("30e0060a9b0f61ba54d4db25a30d416592c1149f56770745c5fc3b796af2acb5", 20228),
    "scratch/t76a/out/slots_server_21.json": ("a161cb20e1e5457b05588a8a2e08aef8c08b5e075d63403c50fc27cdd46f9e4a", 150930),
    "scratch/t76a/out/verify.json": ("ea2dbc4b09379235191fb980e84a0a4eb46e579c2cf9cc022cddc0a8f47ac93b", 6266),
    "scratch/t76a/out/REPORT.md": ("efbb8de03e78b67fae0c90ce6f84bf5db0802de87a3fc65df40b801decf7c4d3", 8293),
    "scratch/t76a/out/DONE.md": ("37ac05bbc4683c847b9c957a64eaff7506ad4a4f537867b5755c8aae6bba85e4", 2522),
    "scratch/t76a/out/verify.py": ("7b1b9e47a9e3757d4b8161ce922a8d071cb14949ebc7e0c64648a6fd5385e8ae", 12097),
    "scratch/t76c/out/slots_client_18.json": ("8d4baf9c3333fcde6bbf25789a5f0dd852d1fc0e1399a87f7de71841d3725a5b", 6621),
    "scratch/t76c/out/slots_client_27.json": ("27cd9afc57f6078118950d1f5737a81089b5bd137eaaf2ae99e7a036207b5c94", 15665),
    "scratch/t76c/out/slots_client_47.json": ("cb02a379aa2e734798bc7bce926f323cc40b11d0d5f8965e48c5effd55b1141d", 7040),
    "scratch/t76c/out/slots_client_56.json": ("4155fcdd8b60a3053524d7c44e349c93a86525c8a5791c5e5e3f292efb0beb96", 3615),
    "scratch/t76c/out/slots_server_18.json": ("4a988e44dfcd95a69db1f56dac571c7b701efd8663f57406631cd40b8ad36062", 7611),
    "scratch/t76c/out/slots_server_27.json": ("c6034b61d5945109f6b50b59b82ef6051e1305ed23efaeaad5d850f4d4f61a43", 15623),
    "scratch/t76c/out/slots_server_47.json": ("866a08c6429f9fa3fd0eb0b6806b1bb19bcdce31e0445ea46cb58c42ad971fc6", 7022),
    "scratch/t76c/out/slots_server_56.json": ("73c5a71d63d21008bab565da20b137d81529143c10782682cbbbe83abaaa656a", 3615),
    "scratch/t76c/out/REPORT.md": ("df88300f99b3b0a4e8d4121f594cc35b755ef78e2281c027db50a519ec29ff40", 11498),
    "scratch/t76c/out/DONE.md": ("fe77daed673ff9f7360a5b5abc960e9bc2676ed6d17247e4da18752ed9b22add", 3315),
    "scratch/t76c/out/verify.py": ("5568899ef0f5ae73d65b7858877421edb00996856be924e267902fd02f280527", 16501),
    "scratch/t78/out/buckets.json": ("911f1adb3f141d0b306f5e8461a97146096768bad5bc87a4c013b24843754e35", 247252),
    "scratch/t78/out/coverage.md": ("2ac89e5a368722a326a9b7bb6539860c93a5cd9f00ff38c13a2a024642e3a3ba", 3663),
    "scratch/t78/out/DONE.md": ("0fc01193041c27c213f64275b14740b6a3201cbae3c04887a7018668000c5471", 226),
    "scratch/t79/out/field_map.json": ("260a30d5308415fb0640361852435c0466ff7884450f5805b69c50674bfe6854", 84264),
    "scratch/t79/out/xref_stad_team.json": ("3dce37eed69383c5069e9820017ad0521033a9daad22f481a4e81c084a32d26a", 57161),
    "scratch/t79/out/REPORT.md": ("ff8aac769a94b3ae2d29688eec6e5d220e20db2baec04b7554a7bd1f82fa1835", 19827),
    "scratch/t79/out/DONE.md": ("2cb3f2375bf94202d32b4a7ee616df8916018db414ab679d6582d1d147737d28", 1469),
    "scratch/t79/out/verify.py": ("4cd9a5dd664414990902612138cbd0c4f94229903da4591866491b7b5ea15fd2", 29921),
}

# Guarded acceptance entries for this fold. E121 (t82) landed after this lane
# departed and is left to t87; E111-E120 are guarded here.
GUARDED_IDS = tuple(f"E{i}" for i in range(111, 121))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return sha(raw)


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def artifact(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": rel(path), "sha256": sha(raw), "bytes": len(raw)}


def artifacts(*paths: str) -> list[dict[str, Any]]:
    return [artifact(ROOT / p) for p in paths]


def ledger_entries() -> dict[str, dict[str, Any]]:
    found = {}
    for item in read_json(LEDGER)["entries"]:
        if item.get("id") in GUARDED_IDS:
            found[item["id"]] = item
    return found


def ledger_record(item: dict[str, Any]) -> dict[str, Any]:
    return {"kind": item["kind"], "level": item["level"],
            "claim_sha256": canonical_sha256(item["claim"])}


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


class CheckFailure(Exception):
    pass
