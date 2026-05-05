#!/usr/bin/env python3
"""
Decode and patch StarLoco / Dofus 1.29 mapData.

Features
--------
- Decode mapData into one row per cell
- Optionally decrypt encrypted hex mapData using maps.key
- Export decoded cells to stdout / CSV / JSON
- Patch a single cell and print the full updated mapData to stdout
- Optionally write the updated mapData to a file
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional


HASH_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


@dataclass
class DecodedCell:
    cell_id: int
    raw_chunk: str
    active: int
    line_of_sight: int
    movement: int
    ground_level: int
    ground_slope: int
    ground_num: int
    ground_flip: int
    ground_rot: int
    object1_num: int
    object1_flip: int
    object1_rot: int
    object2_num: int
    object2_flip: int
    object2_interactive: int

    @property
    def likely_walkable(self) -> bool:
        return self.active == 1 and self.movement != 0

    @property
    def has_visible_content(self) -> bool:
        return any([
            self.object1_num != 0,
            self.object2_num != 0,
            self.object2_interactive != 0,
        ])


def get_int_by_hashed_value(ch: str) -> int:
    idx = HASH_ALPHABET.find(ch)
    if idx == -1:
        raise ValueError(f"Invalid hashed map character: {ch!r}")
    return idx


def get_hashed_value_by_int(value: int) -> str:
    if not 0 <= value < len(HASH_ALPHABET):
        raise ValueError(f"Hashed value out of range: {value}")
    return HASH_ALPHABET[value]


def prepare_key(hex_key: str) -> str:
    raw = bytes.fromhex(hex_key)
    return urllib.parse.unquote(raw.decode("utf-8"))


def checksum_key(data: str) -> str:
    total = 0
    for ch in data:
        total += ord(ch) % 16
    return "0123456789ABCDEF"[total % 16]


def decrypt_map_data(map_data: str, key: str) -> str:
    prepared_key = prepare_key(key)
    checksum = int(checksum_key(prepared_key), 16) * 2

    chars = []
    for i in range(0, len(map_data), 2):
        sub = map_data[i:i + 2]
        num = int(sub, 16)
        s = int(round((((i) / 2) + checksum) % len(prepared_key)))
        num2 = ord(prepared_key[s:s + 1])
        chars.append(chr(num ^ num2))
    return "".join(chars).encode("utf-8", "surrogatepass").decode("unicode_escape")


def is_map_ciphered(map_data: str) -> bool:
    return sum(ch.isdigit() for ch in map_data) > 1000


def expected_cell_count(width: int, height: int) -> int:
    return width * height + (width - 1) * (height - 1)


def decode_cell_chunk(chunk: str, cell_id: int) -> DecodedCell:
    if len(chunk) != 10:
        raise ValueError(f"Cell {cell_id}: expected 10 chars, got {len(chunk)}")

    data = [get_int_by_hashed_value(ch) for ch in chunk]

    active = (data[0] & 0x20) >> 5
    line_of_sight = data[0] & 0x1
    movement = (data[2] & 0x38) >> 3
    ground_level = data[1] & 0xF
    ground_slope = (data[4] & 0x3C) >> 2
    ground_num = ((data[0] & 0x18) << 6) | ((data[2] & 0x7) << 6) | (data[3] & 0x3F)
    ground_flip = (data[4] & 0x2) >> 1
    ground_rot = (data[1] & 0x30) >> 4
    object1_num = ((data[0] & 0x4) << 11) | ((data[4] & 0x1) << 12) | ((data[5] & 0x3F) << 6) | (data[6] & 0x3F)
    object1_flip = (data[7] & 0x8) >> 3
    object1_rot = (data[7] & 0x30) >> 4
    object2_num = ((data[0] & 0x2) << 12) | ((data[7] & 0x1) << 12) | ((data[8] & 0x3F) << 6) | (data[9] & 0x3F)
    object2_flip = (data[7] & 0x4) >> 2
    object2_interactive = (data[7] & 0x2) >> 1

    return DecodedCell(
        cell_id=cell_id,
        raw_chunk=chunk,
        active=active,
        line_of_sight=line_of_sight,
        movement=movement,
        ground_level=ground_level,
        ground_slope=ground_slope,
        ground_num=ground_num,
        ground_flip=ground_flip,
        ground_rot=ground_rot,
        object1_num=object1_num,
        object1_flip=object1_flip,
        object1_rot=object1_rot,
        object2_num=object2_num,
        object2_flip=object2_flip,
        object2_interactive=object2_interactive,
    )


def encode_cell_fields(
    *,
    active: int,
    line_of_sight: int,
    movement: int,
    ground_level: int,
    ground_slope: int,
    ground_num: int,
    ground_flip: int,
    ground_rot: int,
    object1_num: int,
    object1_flip: int,
    object1_rot: int,
    object2_num: int,
    object2_flip: int,
    object2_interactive: int,
) -> str:
    for name, value, max_value in [
        ("active", active, 1),
        ("line_of_sight", line_of_sight, 1),
        ("movement", movement, 7),
        ("ground_level", ground_level, 15),
        ("ground_slope", ground_slope, 15),
        ("ground_num", ground_num, 1023),
        ("ground_flip", ground_flip, 1),
        ("ground_rot", ground_rot, 3),
        ("object1_num", object1_num, 8191),
        ("object1_flip", object1_flip, 1),
        ("object1_rot", object1_rot, 3),
        ("object2_num", object2_num, 8191),
        ("object2_flip", object2_flip, 1),
        ("object2_interactive", object2_interactive, 1),
    ]:
        if not 0 <= value <= max_value:
            raise ValueError(f"{name} must be between 0 and {max_value}, got {value}")

    data = [0] * 10

    data[0] |= (active & 0x1) << 5
    data[0] |= (line_of_sight & 0x1)
    data[0] |= ((ground_num >> 9) & 0x3) << 3
    data[0] |= ((object1_num >> 13) & 0x1) << 2
    data[0] |= ((object2_num >> 13) & 0x1) << 1

    data[1] |= ground_level & 0xF
    data[1] |= (ground_rot & 0x3) << 4

    data[2] |= (movement & 0x7) << 3
    data[2] |= (ground_num >> 6) & 0x7

    data[3] |= ground_num & 0x3F

    data[4] |= (ground_slope & 0xF) << 2
    data[4] |= (ground_flip & 0x1) << 1
    data[4] |= (object1_num >> 12) & 0x1

    data[5] |= (object1_num >> 6) & 0x3F
    data[6] |= object1_num & 0x3F

    data[7] |= (object1_rot & 0x3) << 4
    data[7] |= (object1_flip & 0x1) << 3
    data[7] |= (object2_flip & 0x1) << 2
    data[7] |= (object2_interactive & 0x1) << 1
    data[7] |= (object2_num >> 12) & 0x1

    data[8] |= (object2_num >> 6) & 0x3F
    data[9] |= object2_num & 0x3F

    return "".join(get_hashed_value_by_int(v) for v in data)


def decode_mapdata(map_data: str, width: int, height: int, key: Optional[str] = None) -> tuple[str, List[DecodedCell]]:
    source = map_data.strip()

    if is_map_ciphered(source):
        if not key:
            raise ValueError("mapData looks encrypted, but no --key was provided.")
        source = decrypt_map_data(source, key)

    if len(source) % 10 != 0:
        raise ValueError(
            f"Decoded mapData length must be a multiple of 10. Got {len(source)} characters."
        )

    expected = expected_cell_count(width, height)
    actual = len(source) // 10
    if actual != expected:
        raise ValueError(
            f"Cell count mismatch: got {actual} cells from mapData, expected {expected} "
            f"for width={width}, height={height}."
        )

    cells = [decode_cell_chunk(source[i:i + 10], i // 10) for i in range(0, len(source), 10)]
    return source, cells


def cells_to_rows(cells: Iterable[DecodedCell]) -> List[dict]:
    rows = []
    for cell in cells:
        row = asdict(cell)
        row["likely_walkable"] = cell.likely_walkable
        row["has_visible_content"] = cell.has_visible_content
        rows.append(row)
    return rows


def print_table(rows: List[dict], only_non_empty: bool = False, limit: Optional[int] = None) -> None:
    if only_non_empty:
        rows = [r for r in rows if r["has_visible_content"] or r["object2_interactive"] == 1]

    if limit is not None:
        rows = rows[:limit]

    cols = [
        "cell_id",
        "active",
        "line_of_sight",
        "movement",
        "ground_level",
        "ground_slope",
        "ground_num",
        "object1_num",
        "object2_num",
        "object2_interactive",
        "raw_chunk",
    ]

    widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(row[c])))

    def fmt(row: dict) -> str:
        return " | ".join(str(row[c]).ljust(widths[c]) for c in cols)

    print(fmt({c: c for c in cols}))
    print("-+-".join("-" * widths[c] for c in cols))
    for row in rows:
        print(fmt(row))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def update_cell_from_args(base_cell: DecodedCell, args: argparse.Namespace) -> DecodedCell:
    if args.raw_chunk:
        return decode_cell_chunk(args.raw_chunk, base_cell.cell_id)

    fields = asdict(base_cell)
    fields.pop("cell_id", None)
    fields.pop("raw_chunk", None)

    arg_to_field = {
        "active": "active",
        "line_of_sight": "line_of_sight",
        "movement": "movement",
        "ground_level": "ground_level",
        "ground_slope": "ground_slope",
        "ground_num": "ground_num",
        "ground_flip": "ground_flip",
        "ground_rot": "ground_rot",
        "object1_num": "object1_num",
        "object1_flip": "object1_flip",
        "object1_rot": "object1_rot",
        "object2_num": "object2_num",
        "object2_flip": "object2_flip",
        "object2_interactive": "object2_interactive",
    }

    touched = False
    for arg_name, field_name in arg_to_field.items():
        value = getattr(args, arg_name)
        if value is not None:
            fields[field_name] = value
            touched = True

    if not touched:
        raise ValueError("No patch requested. Provide --raw-chunk or at least one field override.")

    new_chunk = encode_cell_fields(**fields)
    return decode_cell_chunk(new_chunk, base_cell.cell_id)


def patch_mapdata(
    map_data: str,
    width: int,
    height: int,
    cell_id: int,
    key: Optional[str],
    patch_args: argparse.Namespace,
) -> tuple[str, DecodedCell, DecodedCell]:
    decoded_mapdata, cells = decode_mapdata(map_data, width, height, key)

    if not 0 <= cell_id < len(cells):
        raise ValueError(f"cell_id {cell_id} out of range, expected 0..{len(cells)-1}")

    before = cells[cell_id]
    after = update_cell_from_args(before, patch_args)

    chunks = [c.raw_chunk for c in cells]
    chunks[cell_id] = after.raw_chunk
    updated_mapdata = "".join(chunks)
    return updated_mapdata, before, after


def add_source_arguments(parser: argparse.ArgumentParser) -> None:
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--mapdata", help="mapData content")
    src.add_argument("--mapdata-file", type=Path, help="file containing only mapData")
    parser.add_argument("--width", type=int, required=True, help="maps.width")
    parser.add_argument("--height", type=int, required=True, help="maps.heigth")
    parser.add_argument("--key", help="maps.key, required only for encrypted mapData")


def read_mapdata_from_args(args: argparse.Namespace) -> str:
    return args.mapdata if args.mapdata is not None else load_text(args.mapdata_file)


def cmd_decode(args: argparse.Namespace) -> int:
    map_data = read_mapdata_from_args(args)
    _, cells = decode_mapdata(map_data, args.width, args.height, args.key)
    rows = cells_to_rows(cells)

    print_table(rows, only_non_empty=args.only_non_empty, limit=args.limit)

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


def cmd_patch(args: argparse.Namespace) -> int:
    map_data = read_mapdata_from_args(args)
    updated_mapdata, before, after = patch_mapdata(
        map_data=map_data,
        width=args.width,
        height=args.height,
        cell_id=args.cell_id,
        key=args.key,
        patch_args=args,
    )

    print(updated_mapdata)

    if args.output_mapdata:
        args.output_mapdata.parent.mkdir(parents=True, exist_ok=True)
        args.output_mapdata.write_text(updated_mapdata, encoding="utf-8")

    if args.show_diff:
        sys.stderr.write(
            f"Cell {before.cell_id} before: {before.raw_chunk} -> object2_num={before.object2_num}, "
            f"object2_interactive={before.object2_interactive}\n"
        )
        sys.stderr.write(
            f"Cell {after.cell_id} after : {after.raw_chunk} -> object2_num={after.object2_num}, "
            f"object2_interactive={after.object2_interactive}\n"
        )

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Decode and patch StarLoco/Dofus mapData")
    sub = parser.add_subparsers(dest="command", required=True)

    decode_parser = sub.add_parser("decode", help="decode mapData into cells")
    add_source_arguments(decode_parser)
    decode_parser.add_argument("--csv", type=Path, help="export CSV")
    decode_parser.add_argument("--json", type=Path, help="export JSON")
    decode_parser.add_argument("--only-non-empty", action="store_true", help="show only cells that appear to contain objects")
    decode_parser.add_argument("--limit", type=int, help="limit printed rows")
    decode_parser.set_defaults(func=cmd_decode)

    patch_parser = sub.add_parser("patch", help="patch one cell and print updated mapData to stdout")
    add_source_arguments(patch_parser)
    patch_parser.add_argument("--cell-id", type=int, required=True, help="target cell id to patch")
    patch_parser.add_argument("--raw-chunk", help="replace the whole 10-char chunk directly")
    patch_parser.add_argument("--active", type=int)
    patch_parser.add_argument("--line-of-sight", dest="line_of_sight", type=int)
    patch_parser.add_argument("--movement", type=int)
    patch_parser.add_argument("--ground-level", dest="ground_level", type=int)
    patch_parser.add_argument("--ground-slope", dest="ground_slope", type=int)
    patch_parser.add_argument("--ground-num", dest="ground_num", type=int)
    patch_parser.add_argument("--ground-flip", dest="ground_flip", type=int)
    patch_parser.add_argument("--ground-rot", dest="ground_rot", type=int)
    patch_parser.add_argument("--object1-num", dest="object1_num", type=int)
    patch_parser.add_argument("--object1-flip", dest="object1_flip", type=int)
    patch_parser.add_argument("--object1-rot", dest="object1_rot", type=int)
    patch_parser.add_argument("--object2-num", dest="object2_num", type=int)
    patch_parser.add_argument("--object2-flip", dest="object2_flip", type=int)
    patch_parser.add_argument("--object2-interactive", dest="object2_interactive", type=int)
    patch_parser.add_argument("--output-mapdata", type=Path, help="also write updated mapData to a file")
    patch_parser.add_argument("--show-diff", action="store_true", help="print before/after summary to stderr")
    patch_parser.set_defaults(func=cmd_patch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
