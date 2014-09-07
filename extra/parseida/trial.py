#!/home/vagrant/idademo66/python

# copied python into ida demo folder
# also symlinked libida.so to /usr/lib/libida.so for early loads to work

import os
import struct
from ctypes import *
import time
IDAPATH = "/home/vagrant/idademo66/"
FILE = "/home/vagrant/qira/tests/idb/a.out"
BADADDR = 0xFFFFFFFF

string_buffers = [create_string_buffer(""), create_string_buffer(FILE)]
argv = (c_char_p*3)(*map(addressof, string_buffers)+[0])
idle_fxn = None

idp_notify = ['init', 'term', 'newprc', 'newasm', 'newfile', 'oldfile', 'newbinary', 'endbinary', 'newseg', 'assemble', 'obsolete_makemicro', 'outlabel', 'rename', 'may_show_sreg', 'closebase', 'load_idasgn', 'coagulate', 'auto_empty', 'auto_queue_empty', 'func_bounds', 'may_be_func', 'is_sane_insn', 'is_jump_func', 'gen_regvar_def', 'setsgr', 'set_compiler', 'is_basic_block_end', 'reglink', 'get_vxd_name', 'custom_ana', 'custom_out', 'custom_emu', 'custom_outop', 'custom_mnem', 'undefine', 'make_code', 'make_data', 'moving_segm', 'move_segm', 'is_call_insn', 'is_ret_insn', 'get_stkvar_scale_factor', 'create_flat_group', 'kernel_config_loaded', 'might_change_sp', 'is_alloca_probe', 'out_3byte', 'get_reg_name', 'savebase', 'gen_asm_or_lst', 'out_src_file_lnnum', 'get_autocmt', 'is_insn_table_jump', 'auto_empty_finally', 'loader_finished', 'loader_elf_machine', 'is_indirect_jump', 'verify_noreturn', 'verify_sp', 'renamed', 'add_func', 'del_func', 'set_func_start', 'set_func_end', 'treat_hindering_item', 'str2reg', 'create_switch_xrefs', 'calc_switch_cases', 'determined_main', 'preprocess_chart', 'get_bg_color', 'validate_flirt_func', 'get_operand_string', 'add_cref', 'add_dref', 'del_cref', 'del_dref', 'coagulate_dref', 'register_custom_fixup', 'custom_refinfo', 'set_proc_options', 'adjust_libfunc_ea', 'extlang_changed', 'last_cb_before_debugger']

ui_msgs = ['ui_null = 0', 'ui_range', 'ui_list', 'ui_idcstart', 'ui_idcstop', 'ui_suspend', 'ui_resume', 'ui_old_jumpto', 'ui_readsel', 'ui_unmarksel', 'ui_screenea', 'ui_saving', 'ui_saved', 'ui_refreshmarked', 'ui_refresh', 'ui_choose', 'ui_close_chooser', 'ui_banner', 'ui_setidle', 'ui_noabort', 'ui_term', 'ui_mbox', 'ui_beep', 'ui_msg', 'ui_askyn', 'ui_askfile', 'ui_form', 'ui_close_form', 'ui_clearbreak', 'ui_wasbreak', 'ui_asktext', 'ui_askstr', 'ui_askident', 'ui_askaddr', 'ui_askseg', 'ui_asklong', 'ui_showauto', 'ui_setstate', 'ui_add_idckey', 'ui_del_idckey', 'ui_old_get_marker', 'ui_analyzer_options', 'ui_is_msg_inited', 'ui_load_file', 'ui_run_dbg', 'ui_get_cursor', 'ui_get_curline', 'ui_get_hwnd', 'ui_copywarn', 'ui_getvcl', 'ui_idp_event', 'ui_lock_range_refresh', 'ui_unlock_range_refresh', 'ui_setbreak', 'ui_genfile_callback', 'ui_open_url', 'ui_hexdumpea', 'ui_set_xml', 'ui_get_xml', 'ui_del_xml', 'ui_push_xml', 'ui_pop_xml', 'ui_get_key_code', 'ui_setup_plugins_menu', 'ui_refresh_navband', 'ui_new_custom_viewer', 'ui_add_menu_item', 'ui_del_menu_item', 'ui_debugger_menu_change', 'ui_get_curplace', 'ui_create_tform', 'ui_open_tform', 'ui_close_tform', 'ui_switchto_tform', 'ui_find_tform', 'ui_get_current_tform', 'ui_get_tform_handle', 'ui_tform_visible', 'ui_tform_invisible', 'ui_get_ea_hint', 'ui_get_item_hint', 'ui_set_nav_colorizer', 'ui_refresh_custom_viewer', 'ui_destroy_custom_viewer', 'ui_jump_in_custom_viewer', 'ui_set_custom_viewer_popup', 'ui_add_custom_viewer_popup', 'ui_set_custom_viewer_handlers', 'ui_get_custom_viewer_curline', 'ui_get_current_viewer', 'ui_is_idaview', 'ui_get_custom_viewer_hint', 'ui_readsel2', 'ui_set_custom_viewer_range', 'ui_database_inited', 'ui_ready_to_run', 'ui_set_custom_viewer_handler', 'ui_refresh_chooser', 'ui_add_chooser_cmd', 'ui_open_builtin', 'ui_preprocess', 'ui_postprocess', 'ui_set_custom_viewer_mode', 'ui_gen_disasm_text', 'ui_gen_idanode_text', 'ui_install_cli', 'ui_execute_sync', 'ui_enable_input_hotkeys', 'ui_get_chooser_obj', 'ui_enable_chooser_item_attrs', 'ui_get_chooser_item_attrs', 'ui_set_dock_pos', 'ui_get_opnum', 'ui_install_custom_datatype_menu', 'ui_install_custom_optype_menu', 'ui_get_range_marker', 'ui_get_highlighted_identifier', 'ui_lookup_key_code', 'ui_load_custom_icon_file', 'ui_load_custom_icon', 'ui_free_custom_icon', 'ui_process_action', 'ui_new_code_viewer', 'ui_addons', 'ui_execute_ui_requests', 'ui_execute_ui_requests_list', 'ui_register_timer', 'ui_unregister_timer', 'ui_take_database_snapshot', 'ui_restore_database_snapshot', 'ui_set_code_viewer_line_handlers', 'ui_refresh_custom_code_viewer', 'ui_new_source_viewer', 'ui_get_tab_size', 'ui_set_menu_item_icon', 'ui_repaint_qwidget', 'ui_enable_menu_item', 'ui_custom_viewer_set_userdata', 'ui_obsolete_new_ea_viewer', 'ui_jumpto', 'ui_choose_info', 'ui_cancel_exec_request', 'ui_show_form', 'ui_unrecognized_config_directive', 'ui_add_chooser_menu_cb', 'ui_get_viewer_name', 'ui_get_output_cursor', 'ui_get_output_curline', 'ui_get_output_selected_text', 'ui_add_output_popup', 'ui_get_tform_idaview', 'ui_get_renderer_type', 'ui_set_renderer_type', 'ui_askfile2', 'ui_get_viewer_user_data', 'ui_get_viewer_place_type', 'ui_new_ea_viewer', 'ui_ea_viewer_history_push_and_jump', 'ui_ea_viewer_history_info', 'ui_last']

#os.chdir(IDAPATH)
ida = cdll.LoadLibrary(IDAPATH+"libida.so")
libc = cdll.LoadLibrary("libc.so.6")

CALLUI = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p)
def uicallback(a,b,c,d,e,f,g,h,i):
  libc.memset(b, 0, 4)
  global idle_fxn
  if c == 17: # ui_banner
    libc.memset(b, 1, 1)
    return 0
  elif c == 28: # ui_clearbreak
    return 0
  elif c == 29: # ui_wasbreak
    # ui_wasbreak, always return 0
    return 0
  #print "callback",a,b,c,d,e,f
  #return 0
  elif c == 23:
    #st = cast(d, c_char_p).value.strip()
    #print st
    """
    if "%s" in st and f != None:
      print cast(f, c_char_p).value.strip()
    """
    #print cast(f, c_char_p).value
    libc.vprintf(d, e)
    return 0
  elif c == 21:
    # MBOX
    libc.vprintf(e, f)
    print ""
    return 0

  elif c == 50:
    if d == None:
      d = 0
    if d < len(idp_notify):
      print "idp_notify",idp_notify[d]
    else:
      print "idp_notify",d

    #st = struct.unpack("I", cast(e, c_char_p).value[0:4])[0]
    #print cast(st, c_char_p).value.strip()
    #ret = ida.invoke_callbacks(0, d, e)
    #print "RETURN 0"
    # ugh hacks
    libc.memset(b, 0, 4)
    """
    if d == 2 or d == 3:
      print "returning 1"
      libc.memset(b, 1, 1)
    #if d == 0 or d == None:
      libc.memset(b, 0, 4)
    elif d == 4:
      print "newfile",cast(e, c_char_p).value.strip()
    """
    #print cast(b, POINTER(c_int)).contents
    #print cast(b, POINTER(c_int)).contents
    return 1

  print "callback", ui_msgs[c], c,d,e,f,g,h,i

  if c == 43:
    print "load_file:",cast(d, c_char_p).value.strip()
    libc.memset(b, 0, 4)
    libc.memset(b, 1, 1)
  if c == 18:
    print "got set idle",d
    idle_fxn = CFUNCTYPE(c_int)(d)
    
  return 0

fxn = CALLUI(uicallback)
# how hack is that, KFC
rsc = "\xB9"+struct.pack("I", cast(fxn, c_void_p).value)+"\xFF\xD1\x59\x83\xC4\x04\xFF\xE1"
sc = create_string_buffer(rsc)
print "mprotect", libc.mprotect(addressof(sc) & 0xFFFFF000, 0x1000, 7)
print "init_kernel", ida.init_kernel(sc, 2, argv)
#print "init_kernel", ida.init_kernel(CALLUI(uicallback), 0, None)
newfile = c_int(0)

print "init_database", ida.init_database(2, argv, pointer(newfile))
#print "init_database", ida.init_database(1, None, pointer(newfile))
print newfile

print "bedtime"
while 1:
  idle_fxn()
  time.sleep(0.1)

"""
tmp = create_string_buffer(100)
print ida.get_name(BADADDR, 0x8048431, tmp, 100)
print tmp.value
"""

"""
linput = ida.open_linput(FILE, False)
print "loaded file",hex(linput)

NEF_FIRST = 0x80
ret = ida.load_nonbinary_file(FILE, linput, ".", NEF_FIRST, None)
print "load_nonbinary_file", ret

print "save_database_ex", ida.save_database_ex("/tmp/test.idb", 0, None, None)

"""
