from src.unpack import read_file
from src.pc_parser import PCParser
from src.crd_parser import parse_crd_file
from src.pc_svg_renderer import render_pc_html
from src.dip_library import parse_dip_library
import os

os.chdir('/Users/dmoisa/Documents/sun/smi/suds-tools')

octal = '/Users/dmoisa/Documents/sun/smi/smi/octal'
crd = parse_crd_file(f'{octal}/multi0.crd.O')
dip_lib = parse_dip_library(f'{octal}/dips.dip.O')

# g_board
pc_g = PCParser(read_file(f'{octal}/g.pc.O'), source_path='g.pc.O').parse()
render_pc_html(pc_g, '/tmp/g_board.html', crd=crd, dip_lib=dip_lib)

# qx_board  
pc_qx = PCParser(read_file(f'{octal}/qx.pc.O'), source_path='qx.pc.O').parse()
render_pc_html(pc_qx, '/tmp/qx_board.html', crd=crd, dip_lib=dip_lib)

# d_board with silk
pc_d = PCParser(read_file(f'{octal}/d.pc.O'), source_path='d.pc.O').parse()
silk = PCParser(read_file(f'{octal}/mupac.pc.O'), source_path='mupac.pc.O').parse()
render_pc_html(pc_d, '/tmp/d_board_silk.html', crd=crd, silk_pc=silk, dip_lib=dip_lib)

# ti_board
pc_ti = PCParser(read_file(f'{octal}/ti.pc.O'), source_path='ti.pc.O').parse()
render_pc_html(pc_ti, '/tmp/ti_board.html', crd=crd, dip_lib=dip_lib)
