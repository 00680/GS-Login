from config.ConfigLoader import Config
from utils.AccountsNotifier import AccountsNotifier


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
        # Validate required fields
        username = accountData.get('username')
        password = accountData.get('password')
        otp = accountData.get('otp')
        missing = []
        if not username:
            missing.append('username')
        if not password:
            missing.append('password')
        if not otp:
            missing.append('otp')
        if missing:
            raise ValueError(f"Missing required account fields: {', '.join(missing)}")
        accounts[accountId] = accountData
        Config.cfg['accounts'] = accounts
        Config.save()
        try:
            AccountsNotifier.instance().accountsChanged.emit()
        except Exception:
            pass

    @staticmethod
    def deleteAccount(accountId):
        accounts = AccountsConfigManager.getAccounts()
        if accountId in accounts:
            del accounts[accountId]
            Config.cfg['accounts'] = accounts
            Config.save()
            try:
                AccountsNotifier.instance().accountsChanged.emit()
            except Exception:
                pass