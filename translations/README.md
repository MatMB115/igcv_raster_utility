# Traduções - IGCV Raster Utility

Este diretório contém os arquivos de tradução do projeto.

## Arquivos

- `igcv_en.ts` - Traduções em inglês (arquivo fonte)
- `igcv_pt_BR.ts` - Traduções em português brasileiro (arquivo fonte)

## Como compilar as traduções

As traduções precisam ser compiladas de arquivos `.ts` (Translation Source) para arquivos `.qm` (Qt Message) para funcionar na aplicação.

### Opção 1: Usando o script Python (Recomendado)

Execute o script de compilação:

```bash
python compile_translations_simple.py
```

### Opção 2: Instalando ferramentas Qt manualmente

#### Arch Linux
```bash
sudo pacman -S qt5-tools
```

#### Ubuntu/Debian
```bash
sudo apt-get install qttools5-dev-tools
```

#### macOS
```bash
brew install qt5
```

Depois execute:
```bash
lrelease translations/*.ts
```

### Opção 3: Usando Qt Creator

1. Abra o Qt Creator
2. Vá em Tools > External > Linguist > Release
3. Selecione os arquivos `.ts` e compile

## Estrutura dos arquivos .ts

Os arquivos `.ts` contêm:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1">
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../view/main_window.py" line="11"/>
        <source>IGCV Raster Tool - MVP</source>
        <translation type="unfinished"></translation>
    </message>
    <!-- Mais mensagens... -->
</context>
</TS>
```

## Como adicionar novas traduções

1. **Adicionar texto na interface**: Use `self.tr("Texto")` no código Python
2. **Atualizar arquivos .ts**: Execute `pylupdate5` para extrair novos textos
3. **Traduzir**: Edite os arquivos `.ts` adicionando as traduções
4. **Compilar**: Execute o script de compilação

### Exemplo de atualização dos arquivos .ts

```bash
pylupdate5 view/main_window.py -ts translations/igcv_en.ts
pylupdate5 view/main_window.py -ts translations/igcv_pt_BR.ts
```

## Arquivos gerados

Após a compilação, serão criados:

- `igcv_en.qm` - Traduções compiladas em inglês
- `igcv_pt_BR.qm` - Traduções compiladas em português

## Notas importantes

- Os arquivos `.qm` são binários e não devem ser editados manualmente
- Sempre edite os arquivos `.ts` para fazer alterações nas traduções
- Execute a compilação sempre que alterar os arquivos `.ts`
- Os arquivos `.qm` são carregados automaticamente pela aplicação

## Solução de problemas

### "lrelease não encontrado"
Instale as ferramentas Qt conforme as instruções acima.

### "Erro ao compilar"
Verifique se os arquivos `.ts` estão bem formatados (XML válido).

### "Traduções não aparecem na aplicação"
1. Verifique se os arquivos `.qm` foram gerados
2. Confirme se os caminhos no código estão corretos
3. Reinicie a aplicação após compilar as traduções 