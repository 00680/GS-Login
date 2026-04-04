import os
import psutil

class GersangUtils:
    @staticmethod
    def isGersangRunning(folder: str) -> bool | None:
        if not folder:
            return False

        try:
            folderNorm = os.path.normcase(os.path.abspath(folder))
        except Exception:
            folderNorm = (folder or '').lower()

        for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
            try:
                name = (proc.info.get('name') or '').lower()
                exe = (proc.info.get('exe') or '') or ''
                exeNorm = exe and os.path.normcase(exe) or ''
                if 'gersang.exe' in name:
                    if exeNorm and exeNorm.startswith(folderNorm):
                        return True

                    cmd = proc.info.get('cmdline') or []
                    for part in cmd:
                        try:
                            if isinstance(part, str):
                                partNorm = os.path.normcase(os.path.abspath(part)) if os.path.exists(part) else part.lower()
                                if partNorm.startswith(folderNorm) and partNorm.endswith('gersang.exe'):
                                    return True
                        except Exception:
                            continue
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return False
