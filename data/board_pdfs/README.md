# SUDS Schematic Board PDFs

Best-version PDF renderings of Sun Microsystems schematic drawings,
recovered from the SAILDART `[*,SMI]` archive (1978–1986).

> **Interactive index with per-page provenance:** [index.html](index.html) *(open locally)*

## Summary

| Metric | Count |
|--------|-------|
| Source DRW files indexed | 2,215 |
| Unique schematic page names | 685 |
| Canonical board sets identified | 352 |
| Board sets using version history | 146 |
| Best-version PDFs in this directory | 91 |

## How These Were Made

1. **Indexed** all 2,215 DRW files across `smi/octal/` (685 latest) and `smi/prev/` (1,530 version history)
2. **Extracted** metadata: board designator, page number, "of" total, date, body count
3. **Grouped** into 352 canonical board sets using designator-first coherence scoring
4. **Selected** best version per page — may use an older version from `prev/` if it produces a more complete set
5. **Rendered** DRW → SVG → PDF with component designators overlaid from wirelist data

**Scoring formula:** `0.35 × designator_match + 0.20 × of_total_match + 0.20 × coverage + 0.15 × wirelist_match + 0.10 × size`

**PDF filename format:** `{prefix}_v{N}_{designator}_of{total}_s{score%}_BEST.pdf`

## Sun-3 Family

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `x` | SUN 3 F | 15/15 | 96% | [📄 PDF](x/x_v1_sun_3_f_of15_s96%_BEST.pdf) |
| `em` | SUN 3 E | 4/4 | 93% | [📄 PDF](em/em_v1_sun_3_e_of4_s93%_BEST.pdf) |
| `ep` | SUN 3 E | 10/10 | 86% | [📄 PDF](ep/ep_v1_sun_3_e_of10_s86%_BEST.pdf) 🕰️ |
| `x_2` | SUN 3 F | 15/15 | 81% | [📄 PDF](x_2/x_2_v1_sun_3_f_of15_s81%_BEST.pdf) |
| `em_2` | SUN 3 E | 4/4 | 78% | [📄 PDF](em_2/em_2_v1_sun_3_e_of4_s78%_BEST.pdf) |
| `xc` | SUN 3 | 3/15 | 69% | [📄 PDF](xc/xc_v1_sun_3_of15_s69%_BEST.pdf) |

## Sun-3/60 (Ferrari)

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `f` | FERRARI | 20/20 | 100% | [📄 PDF](f/f_v1_ferrari_of20_s100%_BEST.pdf) |
| `fm` | FERRARI | 11/11 | 100% | [📄 PDF](fm/fm_v1_ferrari_of11_s100%_BEST.pdf) |
| `60` | FERRARI | 20/20 | 88% | [📄 PDF](60/60_v1_ferrari_of20_s88%_BEST.pdf) |
| `f_2` | FERRARI | 20/20 | 85% | [📄 PDF](f_2/f_2_v1_ferrari_of20_s85%_BEST.pdf) |
| `ev` | FERRARI | 3/4 | 73% | [📄 PDF](ev/ev_v1_ferrari_of4_s73%_BEST.pdf) |
| `foo` | FERRARI | 1/20 | 66% | [📄 PDF](foo/foo_v1_ferrari_of20_s66%_BEST.pdf) 🕰️ |
| `foo_2` | FERRARI | 1/20 | 66% | [📄 PDF](foo_2/foo_2_v1_ferrari_of20_s66%_BEST.pdf) 🕰️ |
| `newf` | FERRARI | 1/20 | 66% | [📄 PDF](newf/newf_v1_ferrari_of20_s66%_BEST.pdf) |

## Sun-2 Family

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `sio` | SUN 2 | 5/5 | 100% | [📄 PDF](sio/sio_v1_sun_2_of5_s100%_BEST.pdf) |
| `a` | SUN 2 | 19/19 | 98% | [📄 PDF](a/a_v1_sun_2_of19_s98%_BEST.pdf) |
| `vmev` | SUN 2 | 3/4 | 95% | [📄 PDF](vmev/vmev_v1_sun_2_of4_s95%_BEST.pdf) |
| `vmem` | SUN 2251 MEMORY BOARD | 4/4 | 92% | [📄 PDF](vmem/vmem_v1_sun_2251_memory_board_of4_s92%_BEST.pdf) |
| `c` | SUN 2 LC | 5/7 | 87% | [📄 PDF](c/c_v1_sun_2_lc_of7_s87%_BEST.pdf) |
| `b` | SUN 2 | 19/19 | 85% | [📄 PDF](b/b_v1_sun_2_of19_s85%_BEST.pdf) 🕰️ |
| `b_2` | SUN 2 | 19/19 | 85% | [📄 PDF](b_2/b_2_v1_sun_2_of19_s85%_BEST.pdf) 🕰️ |
| `c_2` | SUN 2060 | 5/12 | 85% | [📄 PDF](c_2/c_2_v1_sun_2060_of12_s85%_BEST.pdf) |
| `sio_2` | SUN 2 | 5/5 | 85% | [📄 PDF](sio_2/sio_2_v1_sun_2_of5_s85%_BEST.pdf) |
| `qx` | SUN 2 | 8/8 | 84% | [📄 PDF](qx/qx_v1_sun_2_of8_s84%_BEST.pdf) |
| `a12` | SUN 2 | 19/19 | 83% | [📄 PDF](a12/a12_v1_sun_2_of19_s83%_BEST.pdf) |
| `a16` | SUN 2 | 19/19 | 83% | [📄 PDF](a16/a16_v1_sun_2_of19_s83%_BEST.pdf) |
| `a20` | SUN 2 | 19/19 | 83% | [📄 PDF](a20/a20_v1_sun_2_of19_s83%_BEST.pdf) |
| `a21` | SUN 2 | 19/19 | 83% | [📄 PDF](a21/a21_v1_sun_2_of19_s83%_BEST.pdf) |
| `a_2` | SUN 2 | 19/19 | 83% | [📄 PDF](a_2/a_2_v1_sun_2_of19_s83%_BEST.pdf) |
| `vmes` | SUN 2 | 1/2 | 81% | [📄 PDF](vmes/vmes_v1_sun_2_of2_s81%_BEST.pdf) |
| `h` | SUN 2 GRAPHICS | 4/5 | 78% | [📄 PDF](h/h_v1_sun_2_graphics_of5_s78%_BEST.pdf) |
| `j` | SUN 2 GRAPHICS | 4/5 | 78% | [📄 PDF](j/j_v1_sun_2_graphics_of5_s78%_BEST.pdf) |
| `s` | SUN 2 | 11/15 | 77% | [📄 PDF](s/s_v1_sun_2_of15_s77%_BEST.pdf) |
| `vmem_2` | SUN 2251 MEMORY BOARD | 4/4 | 77% | [📄 PDF](vmem_2/vmem_2_v1_sun_2251_memory_board_of4_s77%_BEST.pdf) |
| `vx` | SUN 2 GRAPHICS | 2/4 | 75% | [📄 PDF](vx/vx_v1_sun_2_graphics_of4_s75%_BEST.pdf) |
| `qq` | SUN 2 | 1/9 | 67% | [📄 PDF](qq/qq_v1_sun_2_of9_s67%_BEST.pdf) |
| `vmep` | SUN 2 | 1/12 | 67% | [📄 PDF](vmep/vmep_v1_sun_2_of12_s67%_BEST.pdf) |
| `vmep_2` | SUN 2 | 1/12 | 67% | [📄 PDF](vmep_2/vmep_2_v1_sun_2_of12_s67%_BEST.pdf) |
| `ap` | SUN 2 | 1/20 | 66% | [📄 PDF](ap/ap_v1_sun_2_of20_s66%_BEST.pdf) |
| `ax` | SUN 2 | 1/20 | 66% | [📄 PDF](ax/ax_v1_sun_2_of20_s66%_BEST.pdf) |
| `ax_2` | SUN 2 | 1/20 | 66% | [📄 PDF](ax_2/ax_2_v1_sun_2_of20_s66%_BEST.pdf) |
| `rj160` | SUN 2 | 19/19 | 66% | [📄 PDF](rj160/rj160_v1_sun_2_of19_s66%_BEST.pdf) |
| `vmes_2` | SUN 2 | 1/2 | 66% | [📄 PDF](vmes_2/vmes_2_v1_sun_2_of2_s66%_BEST.pdf) |

## Sun-1 Family

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `px` | SUN 68000 | 7/7 | 92% | [📄 PDF](px/px_v1_sun_68000_of7_s92%_BEST.pdf) |
| `p` | SUN 68000 10 | 4/5 | 77% | [📄 PDF](p/p_v1_sun_68000_10_of5_s77%_BEST.pdf) |

## Model 25 / Sun-2060

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `2` | MODEL 25 | 1/19 | 77% | [📄 PDF](2/2_v1_model_25_of19_s77%_BEST.pdf) |
| `25` | MODEL 25 | 19/19 | 77% | [📄 PDF](25/25_v1_model_25_of19_s77%_BEST.pdf) |
| `26` | MODEL 25 | 19/19 | 71% | [📄 PDF](26/26_v1_model_25_of19_s71%_BEST.pdf) |

## Graphics & Video

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `cg` | COLOR BOARD | 7/7 | 100% | [📄 PDF](cg/cg_v1_color_board_of7_s100%_BEST.pdf) |
| `cg_2` | COLOR BOARD | 7/7 | 85% | [📄 PDF](cg_2/cg_2_v1_color_board_of7_s85%_BEST.pdf) |
| `g` | SUN GRAPHICS | 7/7 | 85% | [📄 PDF](g/g_v1_sun_graphics_of7_s85%_BEST.pdf) 🕰️ |
| `ve1` | SN 2 VIDEO | 4/4 | 85% | [📄 PDF](ve1/ve1_v1_sn_2_video_of4_s85%_BEST.pdf) |
| `sy` | SUN2 COLOR BOARD | 3/14 | 84% | [📄 PDF](sy/sy_v1_sun2_color_board_of14_s84%_BEST.pdf) |
| `sy_2` | SUN2 COLOR BOARD | 3/14 | 69% | [📄 PDF](sy_2/sy_2_v1_sun2_color_board_of14_s69%_BEST.pdf) |
| `sx` | COLOR BOARD | 1/7 | 68% | [📄 PDF](sx/sx_v1_color_board_of7_s68%_BEST.pdf) |
| `sx_2` | COLOR BOARD | 1/7 | 68% | [📄 PDF](sx_2/sx_2_v1_color_board_of7_s68%_BEST.pdf) |

## I/O & Networking

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `ethp` | ETHERNET BOARD | 6/8 | 95% | [📄 PDF](ethp/ethp_v1_ethernet_board_of8_s95%_BEST.pdf) |
| `d` | IOBOARD | 4/4 | 92% | [📄 PDF](d/d_v1_ioboard_of4_s92%_BEST.pdf) |
| `dx` | IOBOARD | 4/4 | 85% | [📄 PDF](dx/dx_v1_ioboard_of4_s85%_BEST.pdf) |
| `dold` | IOBOARD | 3/4 | 80% | [📄 PDF](dold/dold_v1_ioboard_of4_s80%_BEST.pdf) |
| `eth` | ETHERNET BOARD | 6/7 | 78% | [📄 PDF](eth/eth_v1_ethernet_board_of7_s78%_BEST.pdf) 🕰️ |
| `d_2` | IOBOARD | 4/4 | 77% | [📄 PDF](d_2/d_2_v1_ioboard_of4_s77%_BEST.pdf) |
| `es` | ETHERNET SERVER | 1/5 | 77% | [📄 PDF](es/es_v1_ethernet_server_of5_s77%_BEST.pdf) |
| `ethx` | ETHER | 2/3 | 73% | [📄 PDF](ethx/ethx_v1_ether_of3_s73%_BEST.pdf) |

## Storage

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `fw` | WINCHESTER CONTROLLER | 2/3 | 93% | [📄 PDF](fw/fw_v1_winchester_controller_of3_s93%_BEST.pdf) |
| `ti` | SUN 1 4 TAPE | 4/4 | 85% | [📄 PDF](ti/ti_v1_sun_1_4_tape_of4_s85%_BEST.pdf) 🕰️ |
| `ti2` | SUN 1 4 TAPE | 4/4 | 85% | [📄 PDF](ti2/ti2_v1_sun_1_4_tape_of4_s85%_BEST.pdf) |
| `smd` | DISK | 6/7 | 82% | [📄 PDF](smd/smd_v1_disk_of7_s82%_BEST.pdf) |
| `fw_2` | WINCHESTER CONTROLLER | 2/3 | 78% | [📄 PDF](fw_2/fw_2_v1_winchester_controller_of3_s78%_BEST.pdf) |

## VME & Backplane

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `back` | M 160 BACKPLANE | 12/13 | 98% | [📄 PDF](back/back_v1_m_160_backplane_of13_s98%_BEST.pdf) 🕰️ |
| `vme3x2` | VME 3X TO 2X ADAPTER | 2/2 | 90% | [📄 PDF](vme3x2/vme3x2_v1_vme_3x_to_2x_adapter_of2_s90%_BEST.pdf) |

## Fileserver

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `20` | FILESERVER | 6/6 | 76% | [📄 PDF](20/20_v1_fileserver_of6_s76%_BEST.pdf) |

## Test & Debug

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `r` | ROPC | 2/3 | 93% | [📄 PDF](r/r_v1_ropc_of3_s93%_BEST.pdf) |
| `la` | LOGIC ANALYSER | 2/4 | 75% | [📄 PDF](la/la_v1_logic_analyser_of4_s75%_BEST.pdf) |

## Other

| Board | Designator | Pages | Score | PDF |
|-------|-----------|-------|-------|-----|
| `q` | 501 1007 08 | 9/9 | 100% | [📄 PDF](q/q_v1_501_1007_08_of9_s100%_BEST.pdf) |
| `v` | 501 1003 07 | 5/5 | 100% | [📄 PDF](v/v_v1_501_1003_07_of5_s100%_BEST.pdf) |
| `y` | 501 1013 02 | 4/4 | 100% | [📄 PDF](y/y_v1_501_1013_02_of4_s100%_BEST.pdf) |
| `m1` | 501 1007 08 | 9/9 | 90% | [📄 PDF](m1/m1_v1_501_1007_08_of9_s90%_BEST.pdf) |
| `xx` | SUN X | 8/10 | 89% | [📄 PDF](xx/xx_v1_sun_x_of10_s89%_BEST.pdf) |
| `v_2` | 501 1003 07 | 5/5 | 85% | [📄 PDF](v_2/v_2_v1_501_1003_07_of5_s85%_BEST.pdf) |
| `y_2` | 501 1013 02 | 4/4 | 85% | [📄 PDF](y_2/y_2_v1_501_1013_02_of4_s85%_BEST.pdf) |
| `sc` | CAPACITORS | 2/21 | 82% | [📄 PDF](sc/sc_v1_capacitors_of21_s82%_BEST.pdf) |
| `siod` | I O BOARD | 3/4 | 78% | [📄 PDF](siod/siod_v1_i_o_board_of4_s78%_BEST.pdf) |
| `siox` | I O BOARD | 3/4 | 78% | [📄 PDF](siox/siox_v1_i_o_board_of4_s78%_BEST.pdf) |
| `m` | 501 1007 08 | 7/9 | 75% | [📄 PDF](m/m_v1_501_1007_08_of9_s75%_BEST.pdf) |
| `m11` | 501 1007 08 | 9/9 | 75% | [📄 PDF](m11/m11_v1_501_1007_08_of9_s75%_BEST.pdf) |
| `m16` | 501 1007 08 | 9/9 | 75% | [📄 PDF](m16/m16_v1_501_1007_08_of9_s75%_BEST.pdf) |
| `m20` | 501 1007 08 | 9/9 | 75% | [📄 PDF](m20/m20_v1_501_1007_08_of9_s75%_BEST.pdf) |
| `xx_2` | SUN X | 8/10 | 74% | [📄 PDF](xx_2/xx_2_v1_sun_x_of10_s74%_BEST.pdf) |
| `1` | 501 1007 08 | 1/9 | 67% | [📄 PDF](1/1_v1_501_1007_08_of9_s67%_BEST.pdf) |
| `sc_2` | CAPACITORS | 2/21 | 67% | [📄 PDF](sc_2/sc_2_v1_capacitors_of21_s67%_BEST.pdf) |

---

🕰️ = includes pages recovered from SAILDART version history (`smi/prev/`)

See also:
- [Version selection algorithm](../../docs/version_selection.md)
- [Research journal](../../docs/journey.md)
- [SUDS format reference](../../docs/suds_format_reference.md)

*Generated 2026-08-06 20:35*
