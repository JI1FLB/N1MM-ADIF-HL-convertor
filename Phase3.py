def phase1( adif_file ):
    
    import os

    forming_file = ""
    forming_file2 = ""

    print('*------------ phase1 ------------------')
    print('adif_file -> ', adif_file)
#    print('input_path -> ', input_path)


#------------------------------------------------------------------------
#
#   ファイルオープン
#
#

    forming_file = adif_file[:-4] + "_forming.adi"

    forming_file2 = adif_file[:-4] + "2_forming.adi"

    adi_file = open( adif_file, "r", encoding='utf-8' )
    output_log = open( forming_file2 , "w",encoding='utf-8' )


#-------------------------------------------------------------------- 
#
#   WSJT-xではタグが小文字であるため、大文字へ変換
#
#

    lines = adi_file.readlines()

    for line in lines:

        line = line.upper()
        output_log.write( line )
            
    adi_file.close()
    output_log.close()


#------------------------------------------------------------------------
#
# ADIFファイルが改行分割されたレコードを1レコードに編集
#
#

    data1=""

    adi_file = open( forming_file2,"r",encoding='utf-8' )
    output_log = open( forming_file ,"w",encoding='utf-8' )

    
    lines = adi_file.readlines()

    for line in lines:
        
        if "<CALL:"  in line:
            
            if "<EOR>" in line:
                data1=line
                output_log.write(data1)
                continue
            
            data1=line.rstrip('\n')
            continue
        
        if "<CALL:" not in line:
            
            if "<EOR>" in line:
                data1=data1 + line
                output_log.write(data1)
                data1 = ""
                continue
            
            data1= data1 + line.rstrip('\n')
            continue


        output_log.write(line)
        
    adi_file.close()
    output_log.close()

#　templary fileの削除
    os.remove(forming_file2)

    return


def phase3( adif_file ,JST_convert_flag, QSLyesno,  Remarks1, path ):
    import os
    from datetime import datetime
    from datetime import timedelta
    from datetime import time

    import pickle
    
    forming_file = ""
    HL_file = ""
    HL_log = ""
    HL_line = ""
    okng = True
    dt = ""
    t = ""
    dtstr =""
    
    print('*------------ phase3 ------------------')
    print('adif_file -> ', adif_file)
    print('QSLyesno -> ', QSLyesno)
    print('JST_convert_flag -> ', JST_convert_flag)
    print('Remarks1 -> ', Remarks1)



    #--------------------------------------------------------------------
    #
    #   変数宣言
    #

    # QSO_DB_lib.txtファイルの有無を判定する変数
    
    DBisfile=False



    #--------------------------------------------------------------------
    #
    #   ファイル名の定義
    #

    forming_file = adif_file[:-4] + "_forming.adi"
    csv_file = adif_file[:-4] + ".csv"
    
    output_log = open( forming_file ,"r",encoding='utf-8')
    ham_log = open( csv_file ,"w",encoding='utf-8')


    logs = output_log.readlines()

    #--------------------------------------------------------------------
    #
    #   QSOライブラリーのオープン
    #
    # Libraryのリロード

    if os.path.isfile(path + "/" +'QSO_DB_lib.txt'):
        DBisfile = True
        QSO_DB=set()
        f = open( path + "/" +'QSO_DB_lib.txt', 'rb')
        QSO_DB=pickle.load(f)
    else:
        DBisfile = False
        

    #--------------------------------------------------------------------
    #
    #   変数宣言
    #


    data=""
    data1=""
    data2=""
    data3=""

    log = ""
    i=0

    a = ""
    b = ""
    c = ""

    CALL = ""
    QSO_DATE = ""
    TIME_ON = ""
    FREQ = ""
    MODE = ""
    SUBMODE =""
    RST_SENT = ""
    RST_RCVD = ""
    GRIDSQUARE = ""
    APP_N1MM_EXCHANGE1 = ""
    My_multi = ""
    APP_N1MM_POINTS = ""
    okng = True
    yesno = ""
    text = ""
    FREQ_f=0.0
    sheet = ""
    line = ""
    FREQ_JARL = ""
    Power_code = False
    Power_code_input = ""

    QSO_DATE_HL = ""
    TIME_ON_HL = ""
    UTC_JST = ""
#    Remarks1=""
#    JST_convert_flag = True
    #dt = 0
    dtstr = ""
    t=set

#    QSL = "N"


    #------------------------------------------------------------------------
    #
    #   ハムログ　UTC/JST選択
    #

    if JST_convert_flag  :
        UTC_JST="J"
    else :
        UTC_JST="U"
            
    #------------------------------------------------------------------------
    #
    #   ハムログ　QSLカード発行の選択
    #

    if QSLyesno  :
        QSL = '"J"'
    else :
        QSL = '"N"'

    
    #--------------------------------------------------
    #
    #   N1MM Logger+が出力しないADIFパラメータ対策
    #

    #line = "年月日" +" "+ "時分" +" "+ "バンド" +" "+ "モード" +" "+ "交信局" +" "+ "送信RST" +" "+ "送信ナンバー" +" "+ "受信RST" +" "+ "受信ナンバー" +" "+ "マルチ" +" "+ "得点"+ "\n"
     
    #logsheet.write(line)

    for log in logs:

        if "CALL:" not in log :
            CALL = " "

        if "QSO_DATE:" not in log :
            QSO_DATE = " "

        if "TIME_ON:" not in log :
            TIME_ON = " "

        if "SECTION:" not in log :
            SECTION = " "

        if "GRIDSQUARE:" not in log :
            GRIDSQUARE = " "

        if "BAND:" not in log :
            BAND = " "

        if "STATION_CALLSIGN:" not in log :
            STATION_CALLSIGN = " "

        if "FREQ:" not in log :
            FREQ = " "

        if "CONTEST_ID:" not in log :
            CONTEST_ID = " "

        if "FREQ_RX:" not in log :
            FREQ_RX = " "

        if "<MODE:" not in log :
            MODE = " "

        if "<SUBMODE:" not in log :
            SUBMODE = " "

        if "RST_RCVD:" not in log :
            RST_RCVD = " "

        if "RST_SENT:" not in log :
            RST_SENT = " "

        if "TX_PWR:" not in log :
            TX_PWR = " "

        if "OPERATOR:" not in log :
            OPERATOR = " "

        if "CQZ:" not in log :
            CQZ = " "

        if "SRX:" not in log :
            STX = " "

        if "STX:" not in log :
            STX = " "

        if "APP_N1MM_EXCHANGE1:" not in log :
            APP_N1MM_EXCHANGE1 = " "

        if "APP_N1MM_POINTS:" not in log :
            APP_N1MM_POINTS = " "

        if "APP_N1MM_RADIO_NR:" not in log :
            APP_N1MM_RADIO_NR = " "

        if "APP_N1MM_CONTINENT:" not in log :
            APP_N1MM_CONTINENT = " "

        if "APP_N1MM_CONTACTTYPE:" not in log :
            APP_N1MM_CONTACTTYPE = " "

        if "APP_N1MM_RUN1RUN2:" not in log :
            APP_N1MM_RUN1RUN2 = " "

        if "APP_N1MM_RADIOINTERFACED:" not in log :
            APP_N1MM_RADIOINTERFACED = " "

        if "APP_N1MM_ISORIGINAL:" not in log :
            APP_N1MM_ISORIGINAL = " "

        if "APP_N1MM_NETBIOSNAME:" not in log :
            APP_N1MM_NETBIOSNAME = " "

        if "APP_N1MM_ISRUNQSO:" not in log :
            APP_N1MM_ISRUNQSO = " "

        if "EOR>" not in log :
            EOR = " "

        if "AGE" not in log :
            AGE = " "
            
        if "COMMENT" not in log :
            COMMENT = " "
            
        if "APP_N1MM_MISCTEXT:" not in log :
            APP_N1MM_MISCTEXT = " "

            
    #--------------------------------------------------
    #
    #       JARL LOG作成　　ADIFフォーマットから要素抽出
    #

            
        log = log.replace(' "','')
        log = log.rstrip('\n')
        log = log.lstrip()
        log = log.split("<")

        for i in log:

            if "CALL:" in i :
                a = i
                b = a[5:7]
                b1= b.rstrip(">")
                b2 = len(b1)
                CALL = a[6+b2:7+b2+int(b1)]
                CALL = CALL.rstrip()

            if "QSO_DATE:" in i:
                a = i
                b = a[9:11]
                b1 = b.rstrip(">")
                b2 = len(b1)
                QSO_DATE = a[10+b2:11+b2+int(b1)]
                QSO_DATE = QSO_DATE.rstrip()
                
            if "TIME_ON:" in i:
                a = i
                b = a[8:10]
                b1= b.rstrip(">")
                b2 = len(b1)
                TIME_ON = a[9+b2:10+b2+int(b1)-3]       #   6桁を4桁に変更。秒単位を削除。
                TIME_ON = TIME_ON.rstrip()

                dtstr= QSO_DATE +" "+ TIME_ON
                if JST_convert_flag == True : 
                    dt = datetime.strptime(dtstr, '%Y%m%d %H%M')+timedelta(hours=9)
                    dHL = dt

                elif JST_convert_flag == False : 
                    dt = datetime.strptime(dtstr, "%Y%m%d %H%M")
                    dHL = dt


                
                t=str(dt).split(" ")
                
                QSO_DATE_JARL = t[0]

                c1 = str(t[1])
                c2 = c1[0:5]
                TIME_ON_JARL =  c2             


                dHL=dt.strftime("%Y/%m/%d")

                tHL=str( dHL ).split(" ")
                QSO_DATE_HL = tHL[0]

                TIME_ON_HL =  c2  + UTC_JST

                        

            if "SECTION:" in i:
                a = i
                b = a[8:10]
                b1= b.rstrip(">")
                b2 = len(b1)
                SECTION = a[9+b2:10+b2+int(b1)]
                SECTION = SECTION.rstrip()

            if "BAND:" in i:
                a = i
                b = a[5:7]
                b1= b.rstrip(">")
                b2 = len(b1)
                BAND = a[6+b2:7+b2+int(b1)]
                BAND = BAND.rstrip()

            if "STATION_CALLSIGN:" in i:
                a = i
                b = a[17:19]
                b1= b.rstrip(">")
                b2 = len(b1)
                STATION_CALLSIGN = a[18+b2:19+b2+int(b1)]
                STATION_CALLSIGN = STATION_CALLSIGN.rstrip()

            if "FREQ:" in i:
                a = i
                b = a[5:7]
                b1= b.rstrip(">")
                b2 = len(b1)
                FREQ = a[6+b2:7+b2+int(b1)]
                FREQ = FREQ.rstrip()
                FREQ_f = float(FREQ)
                
                if   1.8 <= FREQ_f and FREQ_f <= 2.0 :
                    FREQ_JARL = "1.9"
                    
                elif   3.5 <= FREQ_f and FREQ_f <= 4.0 :
                    FREQ_JARL = "3.5"
                    
                elif   7.0 <= FREQ_f and FREQ_f <= 7.3 :
                    FREQ_JARL = "7"
                    
                elif   14.0 <= FREQ_f and FREQ_f <= 14.35 :
                    FREQ_JARL = "14"
                    
                elif   21.0 <= FREQ_f and FREQ_f <= 21.45 :
                    FREQ_JARL = "21"
                    
                elif   28.0 <= FREQ_f and FREQ_f <= 29.7 :
                    FREQ_JARL = "28"
                    
                elif 50.0 <= FREQ_f and FREQ_f <= 54.0 :
                    FREQ_JARL = "50"
                    
                elif 144.0 <= FREQ_f and FREQ_f <= 146.0 :
                    FREQ_JARL = "144"
                    
                elif 430.0<= FREQ_f and FREQ_f <= 440.0 :
                    FREQ_JARL = "430"

                elif 1240.0<= FREQ_f and FREQ_f <= 1300.0 :
                    FREQ_JARL = "1.2G"

                elif 2300.0<= FREQ_f and FREQ_f <= 2450.0 :
                    FREQ_JARL = "2.4G"            

                elif 5650.0<= FREQ_f and FREQ_f <= 5925.0 :
                    FREQ_JARL = "5.6G"

                elif 10000.0<= FREQ_f and FREQ_f <= 10500.0 :
                    FREQ_JARL = "10.1G"

            if "COMMENT:" in i:
                a = i
                b = a[8:10]
                b1= b.rstrip(">")
                b2 = len(b1)
                COMMENT = a[9+b2:10+b2+int(b1)]
                COMMENT = COMMENT.rstrip()
                COMMENT = COMMENT.upper()
                    
            if "CONTEST_ID:" in i:
                a = i
                b = a[11:13]
                b1= b.rstrip(">")
                b2 = len(b1)
                CONTEST_ID = a[12+b2:13+b2+int(b1)]
                CONTEST_ID = CONTEST_ID.rstrip()
                
            if "FREQ_RX:" in i:
                a = i
                b = a[8:10]
                b1= b.rstrip(">")
                b2 = len(b1)
                FREQ_RX = a[9+b2:10+b2+int(b1)]
                FREQ_RX = FREQ_RX.rstrip()
                
# 2019/12/10 WSJTXのADIFファイルに対応するため、iの部分一致から特定文字の完全一致へ変更
                
            if "MODE:" == i[:5] :
                a = i
                b = a[5:7]
                b1= b.rstrip(">")
                b2 = len(b1)
                MODE = a[6+b2:7+b2+int(b1)]
                MODE = MODE.rstrip()
                
# 2019/12/10 WSJTXのADIFファイルに対応するため、SUBMODEを追加
# 2019/12/10 WSJTXのADIFファイルに対応するため、iの部分一致から特定文字の完全一致へ変更

            if "SUBMODE:" == i[:8] :
                a = i
                b = a[8:10]
                b1= b.rstrip(">")
                b2 = len(b1)
                SUBMODE = a[9+b2:10+b2+int(b1)]
                SUBMODE = SUBMODE.rstrip()
                
            if "RST_RCVD:" in i:
                a = i
                b = a[9:11]
                b1= b.rstrip(">")
                b2 = len(b1)
                RST_RCVD = a[10+b2:11+b2+int(b1)]
                RST_RCVD = RST_RCVD.rstrip()

            if "RST_SENT:" in i:
                a = i
                b = a[9:11]
                b1= b.rstrip(">")
                b2 = len(b1)
                RST_SENT = a[10+b2:11+b2+int(b1)]
                RST_SENT = RST_SENT.rstrip()

            if "TX_PWR:" in i:
                a = i
                b = a[7:9]
                b1= b.rstrip(">")
                b2 = len(b1)
                TX_PWR = a[8+b2:9+b2+int(b1)]
                TX_PWR = TX_PWR.rstrip()

            if "OPERATOR:" in i:
                a = i
                b = a[9:11]
                b1= b.rstrip(">")
                b2 = len(b1)
                OPERATOR = a[10+b2:11+b2+int(b1)]
                OPERATOR = OPERATOR.rstrip()

            if "GRIDSQUARE:" == i[:11] :
                a = i
                b = a[11:13]
                b1= b.rstrip(">")
                b2 = len(b1)

#                print( a )
#                print( b )
#                print( b1 )
#                print( str(b2) )
                
                if b2 == 0 :
                    GRIDSQUARE = ""
                    print( GRIDSQUARE )
                else :
                    GRIDSQUARE = a[12+b2:13+b2+int(b1)]
                    GRIDSQUARE = GRIDSQUARE.rstrip()
#                    print( GRIDSQUARE )

            if "CQZ:" in i:
                a = i
                b = a[4:6]
                b1= b.rstrip(">")
                b2 = len(b1)
                CQZ = a[5+b2:6+b2+int(b1)]
                CQZ = CQZ.rstrip()

            if "SRX:" in i:
                a = i
                b = a[4:6]
                b1= b.rstrip(">")
                b2 = len(b1)
                SRX = a[5+b2:6+b2+int(b1)]
                SRX = SRX.rstrip()                

            if "STX:" in i:
                a = i
                b = a[4:6]
                b1= b.rstrip(">")
                b2 = len(b1)
                STX = a[5+b2:6+b2+int(b1)]
                STX = STX.rstrip()

            if "APP_N1MM_EXCHANGE1:" in i:
                a = i
                b = a[19:21]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_EXCHANGE1 = a[20+b2:21+b2+int(b1)]
                APP_N1MM_EXCHANGE1 = APP_N1MM_EXCHANGE1.rstrip()

            if "APP_N1MM_POINTS:" in i:
                a = i
                b = a[16:18]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_POINTS = a[17+b2:18+b2+int(b1)]
                APP_N1MM_POINTS = APP_N1MM_POINTS.rstrip()

            if "APP_N1MM_RADIO_NR:" in i:
                a = i
                b = a[18:20]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_RADIO_NR = a[19+b2:20+b2+int(b1)]
                APP_N1MM_RADIO_NR = APP_N1MM_RADIO_NR.rstrip()

            if "APP_N1MM_CONTINENT:" in i:
                a = i
                b = a[19:21]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_CONTINENT = a[20+b2:21+b2+int(b1)]
                APP_N1MM_CONTINENT = APP_N1MM_CONTINENT.rstrip()

            if "APP_N1MM_CONTACTTYPE:" in i:
                a = i
                b = a[21:23]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_CONTACTTYPE = a[22+b2:23+b2+int(b1)]
                APP_N1MM_CONTACTTYPE = APP_N1MM_CONTACTTYPE.rstrip()

            if "APP_N1MM_RUN1RUN2:" in i:
                a = i
                b = a[18:20]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_RUN1RUN2 = a[19+b2:20+b2+int(b1)]
                APP_N1MM_RUN1RUN2 = APP_N1MM_RUN1RUN2.rstrip()         

            if "APP_N1MM_RADIOINTERFACED:" in i:
                a = i
                b = a[25:27]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_RADIOINTERFACED = a[26+b2:27+b2+int(b1)]
                APP_N1MM_RADIOINTERFACED = APP_N1MM_RADIOINTERFACED.rstrip()

            if "APP_N1MM_ISORIGINAL:" in i:
                a = i
                b = a[20:22]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_ISORIGINAL = a[21+b2:22+b2+int(b1)]
                APP_N1MM_ISORIGINAL = APP_N1MM_ISORIGINAL.rstrip()

            if "APP_N1MM_NETBIOSNAME:" in i:
                a = i
                b = a[21:23]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_NETBIOSNAME = a[22+b2:23+b2+int(b1)]
                APP_N1MM_NETBIOSNAME = APP_N1MM_NETBIOSNAME.rstrip()

            if "APP_N1MM_ISRUNQSO:" in i:
                a = i
                b = a[18:20]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_ISRUNQSO = a[19+b2:20+b2+int(b1)]
                APP_N1MM_ISRUNQSO = APP_N1MM_ISRUNQSO.rstrip()

            if "AGE:" in i:
                a = i
                b = a[4:6]
                b1= b.rstrip(">")
                b2 = len(b1)
                AGE = a[5+b2:6+b2+int(b1)]
                AGE = AGE.rstrip()

            if "APP_N1MM_MISCTEXT:" in i:
                a = i
                b = a[18:20]
                b1= b.rstrip(">")
                b2 = len(b1)
                APP_N1MM_MISCTEXT = a[19+b2:20+b2+int(b1)]
                APP_N1MM_MISCTEXT = APP_N1MM_MISCTEXT.rstrip()                


    #--------------------------------------
    #
    #   ハムログCSVファィル出力
    #
    #    CALL          Date      time    his   My     Freq   Mode  code    GL   QSL  His Name     QTH      Remarks1             Remark2    ?
    #    "JA6WFM/6","18/08/04","18:06J","599","599","21.057","CW","   ","    ","J","         ","        ","2018 FD Contest "," 21.057MHz","0"
    #
    #

#
# QSO B4のチェック
#
#   QSO_DB_libにQSOが登録されていない場合には、New QSOとしてQSLカードを発行。
#   
        if DBisfile :
            if QSLyesno :
                        
                QSO_data = CALL+'-'+BAND+'-'+MODE+'\n'
            
                if QSO_data in QSO_DB :
                    QSL = '"N"'
                else :
                    QSL = '"J"'
                    QSO_DB.add( QSO_data )


#
# ハムログファイルの出力
#
# old        HL_line = '"'+CALL+'"'+","+'"'+QSO_DATE_HL+'"'+","+'"'+TIME_ON_HL+'"'+","+'"'+RST_SENT+'"'+","+'"'+RST_RCVD+'"'+","+'"'+str('{:.3f}'.format(float(FREQ)))+'"'+","+'"'+MODE+'"'+","+'""'+","+'"'+GRIDSQUARE+'"'+","+'"J"'+","+'""'+","+'""'+","+'"'+Remarks1+'"'+","+'"'+FREQ+"MHz"+'"'+","+'"'+"0"+'"'+"\n"
                
        HL_line = '"'+CALL+'"'+","+'"'+QSO_DATE_HL+'"'+","+'"'+TIME_ON_HL+'"'+","+'"'+RST_SENT+'"'+","+'"'+RST_RCVD+'"'+","+'"'+str('{:.3f}'.format(float(FREQ)))+'"'+","+'"'+MODE+'"'+","+'""'+","+'"'+GRIDSQUARE+'"'+","+ QSL+","+'""'+","+'""'+","+'"'+Remarks1+'"'+","+'"'+FREQ+"MHz"+'"'+","+'"'+"0"+'"'+"\n"
                
        ham_log.write( HL_line )


    output_log.close()
    ham_log.close()    
    
    
    
    
#　templary fileの削除
    os.remove(forming_file)

 
    if DBisfile :    
    # QSOライブラリーのクローズ
        f.close()

    # 新規QSOライブラリーの保存とクローズ
        f = open( path + "/" +'QSO_DB_lib.txt', 'wb')
        pickle.dump(QSO_DB, f)
        f.close()


    return

