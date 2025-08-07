import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = Service(r'C:\Users\Pc\Downloads\chromedriver-win64\chromedriver.exe')
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)  

    def capturar_screenshot(self, nombre):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.driver.save_screenshot(f"screenshots/{nombre}_{timestamp}.png")


    def test_01_login_campos_vacios(self):
        self.driver.get("http://localhost:5000/login")
        time.sleep(0.3)
        self.driver.find_element(By.ID, "usuario").clear()
        self.driver.find_element(By.ID, "usuario").send_keys(" ")
        time.sleep(2)
        self.driver.find_element(By.ID, "clave").clear()
        self.driver.find_element(By.ID, "clave").send_keys(" ")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
        self.assertTrue(alert.is_displayed())
        time.sleep(4)
        self.capturar_screenshot("login_vacio")

    def test_02_login_fallido(self):
        self.driver.get("http://localhost:5000/login")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "usuario").clear()
        self.driver.find_element(By.ID, "usuario").send_keys("admin")
        time.sleep(2)
        self.driver.find_element(By.ID, "clave").clear()
        self.driver.find_element(By.ID, "clave").send_keys("claveincorrecta")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
        self.assertTrue(alert.is_displayed())
        time.sleep(4)
        self.capturar_screenshot("login_fallido")

    def test_03_login_exitoso(self):
        self.driver.get("http://localhost:5000/login")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "usuario").clear()
        self.driver.find_element(By.ID, "usuario").send_keys("admin")
        time.sleep(2)
        self.driver.find_element(By.ID, "clave").clear()
        self.driver.find_element(By.ID, "clave").send_keys("markethub123")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        self.wait.until(EC.url_contains("dashboard"))
        self.assertIn("dashboard", self.driver.current_url)
        time.sleep(4)
        self.capturar_screenshot("login_exitoso")

    def test_04_dashboard_muestra_productos(self):
        self.driver.get("http://localhost:5000/dashboard")
        time.sleep(3)
        tabla = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        self.assertTrue(tabla.is_displayed())

        filas = tabla.find_elements(By.TAG_NAME, "tr")
        self.assertGreater(len(filas), 1)

        primera_fila = filas[1]
        celdas = primera_fila.find_elements(By.TAG_NAME, "td")
        self.assertTrue(len(celdas) > 0)
        self.assertTrue(len(celdas[1].text) > 0)
        self.capturar_screenshot("listar_productos")

    def test_05_agregar_producto_nombre_largo(self):
        self.driver.get("http://localhost:5000/agregar")
        time.sleep(0.5)
        nombre_largo = "P" * 101
        self.driver.find_element(By.ID, "nombre").clear()
        self.driver.find_element(By.ID, "nombre").send_keys(nombre_largo)
        time.sleep(2)

        self.driver.find_element(By.ID, "precio").clear()
        self.driver.find_element(By.ID, "precio").send_keys("20.00")
        time.sleep(2)

        self.driver.find_element(By.ID, "cantidad").clear()
        self.driver.find_element(By.ID, "cantidad").send_keys("8")
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("El nombre del producto no puede tener más de 100 caracteres", alert.text)
        time.sleep(4)
        self.capturar_screenshot("agregar_producto_nombre_largo")

    def test_06_agregar_producto_exitoso(self):  
        self.driver.get("http://localhost:5000/agregar")
        time.sleep(0.5)

        self.driver.find_element(By.ID, "nombre").clear()
        self.driver.find_element(By.ID, "nombre").send_keys("ProductoTestUnico")
        time.sleep(2)

        self.driver.find_element(By.ID, "precio").clear()
        self.driver.find_element(By.ID, "precio").send_keys("25.50")
        time.sleep(2)

        self.driver.find_element(By.ID, "cantidad").clear()
        self.driver.find_element(By.ID, "cantidad").send_keys("10")
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-success")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("Producto agregado correctamente", alert.text)
        time.sleep(4)
        self.capturar_screenshot("agregar_producto_exitoso")

    def test_07_agregar_producto_existente(self):  
        self.driver.get("http://localhost:5000/agregar")
        time.sleep(0.5)

        self.driver.find_element(By.ID, "nombre").clear()
        self.driver.find_element(By.ID, "nombre").send_keys("ProductoTestUnico")
        time.sleep(2)

        self.driver.find_element(By.ID, "precio").clear()
        self.driver.find_element(By.ID, "precio").send_keys("30.00")
        time.sleep(2)

        self.driver.find_element(By.ID, "cantidad").clear()
        self.driver.find_element(By.ID, "cantidad").send_keys("5")
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("Ya existe un producto con ese nombre", alert.text)
        time.sleep(4)
        self.capturar_screenshot("agregar_producto_existente")

    def test_08_editar_producto_exitosamente(self):
        self.driver.get("http://localhost:5000/dashboard")
        time.sleep(1)

        filas = self.driver.find_elements(By.TAG_NAME, "tr")
        for fila in filas:
            if "ProductoTestUnico" in fila.text:
                editar_btn = fila.find_element(By.LINK_TEXT, "Editar")
                editar_btn.click()
                break

        self.wait.until(EC.url_contains("/editar"))
        nombre_input = self.driver.find_element(By.ID, "nombre")
        nombre_input.clear()
        nombre_input.send_keys("ProductoTestEditado")
        time.sleep(2)

        precio_input = self.driver.find_element(By.ID, "precio")
        precio_input.clear()
        precio_input.send_keys("99.99")
        time.sleep(2)

        cantidad_input = self.driver.find_element(By.ID, "cantidad")
        cantidad_input.clear()
        cantidad_input.send_keys("50")
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-success")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("Producto actualizado correctamente", alert.text)
        time.sleep(4)
        self.capturar_screenshot("actualizar_producto_exitoso")

    def test_09_editar_producto_nombre_largo(self):
        self.driver.get("http://localhost:5000/dashboard")
        time.sleep(1)

        filas = self.driver.find_elements(By.TAG_NAME, "tr")
        for fila in filas:
            if "ProductoTestEditado" in fila.text:
               fila.find_element(By.LINK_TEXT, "Editar").click()
               break

        self.wait.until(EC.url_contains("/editar"))

        nombre_largo = "N" * 101
        nombre_input = self.driver.find_element(By.ID, "nombre")
        nombre_input.clear()
        nombre_input.send_keys(nombre_largo)
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("El nombre del producto no puede tener más de 100 caracteres", alert.text)
        time.sleep(4)
        self.capturar_screenshot("actualizar_producto_nombre_largo")

    def test_10_eliminar_producto_cancelar(self):
        self.driver.get("http://localhost:5000/dashboard")
        time.sleep(1)

        producto_encontrado = False
        for fila in self.driver.find_elements(By.TAG_NAME, "tr"):
            if "ProductoTestEditado" in fila.text:
                fila.find_element(By.LINK_TEXT, "Eliminar").click()
                producto_encontrado = True
                break

        self.assertTrue(producto_encontrado, "ProductoTestEditado no encontrado en la tabla")
        self.wait.until(EC.url_contains("/eliminar"))
        time.sleep(7)

        boton_cancelar = self.driver.find_element(By.CSS_SELECTOR, "button[name='confirmar'][value='no']")
        boton_cancelar.click()
        time.sleep(4)

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-info")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("Eliminación cancelada", alert.text)
        time.sleep(3)
        self.capturar_screenshot("eliminacion_cancelada")

    def test_11_eliminar_producto_confirmar(self):
        self.driver.get("http://localhost:5000/dashboard")
        time.sleep(1)

        producto_encontrado = False
        filas = self.driver.find_elements(By.TAG_NAME, "tr")
        for fila in filas:
            if "ProductoTestEditado" in fila.text:
                fila.find_element(By.LINK_TEXT, "Eliminar").click()
                producto_encontrado = True
                break

        self.assertTrue(producto_encontrado, "ProductoTestEditado no encontrado en la tabla")
        self.wait.until(EC.url_contains("/eliminar"))
        time.sleep(7)

        boton_confirmar = self.driver.find_element(By.CSS_SELECTOR, "button[name='confirmar'][value='si']")
        boton_confirmar.click()

        alert = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-success")))
        self.assertTrue(alert.is_displayed())
        self.assertIn("Producto eliminado correctamente", alert.text)
        time.sleep(5)
        self.capturar_screenshot("eliminacion_confirmada")

    def test_12_logout(self):
        self.wait.until(EC.url_contains("dashboard"))
        self.assertIn("dashboard", self.driver.current_url)

        self.driver.get("http://localhost:5000/logout")

        self.wait.until(EC.url_contains("login"))
        self.assertIn("login", self.driver.current_url)
        time.sleep(5)
        self.capturar_screenshot("logout")

if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output='reportes_html',
            report_title='Reporte de Pruebas - Market Hub',
            report_name='reporte_markethub',
            combine_reports=True
        )
    )