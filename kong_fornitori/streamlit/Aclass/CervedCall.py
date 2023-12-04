from IPython import embed
class CervedCall():    
    def __init__(self, piva: str, apival: str):
            self.piva = piva
            self.headers = {"apikey": apival}
            self.root_url = "https://api.cerved.com/cervedApi/"

    def __getidsoggetto(self):  
        import requests        
        ROOT = f"{self.root_url}v1/entitySearch/live?testoricerca={self.piva}"
        
        res_anagrafica = requests.get(ROOT, headers=self.headers).json()       
        id_soggetto = res_anagrafica["companies"][0]["dati_anagrafici"]["id_soggetto"]
        self.id = id_soggetto

    def __getbalancey(self):
        import requests 
        self.__getidsoggetto()
        ROOT_BAL_CH = f"{self.root_url}v1/entityProfile/balancesheetslist?id_soggetto={self.id}"
        res_chbilanci = requests.get(ROOT_BAL_CH, headers=self.headers).json()
        chbilanci = res_chbilanci["bilanci"]
        self.bilist = chbilanci

    def get_bilanci(self):
        import requests 
        self.__getbalancey()
        finalJ = {}
        for balance in self.bilist:
            chiusura = balance["data_chiusura"]
            tipo = balance["tipo_bilancio"]
            ROOT_BALANCE = f"{self.root_url}v1/entityProfile/balancesheet?id_soggetto={self.id}&data_chiusura={chiusura}&tipo_bilancio={tipo}"
            res_bilancio = requests.get(ROOT_BALANCE, headers=self.headers).json()   
            anno = chiusura[-4:]
            finalJ[anno] = res_bilancio
        return finalJ
    
    def get_negflag(self):
        import requests
        self.__getidsoggetto()
        ROOT_BALANCE = f"{self.root_url}v1.1/rischi/negative/events/flags/ALL?subjectId={self.id}"
        res_negflags = requests.get(ROOT_BALANCE, headers=self.headers).json()
        return res_negflags["companies"]

    def get_negevents(self):
        import requests
        self.__getidsoggetto()
        ROOT_BALANCE = f"{self.root_url}v1/risks/negative/events?subject_id={self.id}"
        res_negevent = requests.get(ROOT_BALANCE, headers=self.headers).json()
        return res_negevent["companies"]
       
    