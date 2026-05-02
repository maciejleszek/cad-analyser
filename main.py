import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt


def convert_dxf_to_pdf(dxf_filename, pdf_filename):
    try:
        # Wczytanie pliku DXF
        doc = ezdxf.readfile(dxf_filename)
        msp = doc.modelspace()

        # Konfiguracja renderowania
        ctx = RenderContext(doc)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_axes([0, 0, 1, 1])

        # Backend Matplotlib do rysowania
        out = MatplotlibBackend(ax)
        frontend = Frontend(ctx, out)

        # Wygenerowanie rysunku
        frontend.draw_layout(msp, finalize=True)

        # Zapis do PDF
        fig.savefig(pdf_filename, format='pdf', dpi=300)
        plt.close(fig)

        print(f"--- SUKCES ---")
        print(f"Wygenerowano wizualizację: {pdf_filename}")

    except Exception as e:
        print(f"Błąd konwersji na PDF: {e}")


def count_and_analyze(filename):
    try:
        doc = ezdxf.readfile(filename)
        lines = doc.modelspace().query('LINE')

        print(f"--- ANALIZA GEOMETRII ---")
        print(f"Plik: {filename}")
        print(f"Znaleziono krawędzi (LINE): {len(lines)}")

    except Exception as e:
        print(f"Błąd analizy: {e}")


if __name__ == "__main__":
    # Nazwy plików
    input_file = "bridge.dxf"
    output_pdf = "bridge_output.pdf"

    # Uruchomienie funkcji
    count_and_analyze(input_file)
    convert_dxf_to_pdf(input_file, output_pdf)