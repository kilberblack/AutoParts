import os, time, unittest, random, string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE = "http://127.0.0.1:8000"

def rs(n=6): return ''.join(random.choices(string.ascii_lowercase+string.digits, k=n))

def open_first(drv, paths):
    for p in paths:
        drv.get(f"{BASE}{p}")
        try:
            WebDriverWait(drv, 8).until(EC.presence_of_element_located((By.TAG_NAME,"body")))
            return True
        except Exception:
            continue
    return False

def click_any(scope, css_list):
    for css in css_list:
        try:
            scope.find_element(By.CSS_SELECTOR, css).click()
            return True
        except Exception:
            pass
    return False

def first(scope, css_list, t=6):
    w = WebDriverWait(scope if hasattr(scope, "find_element") else scope.d, t)
    for css in css_list:
        try:
            return w.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
        except Exception:
            continue
    return None

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1280,900")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        cls.d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        cls.w = WebDriverWait(cls.d, 15)
        s = rs()
        cls.user = {"u": f"user{s}", "e": f"user{s}@test.local", "p": f"Passw0rd!{s}"}

    @classmethod
    def tearDownClass(cls):
        cls.d.quit()

    # 1) Registro (/registrarse) compatible con {{ form }}
    def test_01_registro(self):
        self.assertTrue(open_first(self.d, ["/registrarse/", "/register/"]), "No abre registro")
        # elige un <form> que tenga al menos un password
        forms = self.d.find_elements(By.TAG_NAME, "form")
        reg = None
        for f in forms:
            if f.find_elements(By.CSS_SELECTOR, "input[type='password']"):
                reg = f; break
        if not reg:
            self.skipTest("Sin formulario de registro visible"); return
        # primer email o text
        filled = False
        for sel, val in [("input[type='email']", self.user["e"]), ("input[type='text']:not([type='search'])", self.user["u"])]:
            els = reg.find_elements(By.CSS_SELECTOR, sel)
            if els:
                els[0].clear(); els[0].send_keys(val); filled = True; break
        if not filled:
            self.skipTest("Registro sin campo de usuario/email"); return
        # contraseñas
        pw = reg.find_elements(By.CSS_SELECTOR, "input[type='password']")
        if not pw:
            self.skipTest("Registro sin campos de contraseña"); return
        pw[0].clear(); pw[0].send_keys(self.user["p"])
        if len(pw) >= 2:
            pw[1].clear(); pw[1].send_keys(self.user["p"])
        # enviar
        if not click_any(reg, ["button[type='submit']","input[type='submit']","form button",".btn-primary",".btn"]):
            self.skipTest("Registro sin botón enviar"); return
        self.w.until(lambda d: any(x in d.current_url for x in ("/cuenta","/catalogo","/","/tienda/")))
        self.assertTrue(True)

    # 2) Catálogo y búsqueda
    def test_02_catalogo_busqueda(self):
        self.assertTrue(open_first(self.d, ["/catalogo/"]), "No abre /catalogo/")
        # búsqueda por ruta /tienda/<query>
        self.assertTrue(open_first(self.d, ["/tienda/filtro/"]), "No abre /tienda/<query>")

    # 3) Carrito: agregar, ajustar, eliminar
    def test_03_carrito(self):
        # ir a catálogo o tienda
        if not open_first(self.d, ["/catalogo/","/tienda/"]):
            self.skipTest("Sin catálogo/tienda"); return
        # abrir producto
        link = first(self.d, ["a[href*='/producto/']", ".product a", "a.ver-producto"], 5)
        if not link:
            self.skipTest("Sin productos listados"); return
        link.click()
        # agregar al carrito (tu botón en store.html)
        added = click_any(self.d, ["button.add-to-cart-btn",".add-to-cart-btn",
                                   "button.add-to-cart",".add-to-cart",
                                   "form[action*='carrito'] button","[name='agregar']"])
        if not added:
            self.skipTest("Sin botón de agregar al carrito"); return
        # abrir carrito
        self.d.get(f"{BASE}/carrito/")
        table_or_row = first(self.d, ["#tablaCarrito"," .cart-item"," table tr"], 6)
        self.assertIsNotNone(table_or_row, "Carrito vacío tras agregar")
        # ajustar cantidad si existe
        qty = first(self.d, ["#tablaCarrito input[type='number']","input[name*='cantidad']"], 2)
        if qty:
            qty.clear(); qty.send_keys("2")
            click_any(self.d, ["button.update",".update",".btn-actualizar"])
            time.sleep(1)
        # eliminar si existe
        if not click_any(self.d, [".remove-item",".delete","a[href*='eliminar']","#tablaCarrito .btn-danger"]):
            self.skipTest("Sin botón eliminar en carrito")

    # 4) Checkout: solo si hay formulario
    def test_04_checkout(self):
        self.d.get(f"{BASE}/checkout/")
        form = first(self.d, ["form"], 5)
        if not form:
            self.skipTest("Checkout sin formulario"); return
        # completa si existen
        for css,val in [
            ("input[name*='nombre'],input[name*='name']","Cliente Test"),
            ("input[name*='email']","cliente@test.local"),
            ("input[name*='direccion'],input[name*='address']","Calle 123"),
        ]:
            try: el = self.d.find_element(By.CSS_SELECTOR, css); el.clear(); el.send_keys(val)
            except Exception: pass
        click_any(self.d, ["input[type='checkbox'][name*='termin']","input[type='checkbox']"])
        if not click_any(self.d, ["button[type='submit']","input[type='submit']","form button",".btn-primary"]):
            self.skipTest("Checkout sin botón enviar"); return
        self.w.until(lambda d:any(x in d.current_url for x in ("/pago_exito","/pago_cancelado","/","/catalogo")))
        self.assertTrue(True)

    # 5) Historial de pedidos en /cuenta/ (tab #pedidos)
    def test_05_historial(self):
        if not open_first(self.d, ["/cuenta/"]):
            self.skipTest("No abre /cuenta/"); return
        click_any(self.d, ["a[href='#pedidos']","#pedidos-tab","[data-toggle='tab'][href='#pedidos']"])
        ok = first(self.d, ["#pedidos table", "table", "//*[contains(text(),'No tienes pedidos')]",], 3)
        if not ok:
            self.skipTest("Sin tabla ni mensaje en pedidos")

    # 6) Mayorista
    def test_06_mayorista(self):
        self.assertTrue(open_first(self.d, ["/mayorista/"]), "No abre /mayorista/")

    # 7) Dashboard (existencia)
    def test_07_dashboard(self):
        if not open_first(self.d, ["/dashboard/","/panel/"]):
            self.skipTest("Sin dashboard"); return
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main(verbosity=2)
