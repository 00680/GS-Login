import threading
import time
import traceback
import requests
import base64
import hmac
import hashlib
import struct
import os
import subprocess

# Lazy-import heavy playwright modules at runtime to avoid slowing
# application startup when this module is merely imported by the UI.
from utils.AccountsConfigManager import AccountsConfigManager
from utils.ProcessesConfigManager import ProcessesConfigManager
from utils.SettingsConfigManager import SettingsConfigManager


class AutoLogin:
    DEFAULT_USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    )

    DEFAULT_FIREFOX_PREFS = {
        'dom.min_background_timeout_value': 0,
        'dom.timeout.background_throttling': False,
        'dom.ipc.processPriorityManager.enabled': False,
        'widget.windows.window_occlusion_tracking.enabled': False,
    }

    def __init__(self, process_id: str, account_id: str, headless: bool = False, firefox_prefs: dict | None = None, keep_open_seconds: float = 5.0):
        self.process_id = process_id
        self.account_id = account_id
        self.headless = headless
        self.firefox_prefs = firefox_prefs or dict(self.DEFAULT_FIREFOX_PREFS)
        self.keep_open_seconds = float(keep_open_seconds)
        self._thread: threading.Thread | None = None

    def loginTW(self, page, account: dict):
        username = account.get('username', '')
        password = account.get('password', '')
        otp = account.get('otp', '')
        try:
            page.goto("https://www.mangot5.com/Index/Member/Login?gname=gs&ref=/gs/index?MODE=LIVE", timeout=30000)
            page.wait_for_selector('#oldPassword', timeout=20000)

            page.fill('#oldPassword', username)
            page.fill('#newPassword', password)

            captchaResolved = self.solveRecaptcha(page)
            if captchaResolved is False:
                return False

            page.click('#submitBtn')

            try:
                page.wait_for_selector('#optForm > div:nth-child(1) > div', timeout=20000)
            except TimeoutError:
                return False

            try:
                code = self.resolveOtp(otp)
            except Exception:
                return False

            page.fill('#validCode', str(code))
            
            page.click('#optForm > div:nth-child(3) > div > button')

            try:
                page.wait_for_selector('#wrapper > div.login_box > div.login_top > a', timeout=20000)
            except TimeoutError:
                return False
            
            try:
                jsession = None
                cookies = page.context.cookies()
                for c in cookies:
                    if c.get('name') == 'JSESSIONID':
                        jsession = c.get('value')
                        break
                user_no = page.locator('[name=userNo]').get_attribute('value')
            except Exception as e:
                return False

            try:
                ua = self.DEFAULT_USER_AGENT
                headers = {'User-Agent': ua}
                cookies = {'JSESSIONID': jsession} if jsession else {}
                resp = requests.post('https://gs.mangot5.com/game/gs/getAuthKey.json', data={'userNo': user_no}, headers=headers, cookies=cookies, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                authKey = data.get('authKey') or data.get('data', {}).get('authKey')
            except Exception as e:
                return False

            # launch run.exe if requested (no log output here); store Popen on self for monitoring
            try:
                if self.process_id and authKey and user_no:
                    run_path = os.path.join(self.process_id, 'run.exe')
                    if os.path.exists(run_path):
                        proc = subprocess.Popen([run_path, str(user_no), str(authKey)])
                        try:
                            self._last_run_proc = proc
                            self._last_run_path = run_path
                        except Exception:
                            return False
            except Exception:
                return False

            return True
        except Exception:
            return False

    def performLogin(self):
        acct = AccountsConfigManager.getAccountById(self.account_id) if self.account_id else None

        try:
            # import here to avoid importing Playwright during application
            # module import time (which is expensive and slows exe startup)
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                import tempfile
                profile_dir = tempfile.mkdtemp(prefix='gslogin_firefox_')
                context = p.firefox.launch_persistent_context(
                    user_data_dir=profile_dir,
                    headless=self.headless,
                    firefox_user_prefs=self.firefox_prefs,
                )
                # reuse the initial page created by the persistent context
                pages = context.pages
                if pages:
                    page = pages[0]
                else:
                    page = context.new_page()

                ok = self.loginTW(page, acct)

                time.sleep(self.keep_open_seconds)
                try:
                    context.close()
                except Exception:
                    pass
        except Exception:
            traceback.print_exc()

    def solveRecaptcha(self, page):
        capsolver_key = SettingsConfigManager.getCapSolverApiKey()

        if not capsolver_key:
            return False
        
        try:
            # playwright-recaptcha is optional and can be slow to import; import lazily
            from playwright_recaptcha import recaptchav2

            solver = recaptchav2.SyncSolver(page, capsolver_api_key=capsolver_key)
            res = solver.solve_recaptcha(wait=True, image_challenge=True)
            
            token = None
            if isinstance(res, str):
                token = res
            elif isinstance(res, dict):
                token = res.get('gRecaptchaResponse') or res.get('token') or res.get('response')
            
            if token:
                return token
        except Exception:
            pass

        return False

    def start(self) -> threading.Thread:
        if self._thread and self._thread.is_alive():
            return self._thread
        self._thread = threading.Thread(target=self.performLogin, daemon=True)
        self._thread.start()
        return self._thread

    def resolveOtp(self, secret, digits=6, interval=30):
        key = secret.replace(' ', '').upper()
        key_bytes = base64.b32decode(key)
        t = int(time.time() / interval)
        msg = struct.pack('>Q', t)
        h = hmac.new(key_bytes, msg, hashlib.sha1).digest()
        o = h[19] & 15
        code = (struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff) % (10 ** digits)
        return str(code).zfill(digits)
    
def startLogin(processId, accountId, **kwargs):
    runner = AutoLogin(processId, accountId, **kwargs)
    return runner.start()
