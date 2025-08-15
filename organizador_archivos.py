import os
import argparse
from pathlib import Path

 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Organizador de archivos por categorías")
    parser.add_argument(
        "--carpeta", "-c",
        type=str,
        default="carpeta_prueba",
        help="Carpeta objetivo a organizar (por defecto: carpeta_prueba)"
    )
    parser.add_argument(
        "--sobrescribir", "-s",
        action="store_true",
        help="Sobrescribir archivos duplicados si existen"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular la operación sin mover archivos realmente"
    )
    return parser.parse_args()

# Obtener argumentos de línea de comandos
args = parse_arguments()

# Configurar carpeta objetivo
carpeta_objetivo = Path.cwd() / args.carpeta

categorias = {

    "Imagenes": [".png", ".jpg", ".jpeg", ".gif"],

    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],

    "Videos": [".mp4", ".avi", ".mkv"],

    "Musica": [".mp3", ".wav"],

}

categorias_predeterminadas = ["Otros"]  # donde irá lo que no encaje en las anteriores

extension_a_categoria = {}

for categoria, exts in categorias.items():

    for ext in exts:

        extension_a_categoria[ext.lower()] = categoria

archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()]

for archivo in archivos:

    ext = archivo.suffix.lower()

    categoria = extension_a_categoria.get(ext, "Otros")

    destino_dir = carpeta_objetivo / categoria

    destino_dir.mkdir(exist_ok=True)

    archivo_destino = destino_dir / archivo.name

    # Verificar si el archivo de destino ya existe
    if archivo_destino.exists() and not args.sobrescribir:
        print(f"⚠️  Saltando {archivo.name} - ya existe en {categoria}/")
        continue

    if args.dry_run:
        print(f"🔍 [DRY-RUN] Movería {archivo.name} a {categoria}/")
    else:
        try:
            if archivo_destino.exists() and args.sobrescribir:
                archivo_destino.unlink()  # Eliminar archivo existente
            archivo.rename(archivo_destino)
            print(f"✅ Movido {archivo.name} a {categoria}/")
        except Exception as e:
            print(f"❌ Error moviendo {archivo.name}: {e}")

# Mostrar resumen al final
if args.dry_run:
    print(f"\n🔍 Modo DRY-RUN completado. Revisa los cambios propuestos arriba.")
else:
    print(f"\n✅ Organización completada para la carpeta: {carpeta_objetivo}")

# Mostrar ayuda si no se especificaron argumentos
if len(os.sys.argv) == 1:
    print(f"\n💡 Usa --help para ver todas las opciones disponibles")
    print(f"   Ejemplo: python {os.path.basename(__file__)} --carpeta mi_carpeta --sobrescribir")