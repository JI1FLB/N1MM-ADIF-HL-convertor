import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import filedialog

from Phase3 import phase3,phase1


#Tk class generating
root = tk.Tk()


# screen size
root.geometry("700x250")


# screen title
root.title("N1MM to JARL log converter")


# パラメータ
folder_path = tk.StringVar()
csv_folder_path = tk.StringVar()
form_file = tk.StringVar()
adif_file = tk.StringVar()
csv_file = tk.StringVar()
log_file = tk.StringVar()
HL_file = tk.StringVar()
input_path = tk.StringVar()


def ask_adif():
    """　adif.adiファイル選択ボタンの動作
    """
    
    input_path = filedialog.askdirectory()
    adif_f = filedialog.askopenfilename(filetypes =  [('テキストファイル','*.adi')] , initialdir = input_path )
    folder_path.set(input_path)
    adif_file.set(adif_f)
    
    print( "-------- ask_adif() " ) 
    print( "input_path: ", input_path )
    print( "folder_path: ", folder_path )
    print( "adif_f   ; ", adif_f )
    print( "adif_file: ",adif_file )

    return


def ask_csv():
    """　CSVファイル選択ボタンの動作
    """
    output_path = filedialog.askdirectory()
    csv_f = filedialog.asksaveasfilename(filetypes =  [('テキストファイル','*.csv')] , initialdir = output_path )
    csv_folder_path.set(output_path)
    csv_file.set(csv_f)

    output_file = open( csv_f, "w+", encoding = "utf-8" )
    output_file.close()
    
    print( "-------- ask_csv() " ) 
    print( "output_path: ", output_path )
    print( "csv_folder_path: ", csv_folder_path )
    print( "csv_f   ; ", csv_f )
    print( "csv_file: ",csv_file )

    return


def data_clear():
    Remarks1.delete(0, tk.END)
    JST_convert_flag.set(False)
    QSLyesno.set(False)
    csv_file.set('')
    adif_file.set('')


def log_generate() :
    path = folder_path.get()
    adif_file_path = adif_file.get()
#    csv_file_path = csv_file.get()

    #Phase3を起動

    QSL = QSLyesno.get()
    JST_conv = JST_convert_flag.get()

    phase1( adif_file_path )
#    phase3( adif_file_path, csv_file_path, JST_conv, QSL, Remarks1.get(), folder_path )
    phase3( adif_file_path, JST_conv, QSL, Remarks1.get() , path)


  
def closing():
#    exit()
    root.destroy()


# チェックON・OFF変数
JST_convert_flag = tk.BooleanVar()
JST_convert_flag.set(False)

QSLyesno = tk.BooleanVar()
QSLyesno.set(False)


# check botton
check_JST_convert_flag = tk.Checkbutton(root, variable = JST_convert_flag , text ="ロギングはUTCでJSTに変換しますか？")
check_JST_convert_flag.place(x=140, y=30)

check_QSLyesno = tk.Checkbutton(root, variable = QSLyesno , text ="QSLカードを発行しますか？")
check_QSLyesno.place(x=140, y=50)


# label
Remarks1 = tk.Label(        text="Hamlog Remarks1: ")
Remarks1.place(x=30, y=90)
label_top = tk.Label( text ="N1MM+ ADIFファイルからJARLコンテストログ生成ツール")
label_top.pack()

label_term1 = tk.Label( text ="1.パラメータ設定")
label_term1.place(x=10,y=30)

label_term2 = tk.Label( text ="2.ADIFファイルの指定")
label_term2.place(x=10,y=130)

#label_term2 = tk.Label( text ="3.CSVファイル名指定")
#label_term2.place(x=10,y=170)

label_term2 = tk.Label( text ="3.Turbo HAM log CSVファイル生成")
label_term2.place(x=10,y=170)


# ウィジット作成（form.txtファイル）
#form_label = tk.Label(root, text="ADIFファイルの指定")
#form_label.place(x=30, y=170)
#form_box = tk.Entry(root, textvariable= folder_path, width=80)
form_box = tk.Entry(root, textvariable= adif_file, width=80)
form_box.place(x=145, y=130)
form_btn = tk.Button(root, text="参照", command=ask_adif)
form_btn.place(x=650, y=130)


#csv_box = tk.Entry(root, textvariable= csv_file, width=80)
#csv_box.place(x=145, y=170)
#csv_btn = tk.Button(root, text="参照", command=ask_csv)
#csv_btn.place(x=650, y=170)


# text box
Remarks1 = tk.Entry(width=40)
Remarks1.place(x=145,y=90)


clear_Button = tk.Button(root,text='パラメータClear', command = data_clear )
clear_Button.place(x=350 , y=210)


okButton =tk.Button( root, text='Turbo HAM log CSVファイル生成', command = log_generate )
okButton.place(x=40 , y=210)

closeButton =tk.Button( root, text='Close', command = closing )
closeButton.place(x=600 , y=210)


root.mainloop()
