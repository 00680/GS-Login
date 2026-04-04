from config.ConfigLoader import Config


class AccountsConfigManager:
    @staticmethod
    def getAccounts():
        return Config.get('accounts', {})

    @staticmethod
    def getAccountById(accountId):
        accounts = AccountsConfigManager.getAccounts()
        return accounts.get(accountId)
    
    @staticmethod
    def addOrUpdateAccount(accountData):
        accounts = AccountsConfigManager.getAccounts()
        accountId = accountData.get('id')
        if not accountId:
            raise ValueError("Account data must contain an 'id' field.")
        accounts[accountId] = accountData
        Config.cfg['accounts'] = accounts
        Config.save()