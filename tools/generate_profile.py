#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the metadata-only exact Rechiseled/Fusion rendering profile.

The generator consumes the operator-supplied, hash-pinned runtime artifacts.
It emits only identities, hashes, allowlists, and compact format metadata; no
third-party JSON, model, texture, class, source, or binary is redistributed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
from typing import Any, Iterable
import zipfile


PROFILE_ROOT = Path("src/main/resources/bluemap-rechiseled/profiles")
PROFILE_DIRECTORY = PROFILE_ROOT / "rechiseled/1.2.5-fusion-1.3.12"
CATALOG_PATH = PROFILE_ROOT / "exact-artifacts.json"
PROFILE_PATH = PROFILE_DIRECTORY / "profile.json"
DEFINITIONS_PATH = PROFILE_DIRECTORY / "definitions.tsv"
RESOURCES_PATH = PROFILE_DIRECTORY / "required-resources.tsv"
TEXTURES_PATH = PROFILE_DIRECTORY / "textures.tsv"
HOST_MODELS_PATH = PROFILE_DIRECTORY / "host-models.tsv"

RECHISELED_FILENAME = "rechiseled-1.2.5-neoforge-mc1.21.jar"
RECHISELED_SIZE = 11_498_611
RECHISELED_SHA1 = "ed2973c6952caa3173259314276b5b9d72880494"
RECHISELED_SHA256 = "7bf14cf8a4bfdc4b6c990126a75da29fd2bb7559d1c05b71e29c8fd5ae044435"
RECHISELED_SHA512 = (
    "d849bc3e775577978bbf96dccee11b0904fa928c556a12e05adf759edab9479bd"
    "757f490380475e974eaa137c566ffe8bfb62d5df19f966dfd99b67a2fe0ee9b"
)
FUSION_FILENAME = "fusion-1.3.12-neoforge-mc1.21.1.jar"
FUSION_SIZE = 923_270
FUSION_SHA1 = "79c0c6b6a2d9c9a04298df9a88bb71a93e885235"
FUSION_SHA256 = "17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa"
FUSION_SHA512 = (
    "a13d2a654988f021106f8a455134da1b515872e9122cf70bda064e663749f1c11"
    "aeddc3def23a621e236f2ffeefb6f56b15c2c63eeb2bca5f9833c5a2dc23a93"
)

ALL_BLOCKSTATES_COUNT = 3_627
ROUTED_COUNT = 1_743
STOCK_COUNT = 1_884
ROUTED_STATE_COUNT = 50_571
STOCK_STATE_COUNT = 54_660
DIRECT_MODEL_COUNT = 5_822
MODEL_COUNT = 5_825
PNG_COUNT = 593
MCMETA_COUNT = 590
RESOURCE_COUNT = 8_751
HOST_MODEL_COUNT = 7
ROUTED_DIGEST = "39fb40488844ce35c7f070a4250189e6d61f8769eeb534e6127c355119c9a039"
STOCK_DIGEST = "e5dff72c30c5b758ab5f7e5dfd6bc66b191d76a9d4293daf9108b433d7594cca"
MODEL_DIGEST = "556da4531ffd7255983d660340408027d8325d10b7d63a08d913a2aebaf1889b"
PNG_DIGEST = "c335d7c95314c22bd765f905d425cc8ddbb85b5e2ea9993faac417a627ddbc8b"
MCMETA_DIGEST = "c190ad13ce12d4c1d38e103bddb8eefdcbd96266028d439d43db322f67a13860"
PATH_CLOSURE_DIGEST = "8ebc0ffb63cd675afa5aa3d0f8bb90e3861b3286efb42950bee0a38a812609d3"
LEGAL_STATE_DIGEST = "f2c433df876a79bd3f38406b48367dddd8514ce651514f6c449e2256a5871397"
MINECRAFT_CLIENT_SHA256 = (
    "499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99"
)
HOST_MODELS = (
    ("assets/minecraft/models/block/block.json", 997,
     "3ef6c442f1ab55d2a57fa58e28bb831268159052659f12b453b637b31ded1da8"),
    ("assets/minecraft/models/block/cube.json", 584,
     "3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"),
    ("assets/minecraft/models/block/inner_stairs.json", 1_755,
     "fcb56ce59da95e5c1a77e49149caa3c72c18195141554a2c063d24b7962648d8"),
    ("assets/minecraft/models/block/outer_stairs.json", 1_271,
     "39142eb37d9e9d9ff2404404af460d85b3109bf0c59898c21c676719c3e16ef8"),
    ("assets/minecraft/models/block/slab.json", 761,
     "bd869ebe3ba380d46349e5c6e988b9b1ccf1ab25212ab1de66e2fdcc067edc1d"),
    ("assets/minecraft/models/block/slab_top.json", 733,
     "c02e81cd0b59698040db7a682d32d08ddeb0de64756e309d62ecfbda4af804f9"),
    ("assets/minecraft/models/block/stairs.json", 1_806,
     "962dc154fd3337d6b7e165e2b734e171c4b3595c2b838a5da1e01f5bdcdcae3b"),
)

LAYOUTS = {
    "pieced": (499, 80, 16),
    "full": (43, 128, 128),
    "horizontal": (36, 64, 16),
    "vertical": (8, 16, 64),
    "simple": (4, 64, 64),
}
PREDICATE_TYPES = {
    "fusion:or",
    "fusion:and",
    "fusion:is_direction",
    "fusion:match_block",
    "fusion:match_state",
    "fusion:is_same_state",
}


def digest_bytes(raw: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, raw).hexdigest()


def digest_path(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def roster_digest(values: Iterable[str]) -> str:
    payload = "".join(f"{value}\n" for value in sorted(values)).encode("utf-8")
    return digest_bytes(payload)


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode(
        "ascii"
    )


def resource_path(key: str, kind: str, suffix: str) -> str:
    if ":" in key:
        namespace, value = key.split(":", 1)
    else:
        namespace, value = "minecraft", key
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe resource key: {key}")
    return f"assets/{namespace}/{kind}/{value}{suffix}"


def _verify_identity(
    path: Path, *, filename: str, size: int, sha1: str, sha256: str, sha512: str
) -> None:
    if not path.is_file() or path.name != filename:
        raise ValueError(f"unexpected artifact path: {path}")
    if path.stat().st_size != size:
        raise ValueError(f"unexpected artifact size for {path}")
    for algorithm, expected in (
        ("sha1", sha1),
        ("sha256", sha256),
        ("sha512", sha512),
    ):
        actual = digest_path(path, algorithm)
        if actual != expected:
            raise ValueError(
                f"{path.name} {algorithm} changed: got {actual}, expected {expected}"
            )


def _model_key(value: str, default_namespace: str = "minecraft") -> str:
    return value if ":" in value else f"{default_namespace}:{value}"


def _path_for_model(model: str) -> str:
    namespace, value = model.split(":", 1)
    return f"assets/{namespace}/models/{value}.json"


def _path_for_texture(texture: str, suffix: str = ".png") -> str:
    namespace, value = texture.split(":", 1)
    return f"assets/{namespace}/textures/{value}{suffix}"


def _walk_predicate(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        predicate_type = value.get("type")
        if isinstance(predicate_type, str) and predicate_type.startswith("fusion:"):
            found.add(predicate_type)
        for child in value.values():
            _walk_predicate(child, found)
    elif isinstance(value, list):
        for child in value:
            _walk_predicate(child, found)


def _shape_and_states(block: str, variants: dict[str, Any]) -> tuple[str, int, list[str]]:
    selector_keys = sorted(variants)
    if block.endswith("_slab_connecting"):
        if {key.split("=", 1)[0] for key in selector_keys} != {"type"}:
            raise ValueError(f"{block} slab selectors changed")
        shape, count = "slab", 6
    elif block.endswith("_stairs_connecting"):
        properties = {
            assignment.split("=", 1)[0]
            for key in selector_keys
            for assignment in key.split(",")
        }
        if properties != {"facing", "half", "shape"}:
            raise ValueError(f"{block} stair selectors changed")
        shape, count = "stairs", 80
    elif selector_keys == [""]:
        shape, count = "full", 1
    elif selector_keys == ["axis=x", "axis=y", "axis=z"]:
        shape, count = "axis", 3
    else:
        raise ValueError(f"{block} has an unsupported selector schema")
    return shape, count, selector_keys


def _legal_states(block_id: str, shape: str, selectors: list[str]) -> list[str]:
    rows: list[str] = []
    if shape in {"slab", "stairs"}:
        for selector in selectors:
            properties = selector.split(",") + ["waterlogged=false"]
            rows.append(f"{block_id}\t{','.join(sorted(properties))}")
            properties[-1] = "waterlogged=true"
            rows.append(f"{block_id}\t{','.join(sorted(properties))}")
    else:
        for selector in selectors:
            properties = [] if selector == "" else selector.split(",")
            rows.append(f"{block_id}\t{','.join(sorted(properties))}")
    return rows


def build_outputs(rechiseled: Path, fusion: Path) -> dict[Path, bytes]:
    _verify_identity(
        rechiseled,
        filename=RECHISELED_FILENAME,
        size=RECHISELED_SIZE,
        sha1=RECHISELED_SHA1,
        sha256=RECHISELED_SHA256,
        sha512=RECHISELED_SHA512,
    )
    _verify_identity(
        fusion,
        filename=FUSION_FILENAME,
        size=FUSION_SIZE,
        sha1=FUSION_SHA1,
        sha256=FUSION_SHA256,
        sha512=FUSION_SHA512,
    )

    definitions: list[str] = []
    legal_states: list[str] = []
    routed_paths: list[str] = []
    stock_paths: list[str] = []
    direct_models: set[str] = set()
    model_paths: set[str] = set()
    texture_keys: set[str] = set()
    png_paths: set[str] = set()
    metadata_paths: set[str] = set()
    predicate_types: set[str] = set()
    layouts: dict[str, tuple[str, int, int, str]] = {}

    with zipfile.ZipFile(rechiseled) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Rechiseled JAR contains duplicate ZIP entries")
        available = set(names)
        blockstate_paths = sorted(
            path
            for path in available
            if path.startswith("assets/rechiseled/blockstates/")
            and path.endswith(".json")
        )
        if len(blockstate_paths) != ALL_BLOCKSTATES_COUNT:
            raise ValueError("Rechiseled blockstate count changed")

        for path in blockstate_paths:
            block = path.removeprefix("assets/rechiseled/blockstates/").removesuffix(
                ".json"
            )
            if block.endswith("_connecting"):
                routed_paths.append(path)
                value = json.loads(archive.read(path))
                if set(value) != {"variants"} or not isinstance(
                    value["variants"], dict
                ):
                    raise ValueError(f"{path} blockstate schema changed")
                shape, state_count, selectors = _shape_and_states(
                    block, value["variants"]
                )
                variant_models: set[str] = set()
                for variant in value["variants"].values():
                    variants = variant if isinstance(variant, list) else [variant]
                    if len(variants) != 1 or not isinstance(variants[0], dict):
                        raise ValueError(f"{path} weighted variant changed")
                    model = variants[0].get("model")
                    if not isinstance(model, str):
                        raise ValueError(f"{path} model selector changed")
                    variant_models.add(_model_key(model, "rechiseled"))
                direct_models.update(variant_models)
                block_id = f"rechiseled:{block}"
                legal_states.extend(_legal_states(block_id, shape, selectors))
                definitions.append(
                    "\t".join(
                        (
                            block_id,
                            shape,
                            str(state_count),
                            digest_bytes(archive.read(path)),
                            digest_bytes(
                                "".join(f"{model}\n" for model in sorted(variant_models)).encode(
                                    "ascii"
                                )
                            ),
                        )
                    )
                )
            else:
                stock_paths.append(path)

        if len(routed_paths) != ROUTED_COUNT or roster_digest(routed_paths) != ROUTED_DIGEST:
            raise ValueError("Rechiseled routed roster changed")
        if len(stock_paths) != STOCK_COUNT or roster_digest(stock_paths) != STOCK_DIGEST:
            raise ValueError("Rechiseled stock roster changed")
        if len(direct_models) != DIRECT_MODEL_COUNT:
            raise ValueError("Rechiseled direct Fusion model roster changed")

        pending = list(direct_models)
        visited_models: set[str] = set()
        while pending:
            model = pending.pop()
            if model in visited_models or not model.startswith("rechiseled:"):
                continue
            visited_models.add(model)
            path = _path_for_model(model)
            if path not in available:
                raise ValueError(f"missing Rechiseled model {path}")
            model_paths.add(path)
            value = json.loads(archive.read(path))
            parent = value.get("parent")
            if isinstance(parent, str):
                parent_model = _model_key(parent, "rechiseled")
                if parent_model.startswith("rechiseled:"):
                    pending.append(parent_model)
            for texture in value.get("textures", {}).values():
                if isinstance(texture, str) and not texture.startswith("#"):
                    texture_keys.add(_model_key(texture, "rechiseled"))
            if model in direct_models:
                if value.get("type") != "fusion:connecting" or value.get(
                    "loader"
                ) != "fusion:model":
                    raise ValueError(f"{path} Fusion model schema changed")
                if not isinstance(value.get("connections"), dict):
                    raise ValueError(f"{path} Fusion connections changed")
                _walk_predicate(value["connections"], predicate_types)

        if len(model_paths) != MODEL_COUNT or roster_digest(model_paths) != MODEL_DIGEST:
            raise ValueError("Rechiseled model closure changed")
        if predicate_types != PREDICATE_TYPES:
            raise ValueError("Fusion predicate type roster changed")

        for texture in sorted(texture_keys):
            png = _path_for_texture(texture)
            if png not in available:
                raise ValueError(f"missing Rechiseled texture {png}")
            png_paths.add(png)
            raw = archive.read(png)
            if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
                raise ValueError(f"invalid PNG {png}")
            width, height = struct.unpack(">II", raw[16:24])
            metadata = f"{png}.mcmeta"
            if metadata in available:
                metadata_paths.add(metadata)
                meta = json.loads(archive.read(metadata))
                fusion_meta = meta.get("fusion") if isinstance(meta, dict) else None
                if not isinstance(fusion_meta, dict) or set(fusion_meta) not in (
                    {"connections", "type"},
                    {"connections", "layout", "type"},
                ):
                    raise ValueError(f"{metadata} Fusion metadata schema changed")
                layout = fusion_meta.get("layout", "full")
                if fusion_meta.get("type") != "connecting" or fusion_meta.get(
                    "connections"
                ) != {"type": "false"}:
                    raise ValueError(f"{metadata} Fusion metadata value changed")
                if layout not in LAYOUTS:
                    raise ValueError(f"{metadata} layout changed")
                layouts[texture] = (
                    layout,
                    width,
                    height,
                    digest_bytes(archive.read(metadata)),
                )
            else:
                layouts[texture] = ("plain", width, height, "-")

        if len(png_paths) != PNG_COUNT or roster_digest(png_paths) != PNG_DIGEST:
            raise ValueError("Rechiseled PNG roster changed")
        if len(metadata_paths) != MCMETA_COUNT or roster_digest(metadata_paths) != MCMETA_DIGEST:
            raise ValueError("Rechiseled Fusion metadata roster changed")
        observed_layouts = {
            layout: sum(1 for row in layouts.values() if row[0] == layout)
            for layout in LAYOUTS
        }
        if observed_layouts != {key: value[0] for key, value in LAYOUTS.items()}:
            raise ValueError("Rechiseled Fusion layout counts changed")
        for texture, (layout, width, height, _digest) in layouts.items():
            if layout != "plain" and (width, height) != LAYOUTS[layout][1:]:
                raise ValueError(f"{texture} dimensions changed for {layout}")

        closure = sorted(
            routed_paths + list(model_paths) + list(png_paths) + list(metadata_paths)
        )
        if len(closure) != RESOURCE_COUNT or roster_digest(closure) != PATH_CLOSURE_DIGEST:
            raise ValueError("Rechiseled exact resource closure changed")
        resource_rows = []
        for path in closure:
            if "/blockstates/" in path:
                kind = "blockstate"
            elif "/models/" in path:
                kind = "model"
            elif path.endswith(".png.mcmeta"):
                kind = "metadata"
            else:
                kind = "texture"
            raw = archive.read(path)
            resource_rows.append(
                f"{kind}\t{path}\t{len(raw)}\t{digest_bytes(raw)}"
            )

    if len(legal_states) != ROUTED_STATE_COUNT or digest_bytes(
        "".join(f"{row}\n" for row in sorted(legal_states)).encode("ascii")
    ) != LEGAL_STATE_DIGEST:
        raise ValueError("Rechiseled routed legal-state roster changed")

    definitions_raw = ("\n".join(sorted(definitions)) + "\n").encode("ascii")
    resources_raw = ("\n".join(resource_rows) + "\n").encode("ascii")
    textures_raw = (
        "\n".join(
            "\t".join((texture, layout, str(width), str(height), meta_digest))
            for texture, (layout, width, height, meta_digest) in sorted(layouts.items())
        )
        + "\n"
    ).encode("ascii")
    host_models_raw = (
        "\n".join(
            f"model\t{path}\t{size}\t{sha256}"
            for path, size, sha256 in HOST_MODELS
        )
        + "\n"
    ).encode("ascii")
    if len(HOST_MODELS) != HOST_MODEL_COUNT:
        raise ValueError("host geometry ABI roster changed")

    catalog = {
        "schema": 1,
        "artifacts": [
            {
                "modId": "rechiseled",
                "version": "1.2.5",
                "filename": RECHISELED_FILENAME,
                "size": RECHISELED_SIZE,
                "sha1": RECHISELED_SHA1,
                "sha256": RECHISELED_SHA256,
                "sha512": RECHISELED_SHA512,
            },
            {
                "modId": "fusion",
                "version": "1.3.12",
                "filename": FUSION_FILENAME,
                "size": FUSION_SIZE,
                "sha1": FUSION_SHA1,
                "sha256": FUSION_SHA256,
                "sha512": FUSION_SHA512,
            },
        ],
        "requiredForStaticRendering": ["rechiseled", "fusion"],
    }
    profile = {
        "schema": 1,
        "profileId": "rechiseled-fusion-1.2.5-1.3.12",
        "namespaceOwner": "rechiseled",
        "formatOwner": "fusion",
        "counts": {
            "allBlockstates": ALL_BLOCKSTATES_COUNT,
            "routedBlocks": ROUTED_COUNT,
            "stockBlocks": STOCK_COUNT,
            "routedLegalStates": ROUTED_STATE_COUNT,
            "stockLegalStates": STOCK_STATE_COUNT,
            "directFusionModels": DIRECT_MODEL_COUNT,
            "modelClosure": MODEL_COUNT,
            "textures": PNG_COUNT,
            "fusionMetadata": MCMETA_COUNT,
            "resourceClosure": RESOURCE_COUNT,
            "hostGeometryModels": HOST_MODEL_COUNT,
        },
        "shapes": {"full": 569, "axis": 12, "slab": 581, "stairs": 581},
        "layouts": {key: value[0] for key, value in LAYOUTS.items()},
        "predicateTypes": sorted(PREDICATE_TYPES),
        "digests": {
            "routedRoster": ROUTED_DIGEST,
            "stockRoster": STOCK_DIGEST,
            "legalStateRoster": LEGAL_STATE_DIGEST,
            "modelRoster": MODEL_DIGEST,
            "pngRoster": PNG_DIGEST,
            "metadataRoster": MCMETA_DIGEST,
            "resourcePathClosure": PATH_CLOSURE_DIGEST,
            "definitions": digest_bytes(definitions_raw),
            "requiredResources": digest_bytes(resources_raw),
            "textures": digest_bytes(textures_raw),
            "hostGeometryModels": digest_bytes(host_models_raw),
        },
        "hostGeometryAbi": {
            "owner": "minecraft",
            "clientJarSha256": MINECRAFT_CLIENT_SHA256,
            "pathsAreOutsideRechiseledClosure": True,
        },
        "failurePolicy": "route-wide-inactive-or-atomic-stock-fallback",
        "assetPolicy": "operator-installed-only",
    }
    return {
        CATALOG_PATH: canonical_json(catalog),
        PROFILE_PATH: canonical_json(profile),
        DEFINITIONS_PATH: definitions_raw,
        RESOURCES_PATH: resources_raw,
        TEXTURES_PATH: textures_raw,
        HOST_MODELS_PATH: host_models_raw,
    }


def write_or_check(outputs: dict[Path, bytes], check: bool) -> str:
    changed: list[str] = []
    for path, raw in outputs.items():
        if not path.is_file() or path.read_bytes() != raw:
            changed.append(str(path))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
    if check and changed:
        raise ValueError("generated profile is stale: " + ", ".join(changed))
    return "verified" if check else "generated"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rechiseled", required=True, type=Path)
    parser.add_argument("--fusion", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    outputs = build_outputs(arguments.rechiseled, arguments.fusion)
    action = write_or_check(outputs, arguments.check)
    print(f"{action} exact Rechiseled/Fusion profile ({ROUTED_COUNT} routed blocks)")


if __name__ == "__main__":
    main()
