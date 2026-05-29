from utils.query import QUERY_PRESENTACIONES
from datetime import datetime
from lib_resources.sql import DBManager
import json, os
db = DBManager()

def db_fas(page):
    try:
        page.reload()
        page.set_default_timeout(510000)
        page.goto("https://fas.crp.com.pe/os/dbstudio#/tabs/studio%2Fprimary%2FDatabases%2Fcrp_ifas%2FSQL")
        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > div:nth-child(27) > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.click("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > div:nth-child(27) > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.get_by_text("1000000").click()
        selector_editor = "#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(1) > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text"
        page.click(selector_editor)
        query_final = QUERY_PRESENTACIONES
        page.locator(selector_editor).click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(query_final)
        page.wait_for_selector("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")
        page.click("#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > header > div > div:nth-child(1) > button:nth-child(4) > span > i")
        
        selector_exportar = "#dbstudio-main-content > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div > div > div:nth-child(3) > div > div:nth-child(2) > div > header > div > div.v-toolbar__items > button.dbstudio-extra-small-button.mt-0.v-btn.v-btn--icon.v-btn--round.v-btn--text.theme--light.v-size--small.green--text > span > i"
        print("⏳ Query en ejecución... esperando icono de exportación (~1.5 min)")
        
        page.wait_for_selector(selector_exportar, state="visible", timeout=500000)
        page.click(selector_exportar)   

        page.wait_for_selector("#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.pb-0 > div > div.v-stepper__items > div:nth-child(1) > div > form > div > div > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > div > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.click("#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.pb-0 > div > div.v-stepper__items > div:nth-child(1) > div > form > div > div > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > div > div > div > div.v-select__slot > div.v-input__append-inner > div > i")
        page.get_by_text("Excel 2007 OOXML (.xlsx)", exact=True).click()   

        page.wait_for_selector("#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.px-6 > button:nth-child(4) > span")
        page.click("#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.px-6 > button:nth-child(4) > span")
    
        #selector2 = "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.px-6 > button:nth-child(4) > span"
        #page.wait_for_selector(selector_exportar, state="visible", timeout=500000)
        #page.click(selector2)
        
        #CORRECCION
        #selectorPrevious = "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.px-6 > button:nth-child(3) > span"
        #page.wait_for_selector(selectorPrevious, state = "visible", timeout = 500000)
        #page.click(selectorPrevious)
    
        page.wait_for_selector("#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.px-6 > button.rounded-lg.primary.text-none.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default > span")

        fecha_hoy = datetime.now().strftime("%d-%m-%Y")
        ruta_final = fr"\\10.7.2.14\Reportes Axional\FACT.PLANSALUD-IMFORMACIÓN - PLS\PrestacionesSinIntegrar"

        with page.expect_download() as download_info:
            page.locator("button:has-text('Finish')").click() 

        download = download_info.value

        nuevo_nombre = f"PresyProdSinCuenta_EpisodiosFinalizado_al_{fecha_hoy}.xls"
        ruta_completa_archivo = os.path.join(ruta_final, nuevo_nombre)

        download.save_as(ruta_completa_archivo)
        size = os.path.getsize(ruta_completa_archivo)
        print(f"Descarga finalizada en: {ruta_completa_archivo}")
        anio = datetime.now().year
        db.registrar_log("PRESENTACIONES", "DESCARGAR PRESENTACIONES", "EXITO", f"{anio}", f"{size}")
        with open("logs/logs_presentaciones.txt", "a") as f:
            f.write(f"{datetime.now()} : Descargo y guardo PRESENTACIONES Tamaño: {size} bytes Correctamente\n")
        return True
    except Exception as e:
        db.registrar_log("PRESENTACIONES", "DESCARGAR PRESENTACIONES", "ERROR", f"{anio}", f"{size}", f"{e}")
        with open("logs/logs_presentaciones.txt", "a") as f:
            f.write(f"{datetime.now()} : ERROR al descargar y guardar PRESENTACIONES\nConsola : {e}")
        return False

def login(page):
    try:
        with open("credentials/credentials_fas.json","r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        usuario = datos["usuario"]
        contrasena = datos["contrasena"]
        page.wait_for_selector("#input-11")
        page.wait_for_selector("#input-12")
        page.fill("#input-11", usuario)
        page.fill("#input-12", contrasena)
        page.wait_for_selector("#app > div > main > div > div > div > div.d-flex.col-md-6.col-lg-5.col-12 > div > div.v-card__text.pa-0 > form > button > span")
        page.click("#app > div > main > div > div > div > div.d-flex.col-md-6.col-lg-5.col-12 > div > div.v-card__text.pa-0 > form > button > span")
        with open("logs/logs_presentaciones.txt", "a") as f:
            f.write(f"{datetime.now()} : Login Exitoso\n")
        return True
    except Exception as e:
        with open("logs/logs_presentaciones.txt", "a") as f:
            f.write(f"{datetime.now()} : ERROR en el proceso del Login\nConsola : {e}")
        return False

def proceso(page):
    try:
        verifLogin = login(page)

        if not verifLogin:
            print("Error: Login Fallo, Cerrando aplicativo")
            return
        print("\nExito: Login Existoso") 
        
        verifDb_fas = db_fas(page)
        if not verifDb_fas:
            print("Error: funcion db_fas Fallo, Cerrando aplicativo")
            with open("logs/logs_presentaciones.txt", "a") as f:
                f.write(f"{datetime.now()} : ERROR: funcion db_fas Fallo, Cerrando aplicativo\nConsola : {e}")
            return
        
        if verifDb_fas:
            print("PROCESO TERMINADO CORRECTAMENTE, CERRANDO APLICATIVO...")
            with open("logs/logs_presentaciones.txt", "a") as f:
                f.write(f"{datetime.now()} : PROCESO TERMINADO CORRECTAMENTE\n")
        return True
    except Exception as e:
        return False