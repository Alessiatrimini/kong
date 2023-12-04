
SAP_LOGIN_API = ":50000/b1s/v1/Login"
SAP_BP = ":50000/b1s/v1/BusinessPartners"
SAP_BP_ID = ":50000/b1s/v1/BusinessPartners?$filter=CardType eq 'cSupplier'&$orderby=CardCode desc"
LEN_BP_ID = 7
accepted_status = [200, 201, 204]

class SyncSapSupplier(): 

    def __init__(self, root_url: str, supplier_data, erp_data):
        self.supplier_data = supplier_data
        self.erp_data = erp_data
        self.root_url = root_url

    def __login(self):
        import requests
        body = {"UserName": self.erp_data.user,
                "Password": self.erp_data.psw,
                "CompanyDB":self.erp_data.dbname
                }
        login = requests.post(self.root_url + SAP_LOGIN_API, json=body, verify = False)
        if login.status_code in accepted_status:
            token = login.json()["SessionId"]
            cookies = {"B1SESSION": token,
                        "ROUTEID": ".node4"}
            self.cookies = cookies
        else:
            Exception(f"Errore nel login status code {login.status_code}")

    def __logout(self):
        import requests

        logout = requests.post(self.root_url + SAP_BP,
                cookies=self.cookies,
                verify=False)
        if logout.status_code in accepted_status:
            return "1"
        else:
            Exception(f"Errore nel login status code {login.status_code}")


    def getbpid(self):
        import requests
        self.__login()
        result = requests.get(self.root_url + SAP_BP_ID,
                cookies=self.cookies,
                verify=False)
        self.__logout()
        if result.status_code not in accepted_status:
            Exception(f"Errore nella richiesta del BP code status code {result.status_code}")
        else: 
            actual_id = result.json()["value"][0]["CardCode"]
            n = int(actual_id[1:])+1
            id = 'F' + str(n).zfill(LEN_BP_ID-1)
            return id



    def sync_bp(self):
        import requests
        self.__login()

        body = {
            "CardCode": self.supplier_data['sapcode'],
            "CardType": "cSupplier",
            "CardName" : self.supplier_data['ragsoc'],
            "FederalTaxID" : self.supplier_data['indirizzo']['stato'] + self.supplier_data['piva'],
            "AdditionalID" : self.supplier_data['cf'],
            "U_TG_ATECO" : self.supplier_data['cdateco'],
            "U_TG_REA" : self.supplier_data['rea'],
            #indirizzo di fatturazione
            "EDocStreet" : self.supplier_data['indirizzo']['via'],
            "EDocStreetNumber" : self.supplier_data['indirizzo']['civico'],
            "EDocZipCode" : self.supplier_data['indirizzo']['cap'],
            "EDocCity" : self.supplier_data['indirizzo']['citta'],
            "EDocCountry" : self.supplier_data['indirizzo']['stato'],
            "EDocDistrict" : self.supplier_data['indirizzo']['provincia'],
            "EDocPECAddress": self.supplier_data['pec'],
            #contatti
            "Phone1" : self.supplier_data['telefono'],
            "Fax" : self.supplier_data['fax'],
            "EmailAddress" : self.supplier_data['email'],
            "U_TG_GRUPPO_AZIENDA" : self.supplier_data['gruppo_azienda'],
            #banca
            # "BPBankAccounts" : [
            #     {
            #         "BankCode" : self.supplier_data['banca'][0]['codice'],
            #         "BPCode": self.id,
            #         "IBAN" :  self.supplier_data['banca'][0]['iban'],
            #         "AccountNo" :  self.supplier_data['banca'][0]['numconto'],
            #         "BICSwiftCode" :  self.supplier_data['banca'][0]['bic'],

            #     }
            # ]           
        }

        result = requests.post(self.root_url + SAP_BP,
                cookies=self.cookies,
                json = body,
                verify=False)
        self.__logout()
        if result.status_code not in accepted_status:
            Exception(f"Errore nella creazione del BP status code {result.status_code}")
        else: 
            return result.json()['CardCode']