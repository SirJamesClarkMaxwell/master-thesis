from __future__ import annotations

import json
import math
from pathlib import Path

from manim import *


LEVELS_JSON = Path('C:\\Users\\fzabi\\Desktop\\tmp\\master-theisis\\00_Project\\hBN\\electron_structure\\figs\\_work\\dimer\\levels.json')
CFG_JSON = Path('C:\\Users\\fzabi\\Desktop\\tmp\\master-theisis\\00_Project\\hBN\\electron_structure\\figs\\_work\\dimer\\render_config.json')

# Canvas/aspect-ratio bootstrap.
# Must be applied before the Scene object is rendered.
_BOOT_CFG = json.loads(CFG_JSON.read_text(encoding="utf-8"))
_CANVAS_CFG = _BOOT_CFG.get("canvas", {}) if isinstance(_BOOT_CFG, dict) else {}

config.pixel_width = int(_CANVAS_CFG.get("pixel_width", 1130))
config.pixel_height = int(_CANVAS_CFG.get("pixel_height", 1906))
config.frame_width = float(_CANVAS_CFG.get("frame_width", 7.0))
config.frame_height = float(_CANVAS_CFG.get("frame_height", 11.81))


def deep_get(d, keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def as_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


class KSLevelsScene(Scene):
    def construct(self):
        data = json.loads(LEVELS_JSON.read_text(encoding="utf-8"))
        cfg = json.loads(CFG_JSON.read_text(encoding="utf-8"))

        meta = data["meta"]
        levels = data["levels"]

        plot_cfg = deep_get(cfg, ["plot"], {})
        axis_cfg = deep_get(cfg, ["axis"], {})
        label_cfg = deep_get(cfg, ["labels"], {})
        occ_cfg = deep_get(cfg, ["occupancy"], {})

        layout = plot_cfg.get("layout", "paired_orbital")
        title = plot_cfg.get("title", "")
        title_mode = plot_cfg.get("title_mode", "text")
        show_title = as_bool(plot_cfg.get("show_title", True), True)

        cbm = float(meta["cbm_relative_eV"])
        energies = [float(lv["energy_relative_eV"]) for lv in levels if lv.get("energy_relative_eV") is not None]

        major_tick = float(axis_cfg.get("major_tick_eV", 0.5))
        minor_tick = float(axis_cfg.get("minor_tick_eV", 0.25))
        axis_padding = float(axis_cfg.get("auto_padding_eV", 0.25))
        expand_to_fit = as_bool(axis_cfg.get("expand_to_fit_levels", True), True)

        requested_y_min = axis_cfg.get("y_min_eV", None)
        requested_y_max = axis_cfg.get("y_max_eV", None)

        # Include a small margin for electron arrows and labels when auto-extending the axis.
        data_min = min([0.0, cbm] + energies) if energies else 0.0
        data_max = max([0.0, cbm] + energies) if energies else cbm
        arrow_energy_margin = float(axis_cfg.get("arrow_energy_margin_eV", 0.12))
        data_min -= arrow_energy_margin
        data_max += arrow_energy_margin

        if requested_y_min is None:
            y_min = math.floor((data_min - axis_padding) / minor_tick) * minor_tick
        else:
            y_min = float(requested_y_min)

        if requested_y_max is None:
            y_max = math.ceil((data_max + axis_padding) / minor_tick) * minor_tick
        else:
            y_max = float(requested_y_max)

        if expand_to_fit:
            y_min = min(y_min, math.floor((data_min - axis_padding) / minor_tick) * minor_tick)
            y_max = max(y_max, math.ceil((data_max + axis_padding) / minor_tick) * minor_tick)

        if y_max <= y_min:
            raise ValueError("Invalid y-axis limits.")

        show_grid = as_bool(axis_cfg.get("show_grid", True), True)

        energy_decimals = int(label_cfg.get("energy_decimals", 2))
        occ_decimals = int(label_cfg.get("occupation_decimals", 2))
        show_energy_labels = as_bool(label_cfg.get("show_energy_labels", True), True)
        show_band_index = as_bool(label_cfg.get("show_band_index", False), False)
        energy_label_font_size = int(label_cfg.get("energy_label_font_size", 15))
        occ_label_font_size = int(label_cfg.get("occupation_label_font_size", 14))
        label_min_sep = float(label_cfg.get("label_min_separation", 0.20))
        label_connector = as_bool(label_cfg.get("draw_label_connectors", True), True)

        show_occ_text_if_not_full = as_bool(occ_cfg.get("show_occ_text_if_not_full", True), True)
        show_empty_occ_text = as_bool(occ_cfg.get("show_empty_occ_text", False), False)
        show_fractional_occ_text_only = as_bool(occ_cfg.get("show_fractional_occ_text_only", True), True)
        full_tol = float(occ_cfg.get("full_occupation_tolerance", 0.05))
        empty_tol = float(occ_cfg.get("empty_occupation_tolerance", 0.05))
        fractional_arrow_opacity = float(occ_cfg.get("fractional_arrow_opacity", 0.45))

        pair_tol = float(plot_cfg.get("pairing_energy_tolerance_eV", 0.05))
        level_stroke_width = float(plot_cfg.get("level_stroke_width", 3.0))
        show_electron_arrows = as_bool(plot_cfg.get("show_electron_arrows", True), True)
        electron_arrow_length = float(plot_cfg.get("electron_arrow_length", 0.44))
        electron_arrow_stroke_width = float(plot_cfg.get("electron_arrow_stroke_width", 2.6))
        electron_arrow_dx = float(plot_cfg.get("electron_arrow_dx", 0.16))

        self.camera.background_color = WHITE

        plot_width = float(plot_cfg.get("plot_width", 5.15))
        plot_height = float(plot_cfg.get("plot_height", 8.25))
        x_left = -plot_width / 2
        x_right = plot_width / 2
        y_bottom = -plot_height / 2
        y_top = y_bottom + plot_height

        def y_of(e):
            return y_bottom + (float(e) - y_min) / (y_max - y_min) * plot_height

        vb_top = max(y_bottom, min(y_top, y_of(0.0)))
        cb_bottom = max(y_bottom, min(y_top, y_of(cbm)))

        vb_rect = Rectangle(width=plot_width, height=max(0.001, vb_top - y_bottom), stroke_width=0, fill_color=BLUE, fill_opacity=0.11)
        vb_rect.move_to([0, (y_bottom + vb_top) / 2, 0])
        cb_rect = Rectangle(width=plot_width, height=max(0.001, y_top - cb_bottom), stroke_width=0, fill_color=RED, fill_opacity=0.10)
        cb_rect.move_to([0, (cb_bottom + y_top) / 2, 0])
        self.add(vb_rect, cb_rect)

        frame = Rectangle(width=plot_width, height=plot_height, stroke_color=BLACK, stroke_width=1.2)
        frame.move_to([0, (y_bottom + y_top) / 2, 0])
        self.add(frame)

        if show_grid:
            e = math.ceil(y_min / minor_tick) * minor_tick
            while e <= y_max + 1e-9:
                yy = y_of(e)
                is_major = abs((e / major_tick) - round(e / major_tick)) < 1e-8
                line = Line([x_left, yy, 0], [x_right, yy, 0])
                line.set_stroke(color=GREY_B if is_major else GREY_C, width=0.70 if is_major else 0.32, opacity=0.65 if is_major else 0.40)
                self.add(line)
                e += minor_tick

        if layout == "split_spin_channels":
            divider = DashedLine([0, y_bottom, 0], [0, y_top, 0], dash_length=0.12)
            divider.set_stroke(color=GREY_B, width=1.0, opacity=0.8)
            self.add(divider)

        e = math.ceil(y_min / major_tick) * major_tick
        while e <= y_max + 1e-9:
            yy = y_of(e)
            tick = Line([x_left - 0.07, yy, 0], [x_left, yy, 0], color=BLACK, stroke_width=1)
            lab = Text(f"{e:.1f}", font_size=17, color=BLACK)
            lab.next_to(tick, LEFT, buff=0.07)
            self.add(tick, lab)
            e += major_tick

        y_axis_label = Text("E [eV]", font_size=20, color=BLACK)
        y_axis_label.rotate(PI / 2)
        y_axis_label.next_to(frame, LEFT, buff=0.55)
        self.add(y_axis_label)

        if as_bool(plot_cfg.get("show_vbm_cbm_labels", True), True):
            vb_label = Text("VB", font_size=31, color=BLACK)
            vb_label.next_to([x_right, y_of(0.0), 0], RIGHT, buff=0.20)
            cb_label = Text("CB", font_size=31, color=BLACK)
            cb_label.next_to([x_right, y_of(cbm), 0], RIGHT, buff=0.20)
            self.add(vb_label, cb_label)

        if show_title and title:
            if title_mode in {"tex", "latex", "mathtex"}:
                title_obj = Tex(title, color=BLACK, font_size=27)
            else:
                title_obj = Text(title, color=BLACK, font_size=26)
            title_obj.next_to(frame, UP, buff=0.14)
            self.add(title_obj)

        def occ_class(occ):
            occ = float(occ)
            if occ >= 1.0 - full_tol:
                return "full"
            if occ <= empty_tol:
                return "empty"
            return "fractional"

        def should_show_occ_label(occ):
            cls = occ_class(occ)
            if not show_occ_text_if_not_full:
                return False
            if show_fractional_occ_text_only:
                return cls == "fractional"
            if cls == "full":
                return False
            if cls == "empty" and not show_empty_occ_text:
                return False
            return True

        def energy_text(e, band_index=None):
            txt = f"{e:.{energy_decimals}f} eV"
            if show_band_index and band_index is not None:
                txt = f"b{band_index}: " + txt
            return txt

        def add_arrow(x, y, spin, occ, scale=1.0):
            if not show_electron_arrows:
                return
            cls = occ_class(occ)
            if cls == "empty":
                return
            length = electron_arrow_length * scale
            if spin == "down":
                start = [x, y + length / 2, 0]
                end = [x, y - length / 2, 0]
            else:
                start = [x, y - length / 2, 0]
                end = [x, y + length / 2, 0]
            arr = Arrow(start=start, end=end, buff=0, stroke_width=electron_arrow_stroke_width, max_tip_length_to_length_ratio=0.32, color=BLACK)
            if cls == "fractional":
                arr.set_opacity(fractional_arrow_opacity)
            self.add(arr)

        def add_level_line(x0, x1, y, color=BLACK, stroke_width=None):
            line = Line([x0, y, 0], [x1, y, 0], color=color)
            line.set_stroke(width=stroke_width or level_stroke_width)
            self.add(line)
            return line

        def pack_label_positions(label_reqs):
            if not label_reqs:
                return {}
            min_y = y_bottom + 0.08
            max_y = y_top - 0.08
            sorted_reqs = sorted(label_reqs, key=lambda r: r["desired_y"])
            packed = []
            last = min_y - label_min_sep
            for req in sorted_reqs:
                yy = max(req["desired_y"], last + label_min_sep)
                packed.append([req, yy])
                last = yy
            overflow = packed[-1][1] - max_y
            if overflow > 0:
                for item in packed:
                    item[1] -= overflow
                last = min_y - label_min_sep
                for item in packed:
                    item[1] = max(item[1], last + label_min_sep)
                    last = item[1]
            return {id(req): yy for req, yy in packed}

        energy_label_reqs = []
        occ_label_reqs = []

        def request_energy_label(text, desired_y, side, anchor_x, anchor_y):
            if show_energy_labels:
                energy_label_reqs.append({"text": text, "desired_y": desired_y, "side": side, "anchor_x": anchor_x, "anchor_y": anchor_y})

        def request_occ_label(text, desired_y, side, anchor_x, anchor_y):
            occ_label_reqs.append({"text": text, "desired_y": desired_y, "side": side, "anchor_x": anchor_x, "anchor_y": anchor_y})

        if layout == "split_spin_channels":
            up_center = -plot_width * 0.25
            dn_center = plot_width * 0.25
            line_w = float(plot_cfg.get("split_level_width", 1.45))
            for lv in levels:
                spin = lv["spin"]
                if spin not in {"up", "down"}:
                    center = 0.0; color = BLACK
                elif spin == "up":
                    center = up_center; color = RED
                else:
                    center = dn_center; color = BLUE
                e_rel = float(lv["energy_relative_eV"])
                yy = y_of(e_rel)
                x0, x1 = center - line_w / 2, center + line_w / 2
                add_level_line(x0, x1, yy, color=color)
                request_energy_label(energy_text(e_rel, lv["band_index"]), yy, "left", x0, yy)
                occ = float(lv["occupation"])
                if should_show_occ_label(occ):
                    request_occ_label(f"occ = {occ:.{occ_decimals}f}", yy, "right", x1, yy)
                add_arrow(center, yy, "up" if spin == "up" else "down", occ)

        elif layout == "paired_orbital":
            # Important: in spin-polarized VASP calculations the same band index in
            # spin-up and spin-down is not guaranteed to represent the same spatial
            # orbital. Pair by energy only when the two levels are nearly degenerate.
            line_w = float(plot_cfg.get("paired_level_width", 2.35))
            split_line_w = float(plot_cfg.get("paired_split_level_width", 0.90))
            split_offset = float(plot_cfg.get("paired_split_offset", 0.55))

            up_levels = [lv for lv in levels if lv.get("spin") == "up"]
            dn_levels = [lv for lv in levels if lv.get("spin") == "down"]
            none_levels = [lv for lv in levels if lv.get("spin") not in {"up", "down"}]
            up_levels.sort(key=lambda lv: float(lv["energy_relative_eV"]))
            dn_levels.sort(key=lambda lv: float(lv["energy_relative_eV"]))

            used_down = set()
            pairs = []
            unpaired = []

            for up in up_levels:
                e_up = float(up["energy_relative_eV"])
                best_i = None
                best_de = None
                for i, dn in enumerate(dn_levels):
                    if i in used_down:
                        continue
                    de = abs(e_up - float(dn["energy_relative_eV"]))
                    if de <= pair_tol and (best_de is None or de < best_de):
                        best_i = i
                        best_de = de
                if best_i is None:
                    unpaired.append(up)
                else:
                    used_down.add(best_i)
                    pairs.append((up, dn_levels[best_i]))

            for i, dn in enumerate(dn_levels):
                if i not in used_down:
                    unpaired.append(dn)

            # Draw unpaired spin-resolved lines.
            for lv in unpaired:
                e_rel = float(lv["energy_relative_eV"])
                occ = float(lv["occupation"])
                yy = y_of(e_rel)
                spin = lv["spin"]
                if spin == "up":
                    center = -split_offset; color = RED
                elif spin == "down":
                    center = split_offset; color = BLUE
                else:
                    center = 0.0; color = BLACK
                x0, x1 = center - split_line_w / 2, center + split_line_w / 2
                add_level_line(x0, x1, yy, color=color)
                add_arrow(center, yy, "up" if spin != "down" else "down", occ)
                request_energy_label(energy_text(e_rel, lv["band_index"]), yy, "left", -line_w / 2, yy)
                if should_show_occ_label(occ):
                    request_occ_label(f"occ = {occ:.{occ_decimals}f}", yy, "right", x1, yy)

            # Draw paired nearly-degenerate spin-up/spin-down levels as one orbital.
            for up, dn in pairs:
                e_up = float(up["energy_relative_eV"])
                e_dn = float(dn["energy_relative_eV"])
                occ_up = float(up["occupation"])
                occ_dn = float(dn["occupation"])
                e_avg = 0.5 * (e_up + e_dn)
                yy = y_of(e_avg)
                x0, x1 = -line_w / 2, line_w / 2
                add_level_line(x0, x1, yy, color=BLACK)
                add_arrow(-electron_arrow_dx, yy, "up", occ_up)
                add_arrow(electron_arrow_dx, yy, "down", occ_dn)
                request_energy_label(energy_text(e_avg, up["band_index"]), yy, "left", x0, yy)
                occ_texts = []
                if should_show_occ_label(occ_up):
                    occ_texts.append(f"up: {occ_up:.{occ_decimals}f}")
                if should_show_occ_label(occ_dn):
                    occ_texts.append(f"down: {occ_dn:.{occ_decimals}f}")
                if occ_texts:
                    request_occ_label("occ = " + ", ".join(occ_texts), yy, "right", x1, yy)

            for lv in none_levels:
                e_rel = float(lv["energy_relative_eV"])
                occ = float(lv["occupation"])
                yy = y_of(e_rel)
                x0, x1 = -line_w / 2, line_w / 2
                add_level_line(x0, x1, yy, color=BLACK)
                if occ >= 2.0 - full_tol:
                    add_arrow(-electron_arrow_dx, yy, "up", 1.0)
                    add_arrow(electron_arrow_dx, yy, "down", 1.0)
                elif occ >= 1.0 - full_tol:
                    add_arrow(0.0, yy, "up", 1.0)
                elif occ > empty_tol:
                    add_arrow(0.0, yy, "up", min(occ, 1.0))
                request_energy_label(energy_text(e_rel, lv["band_index"]), yy, "left", x0, yy)
                if should_show_occ_label(occ):
                    request_occ_label(f"occ = {occ:.{occ_decimals}f}", yy, "right", x1, yy)

        else:
            raise ValueError(f"Unknown layout: {layout}")

        def draw_label_requests(reqs, is_occ=False):
            left_reqs = [r for r in reqs if r["side"] == "left"]
            right_reqs = [r for r in reqs if r["side"] == "right"]
            packed = {}
            packed.update(pack_label_positions(left_reqs))
            packed.update(pack_label_positions(right_reqs))
            for req in reqs:
                yy = packed.get(id(req), req["desired_y"])
                font_size = occ_label_font_size if is_occ else energy_label_font_size
                label = Text(req["text"], font_size=font_size, color=BLACK)
                if req["side"] == "left":
                    label.next_to([req["anchor_x"], yy, 0], LEFT, buff=0.08)
                    conn_start = [req["anchor_x"] - 0.03, yy, 0]
                else:
                    label.next_to([req["anchor_x"], yy, 0], RIGHT, buff=0.08)
                    conn_start = [req["anchor_x"] + 0.03, yy, 0]
                self.add(label)
                if label_connector and abs(yy - req["anchor_y"]) > 0.04:
                    conn = Line(conn_start, [req["anchor_x"], req["anchor_y"], 0], color=GREY_B)
                    conn.set_stroke(width=0.45, opacity=0.55)
                    self.add(conn)

        draw_label_requests(energy_label_reqs, is_occ=False)
        draw_label_requests(occ_label_reqs, is_occ=True)
