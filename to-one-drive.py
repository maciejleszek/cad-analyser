import ezdxf
import pandas as pd
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import os


def get_onedrive_path():
    """Automatycznie znajduje ścieżkę do folderu OneDrive na Windowsie."""
    # Próbuje znaleźć OneDrive biznesowy, potem prywatny
    path = os.environ.get('OneDriveCommercial') or os.environ.get('OneDrive')
    if not path:
        # Jeśli zmienne środowiskowe zawiodą, próbuje domyślnej ścieżki
        path = os.path.join(os.environ['USERPROFILE'], 'OneDrive')

    if not os.path.exists(path):
        print("BŁĄD: Nie można odnaleźć folderu OneDrive. Sprawdź, czy aplikacja jest zalogowana.")
        return None
    return path


def analyze_dxf(filename):
    """Analizuje geometrię pliku DXF."""
    try:
        doc = ezdxf.readfile(filename)
        msp = doc.modelspace()

        circles = msp.query('CIRCLE')

        # Tworzymy słownik z danymi
        stats = {
            "Nazwa_Pliku": os.path.basename(filename),
            "Liczba_Linii": len(msp.query('LINE')),
            "Liczba_Okregow": len(circles),
            "Liczba_Lukow": len(msp.query('ARC')),
            "Polilinie": len(msp.query('LWPOLYLINE')),
            "Opisy_Wymiary": len(msp.query('TEXT MTEXT DIMENSION')),
            "Srednia_Srednica": 0.0
        }

        if len(circles) > 0:
            avg_diam = (sum(c.dxf.radius for c in circles) / len(circles)) * 2
            stats["Srednia_Srednica"] = round(avg_diam, 2)

        return stats
    except Exception as e:
        print(f"Błąd podczas analizy DXF: {e}")
        return None


def save_to_excel_table(data_dict, output_path):
    """Zapisuje dane do Excela i formatuje je jako Tabelę dla Power Automate."""
    try:
        df = pd.DataFrame([data_dict])

        # Power Automate wymaga, aby dane były wewnątrz nazwanej Tabeli
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            sheet_name = 'DaneCAD'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            (max_row, max_col) = df.shape
            column_settings = [{'header': column} for column in df.columns]

            # Dodanie obiektu Tabeli (to kluczowe dla Power Automate!)
            worksheet.add_table(0, 0, max_row, max_col - 1, {
                'columns': column_settings,
                'name': 'TabelaWynikowa',
                'style': 'Table Style Medium 9'
            })
        print(f"--- Sukces: Dane zapisane w {output_path}")
    except Exception as e:
        print(f"Błąd zapisu Excel: {e}")


def create_pdf_preview(dxf_filename, pdf_path):
    """Tworzy wizualizację PDF rysunku CAD."""
    try:
        doc = ezdxf.readfile(dxf_filename)
        msp = doc.modelspace()
        ctx = RenderContext(doc)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_axes([0, 0, 1, 1])
        out = MatplotlibBackend(ax)
        frontend = Frontend(ctx, out)
        frontend.draw_layout(msp, finalize=True)
        fig.savefig(pdf_path, format='pdf', dpi=300)
        plt.close(fig)
        print(f"--- Sukces: PDF zapisany w {pdf_path}")
    except Exception as e:
        print(f"Błąd generowania PDF: {e}")


# --- URUCHOMIENIE ---
if __name__ == "__main__":
    # Twoja konkretna ścieżka (używamy 'r' przed cudzysłowem, aby uniknąć błędów ze slashami)
    target_folder = r"C:\Users\Maciej\OneDrive - Politechnika Warszawska\CAD analyzer"

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Utworzono folder: {target_folder}")

    input_dxf = "caddexpert_146.dxf"
    path_excel = os.path.join(target_folder, "raport.xlsx")
    path_pdf = os.path.join(target_folder, "wizualizacja.pdf")

    print(f"Rozpoczynam pracę...")

    dane = analyze_dxf(input_dxf)
    if dane:
        save_to_excel_table(dane, path_excel)
        create_pdf_preview(input_dxf, path_pdf)
        print("\n--- GOTOWE: Pliki są już w OneDrive ---")