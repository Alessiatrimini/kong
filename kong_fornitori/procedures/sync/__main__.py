from IPython import embed
from datetime import datetime
from fclass.DataBaseExecuter import DataBaseExecuter as de
from fclass.SyncSapSupplier import SyncSapSupplier as SapSyncer
from config import *



def main():
    print("start")

    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    embed()
    assert(False)
    #Anagrafica generica
    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "anagrafica_fornitori",  "", "mongo")
    fornitori_to_sync = mongodb_anafor.selectbyqry({"syncedon": {"$eq": []}})
    
    # mysqldb.dblog("sync_fornitori", "inizio") 

    az_partner = mysqldb.selectbyqry(QRY_AZIENDE)

    if az_partner.empty:
        mysqldb.dblog("sync_fornitori", "Non ci sono aziende da sincornizzare")   
    else:
        #ciclo for sulle row di az_partner
        for j, row in az_partner.iterrows():
            idaz = row.idazienda
            idprocedura = row.idprocedura
            iderp = row.iderp

            #se la procedura impostata è di tipo automatico
            if idprocedura == 1:
                #SAP
                if iderp == 2:
                    qryerp = f"""SELECT ip, dbname, user, psw from erpconn_partner where idazienda = {idaz}"""
                    erp_data = mysqldb.selectbyqry(qryerp)
                    if ((erp_data.isna().sum().sum() != 0) | (erp_data.empty)):
                        mysqldb.dblog("sync_fornitori", f"Missing data in erpconn_partner for idazienda {idaz}")
                        pass
                    else:
                        for i, row_f in fornitori_to_sync.iterrows():
                            root_url = HTTPS_ROOT + erp_data.iloc[0].ip                    
                            sap_syncer = SapSyncer(root_url, row_f, erp_data.iloc[0])
                            try:
                                sap_syncer.sync_bp()
                                row_f["syncedon"].append(idaz)
                                mongodb_anafor.update_mg({"_id" : row_f._id},row_f.to_dict())
                                
                            except Exception as e:
                                now = datetime.now()
                                now = now.strftime("%d/%m/%Y, %H:%M:%S")
                                mongodb = de(mongoKong['conn_str'], mongoKong['database'],  "sync_notification",  "", "mongo")
                                mongodb.executeqry({"idazienda" : idaz, "messaggio": f"Errore nella sincronizzazione di {row_f.ragsoc} con PIVA {row_f.piva}", "errore" : e, "dtm" : now})
                         

                #AS400
                elif iderp == 1:
                    qryerp = f"""SELECT ip, dbname, user, psw, file from erpconn_partner where idazienda = {idaz}"""
                    erp_data = mysqldb.selectbyqry(qryerp)
                    if ((erp_data.isna().sum().sum() != 0) | (erp_data.empty)):
                        mysqldb.dblog("sync_fornitori", f"Missing data in erpconn_partner for idazienda {idaz}")
                        pass
                    else:
                        print('scrivo in as')
                
                #INVALID ERP
                else:
                    mysqldb.dblog("sync_fornitori", f"Invalid ERP type for idazienda {idaz}")
                    #pass








        


if __name__ == "__main__":
    main()
    