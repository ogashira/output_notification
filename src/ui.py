# -*- coding: utf-8 -*-
import tkinter as tk
import re
from tkinter import ttk, messagebox
from typing import List, Dict, Any

# グローバル変数の宣言（各関数からアクセスするため）
root = None
combobox = None
dest_combobox = None
deliv_combobox = None
label_combobox = None
can_combobox = None
type_var = None
cert_var = None
custCD_combobox = None
delivCD_combobox = None
fmt_combobox = None
result_label = None
extra_frame = None
button_frame = None
parts_list = None
tokuis_dict = None

# 表示切り替え用のフレーム
dest_frame = None
deliv_frame = None
cert_frame = None
label_frame = None
can_frame = None


def init_visibility():
    """品番の入力内容に応じてフィールドの表示/非表示を切り替える"""
    if not combobox:
        return
    
    # 一旦すべて非表示にする
    dest_frame.pack_forget()
    deliv_frame.pack_forget()
    cert_frame.pack_forget()
    label_frame.pack_forget()
    extra_frame.pack_forget()
    can_frame.pack_forget()



def update_visibility(is_export, is_furikae_hinban):
    """品番の入力内容に応じてフィールドの表示/非表示を切り替える"""
    if not combobox:
        return
        
    part = combobox.get()

    
    # 一旦すべて非表示にする
    dest_frame.pack_forget()
    deliv_frame.pack_forget()
    cert_frame.pack_forget()
    label_frame.pack_forget()
    extra_frame.pack_forget()
    can_frame.pack_forget()
    
    if not part:
        # 品番が空の場合は何もしない（radio_frameとcomboboxのみの状態）
        return

    if is_furikae_hinban:
        dest_frame.pack(pady=5, before=result_label)
        deliv_frame.pack(pady=5, before=result_label)
    elif is_export:
        # "-EX"で終わる場合は向け先・納入先を表示
        dest_frame.pack(pady=5, before=result_label)
        deliv_frame.pack(pady=5, before=result_label)
        label_frame.pack(pady=5, before=result_label)
        can_frame.pack(pady=5, before=result_label)
    else:
        # それ以外の場合は成績書チェックボックスを表示
        cert_frame.pack(pady=10, before=result_label)
        # チェックが入っていれば追加フィールドも表示
        if cert_var.get():
            extra_frame.pack(pady=10, before=result_label)


def on_select(event=None):

    part = combobox.get()
    
    is_furikae_hinban = False
    is_export = False
    pattern_export = r"-EX(?:-[A-Z0-9]+)?$"
    pattern_furikae = r"-EX-[A-Z0-9]+$" # S4-SR001A-U-R-EX-TH
    if re.search(pattern_export, part):
        is_export = True

    if re.search(pattern_furikae, part):
        is_furikae_hinban = True


    prod_type = type_var.get()

    """選択内容が更新されたときに実行される関数"""
    update_visibility(is_export, is_furikae_hinban)

    
    result_text = f"区分: {prod_type}\n品番: {part}"
    
    if is_export:
        dest = dest_combobox.get()
        deliv = deliv_combobox.get()
        label = label_combobox.get()
        can = can_combobox.get()
        result_text += f"\n向け先: {dest}\n納入先: {deliv}\n製品ラベル: {label}\n輸出缶: {can}"
    elif part:
        if cert_var.get():
            cust_code = custCD_combobox.get()
            deliv_code = delivCD_combobox.get()
            fmt = fmt_combobox.get()
            result_text += f"\n--- 成績書情報 ---\n得意先: {cust_code}\n納入先: {deliv_code}\nFormat: {fmt}"
    
    result_label.config(text=result_text)

def check_on_leave(event):
    """別の作業に移ろうとした（フォーカスが外れた）時のチェック処理"""
    # 1. 新しくフォーカスが移った先のウィジェット名を取得
    # root.focus_get() はドロップダウンリスト(popdown)にフォーカスがある際に
    # Tkinterの管理外のため KeyError: 'popdown' が発生します。
    # そのため root.tk.call('focus') で Tcl のウィジェット名文字列を安全に取得します。
    try:
        focused_widget_name = str(root.tk.call('focus'))
    except (KeyError, tk.TclError):
        return

    # 2. フォーカス移動先が「ドロップダウンリスト（popdown）」や combobox 自身だった場合はスルーする
    if focused_widget_name:
        if 'popdown' in focused_widget_name or focused_widget_name == str(combobox):
            return     # 絞り込み中なので警告を出さない

    # 3. 本当に別の入力欄やボタンに移った場合のみチェックを実行
    current_val = combobox.get()
    allowed_values = combobox['values']

    # 空文字の場合はスルー（未入力許可の場合）
    if not current_val:
        return
        
    # リストの完全一致に含まれていない場合だけ警告
    if current_val not in allowed_values:
        messagebox.showerror("エラー", f"「{current_val}」はリストにありません。リストから選択してください。")
        combobox.set("")
        combobox.focus_set()


def toggle_cert_fields():
    """チェックボックスの状態に応じて追加フィールドの表示/非表示を切り替える"""
    on_select()


def filter_parts(event):
    """入力された文字で品番リストをフィルタリングする関数"""
    value = event.widget.get()

    if value == '':
        combobox['values'] = parts_list
    else:
        data = [item for item in parts_list if value.lower() in item.lower()]
        combobox['values'] = data
    event.widget.event_generate('<Down>')
    # フィルタリング時にも表示を更新
    on_select()

def filter_custCD(event):
    """custCDでdelivCDをフィルタリングする関数"""
    value = custCD_combobox.get()

    tk.Label(extra_frame, text="納入先コード:").grid(row=1, column=0, sticky="w", pady=2)
    delivCD_combobox['values'] = tokuis_dict.get(value, [])
    event.widget.event_generate('<Down>')
    # フィルタリング時にも表示を更新
    on_select()


def check_is_ok_input(ui_infos: Dict[str, Any])-> bool:
    '''空白がないかチェックする'''

    is_furikae_hinban = False
    pattern_furikae = r"-EX-[A-Z0-9]+$" # S4-SR001A-U-R-EX-TH
    if re.search(pattern_furikae, ui_infos['hinban']):
        is_furikae_hinban = True

    is_ok_furiake_hinban = (is_furikae_hinban and
                            ui_infos['mukesaki'] != "" and 
                            ui_infos['nonyusaki'] != ""  
                            )

    is_ok_for_export = (is_furikae_hinban == False and
                        ui_infos['is_export'] and 
                        ui_infos['mukesaki'] != "" and 
                        ui_infos['nonyusaki'] != "" and 
                        ui_infos['label'] != "" and 
                        ui_infos['can'] != ""
                        )

    is_ok_for_domestic = (is_furikae_hinban == False and
                          ui_infos['is_export'] == False and
                          ui_infos['is_coa_need'] == True and
                          ui_infos['tokuiCD'] != "" and
                          ui_infos['nonyuCD'] != "" and
                          ui_infos['format'] != ""
                         ) or (
                         is_furikae_hinban == False and
                         ui_infos['is_export'] == False and
                         ui_infos['is_coa_need'] == False
                         )

    if is_ok_furiake_hinban:
        return True
    if is_ok_for_export:
        return True
    if is_ok_for_domestic:
        return True

    return False
                        
def press_start():
    """Startボタンが押された時の処理"""
    prod_type: str = type_var.get()
    part_no: str = combobox.get() # hinban
    
    is_export = False
    pattern = r"-EX(?:-[A-Z0-9]+)?$"
    if re.search(pattern, part_no):
        is_export = True

    destination: str = ""
    deliv:str = ""
    label = '日本'
    cert_needed: str = ""
    cust_code: str = ""
    deliv_code: str = ""
    fmt: str = ""
    can: str = ""
    
    if is_export:
        destination = dest_combobox.get()
        deliv = deliv_combobox.get()
        label = label_combobox.get()
        can = can_combobox.get()
    else:
        cert_needed = cert_var.get()
        if cert_needed:
            cust_code = custCD_combobox.get()
            deliv_code = delivCD_combobox.get()
            fmt = fmt_combobox.get()

    ui_infos: Dict[str, Any] = {}
    ui_infos['is_export'] = is_export
    ui_infos['order_or_stocked'] = prod_type
    ui_infos['hinban'] = part_no
    ui_infos['mukesaki'] = destination
    ui_infos['nonyusaki'] = deliv
    ui_infos['label'] = label
    ui_infos['is_coa_need'] = cert_needed
    ui_infos['tokuiCD'] = cust_code
    ui_infos['nonyuCD'] = deliv_code
    ui_infos['format'] = fmt
    ui_infos['can'] = can


    if not check_is_ok_input(ui_infos): 
        messagebox.showerror("エラー", f"項目は全て入力してください。")
        return

    try:
        from flow import Flow
        Flow.start( ui_infos)

        root.destroy()
    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")

def press_cancel():
    """Cancelボタンが押された時の処理"""
    root.destroy()

def run(hinbans: List[str], mukesakis_export: List[str], 
        nonyusakis: List[str], seihinLabels: List[str], 
        local_tokuis_dict: Dict[str, List[str]], coaFormats: List[str],
        cans: List[str])-> None:
    """UIを起動するメイン関数"""
    global root, combobox, dest_combobox, deliv_combobox, type_var, cert_var
    global custCD_combobox, delivCD_combobox, fmt_combobox, result_label
    global extra_frame, button_frame, parts_list
    global dest_frame, deliv_frame, cert_frame
    global label_frame, label_combobox, tokuis_dict
    global can_frame, can_combobox

    tokuis_dict = local_tokuis_dict

    tokuis: List[str] = sorted(list(set(tokuis_dict.keys())))

    root = tk.Tk()
    root.title("開発アウトプット登録(営業用)")
    root.geometry("450x750")

    # --- 区分セクション ---
    tk.Label(root, text="製品区分:", font=("MS Gothic", 10, "bold")).pack(pady=(20, 0))
    type_var = tk.StringVar(value="受注製品")
    radio_frame = tk.Frame(root)
    radio_frame.pack(pady=5)
    tk.Radiobutton(radio_frame, text="受注製品", variable=type_var, value="受注製品", command=on_select).pack(side="left", padx=10)
    tk.Radiobutton(radio_frame, text="見込製品", variable=type_var, value="見込製品", command=on_select).pack(side="left", padx=10)

    # --- 品番セクション ---
    parts_list = hinbans
    tk.Label(root, text="品番 (一部入力してEnterで検索):", font=("MS Gothic", 10, "bold")).pack(pady=(10, 0))
    combobox = ttk.Combobox(root, values=parts_list, width=35, state="normal")
    combobox.pack(pady=5)
    combobox.bind("<Return>", filter_parts)
    combobox.bind("<<ComboboxSelected>>", on_select)
    combobox.bind("<FocusOut>", check_on_leave)

    # --- 向け先フレーム (初期状態では隠す) ---
    dest_list = mukesakis_export
    dest_frame = tk.Frame(root)
    tk.Label(dest_frame, text="向け先:", font=("MS Gothic", 10, "bold")).pack(pady=(10, 0))
    dest_combobox = ttk.Combobox(dest_frame, values=dest_list, width=35, state="readonly")
    dest_combobox.pack(pady=5)
    dest_combobox.bind("<<ComboboxSelected>>", on_select)

    # --- 納入先フレーム (初期状態では隠す) ---
    deliv_list = nonyusakis
    deliv_frame = tk.Frame(root)
    tk.Label(deliv_frame, text="納入先:", font=("MS Gothic", 10, "bold")).pack(pady=(10, 0))
    deliv_combobox = ttk.Combobox(deliv_frame, values=deliv_list, width=35, state="readonly")
    deliv_combobox.pack(pady=5)
    deliv_combobox.bind("<<ComboboxSelected>>", on_select)

    # --- ラベルフレーム (初期状態では隠す) ---
    label_list = seihinLabels
    label_frame = tk.Frame(root)
    tk.Label(label_frame, text="製品ラベル:", font=("MS Gothic", 10, "bold")).pack(pady=(10, 0))
    label_combobox = ttk.Combobox(label_frame, values=label_list, width=35, state="readonly")
    label_combobox.pack(pady=5)
    label_combobox.bind("<<ComboboxSelected>>", on_select)

    # --- 缶フレーム (初期状態では隠す) ---
    can_list = cans
    can_frame = tk.Frame(root)
    tk.Label(can_frame, text="輸出缶:", font=("MS Gothic", 10, "bold")).pack(pady=(10, 0))
    can_combobox = ttk.Combobox(can_frame, values=can_list, width=35, state="readonly")
    can_combobox.pack(pady=5)
    can_combobox.bind("<<ComboboxSelected>>", on_select)

    # --- 成績書フレーム (初期状態では隠す) ---
    cert_frame = tk.Frame(root)
    cert_var = tk.BooleanVar(value=False)
    tk.Checkbutton(cert_frame, text="成績書必要", variable=cert_var, command=toggle_cert_fields, font=("MS Gothic", 10, "bold")).pack(pady=10)

    # --- 追加フィールドフレーム (成績書用) ---
    extra_frame = tk.Frame(root, bd=1, relief="solid", padx=10, pady=10)
    tk.Label(extra_frame, text="得意先コード:").grid(row=0, column=0, sticky="w", pady=2)
    custCD_combobox = ttk.Combobox(extra_frame, values=tokuis, state="readonly")
    custCD_combobox.grid(row=0, column=1, pady=2)
    custCD_combobox.bind("<<ComboboxSelected>>", on_select)
    delivCD_combobox = ttk.Combobox(extra_frame, values= [], state="readonly")
    custCD_combobox.bind("<<ComboboxSelected>>", filter_custCD)
    delivCD_combobox.grid(row=1, column=1, pady=2)
    delivCD_combobox.bind("<<ComboboxSelected>>", on_select)
    tk.Label(extra_frame, text="成績書フォーマット:").grid(row=2, column=0, sticky="w", pady=2)
    fmt_combobox = ttk.Combobox(extra_frame, values=coaFormats, state="readonly")
    fmt_combobox.grid(row=2, column=1, pady=2)
    fmt_combobox.bind("<<ComboboxSelected>>", on_select)

    # --- 結果表示ラベル ---
    result_label = tk.Label(root, text="選択内容: 未確定", fg="blue", justify="left", font=("MS Gothic", 11))
    result_label.pack(pady=20)

    # --- ボタンセクション ---
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Start", command=press_start, width=15, bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", command=press_cancel, width=15, bg="lightcoral", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    # 初期表示状態の適用
    init_visibility()
    
    root.mainloop()
