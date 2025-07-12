#!/usr/bin/env python3
"""
Script simples para compilar traduções do projeto IGCV Raster Utility
Converte arquivos .ts para .qm usando lrelease (se disponível)
"""

import os
import sys
import subprocess
import shutil

def check_lrelease():
    """
    Verifica se o lrelease está disponível
    """
    return shutil.which('lrelease')

def compile_ts_to_qm(ts_file_path, qm_file_path):
    """
    Compila um arquivo .ts para .qm usando lrelease
    
    Args:
        ts_file_path (str): Caminho para o arquivo .ts
        qm_file_path (str): Caminho de saída para o arquivo .qm
    """
    try:
        # Executar lrelease
        result = subprocess.run([
            'lrelease', 
            ts_file_path, 
            '-qm', 
            qm_file_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Compilado: {ts_file_path} -> {qm_file_path}")
            return True
        else:
            print(f"✗ Erro ao compilar {ts_file_path}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Erro durante compilação: {e}")
        return False

def compile_all_translations():
    """
    Compila todos os arquivos .ts na pasta translations/
    """
    translations_dir = "translations"
    
    if not os.path.exists(translations_dir):
        print(f"✗ Diretório {translations_dir} não encontrado")
        return False
    
    # Encontrar todos os arquivos .ts
    ts_files = [f for f in os.listdir(translations_dir) if f.endswith('.ts')]
    
    if not ts_files:
        print(f"✗ Nenhum arquivo .ts encontrado em {translations_dir}")
        return False
    
    print(f"Encontrados {len(ts_files)} arquivo(s) .ts para compilar:")
    
    success_count = 0
    for ts_file in ts_files:
        ts_path = os.path.join(translations_dir, ts_file)
        qm_file = ts_file.replace('.ts', '.qm')
        qm_path = os.path.join(translations_dir, qm_file)
        
        if compile_ts_to_qm(ts_path, qm_path):
            success_count += 1
    
    print(f"\nResumo: {success_count}/{len(ts_files)} arquivos compilados com sucesso")
    return success_count == len(ts_files)

def main():
    """
    Função principal
    """
    print("=== Compilador de Traduções IGCV Raster Utility ===\n")
    
    # Verificar se lrelease está disponível
    if not check_lrelease():
        print("✗ lrelease não encontrado no sistema.")
        print("\nPara compilar traduções, você precisa instalar as ferramentas Qt:")
        print("  Arch Linux: sudo pacman -S qt5-tools")
        print("  Ubuntu/Debian: sudo apt-get install qttools5-dev-tools")
        print("  macOS: brew install qt5")
        print("\nAlternativamente, você pode:")
        print("  1. Instalar o Qt Creator que inclui lrelease")
        print("  2. Baixar as ferramentas Qt do site oficial")
        sys.exit(1)
    
    if compile_all_translations():
        print("\n✓ Todas as traduções foram compiladas com sucesso!")
        print("Os arquivos .qm estão prontos para uso na aplicação.")
    else:
        print("\n✗ Algumas traduções falharam na compilação.")
        sys.exit(1)

if __name__ == "__main__":
    main() 