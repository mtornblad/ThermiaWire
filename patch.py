import os
import re

def patch_content(content):
    # Spara originalet för att jämföra senare
    original_content = content

    # 1. Byt ut klassnamn först (TwoWire -> ThermiaTwoWire)
    # Detta måste göras innan vi byter ut "Wire" generellt för att undvika "ThermiaTwoThermiaWire"
    content = content.replace("TwoWire", "ThermiaTwoWire")
    
    # 2. Hantera filnamn i includes och kommentarer
    # Detta hanterar både <Wire.h> och "Wire.h"
    content = content.replace("Wire.h", "ThermiaWire.h")
    content = content.replace("Wire.cpp", "ThermiaWire.cpp")
    
    # 3. Byt ut makron/konstanter (t.ex. WIRE_HAS_END -> THERMIAWIRE_HAS_END)
    # Regexen letar efter WIRE_ följt av stora bokstäver/siffror/understreck
    content = re.sub(r'\bWIRE_([A-Z0-9_]+)', r'THERMIAWIRE_\1', content)
    
    # 4. Byt ut instanserna Wire och Wire1
    # \b betyder "word boundary", så den matchar "Wire" men inte "TwoWire" (eftersom det är ett ord)
    # eller "WireLess" etc.
    content = re.sub(r'\bWire\b', 'ThermiaWire', content)
    content = re.sub(r'\bWire1\b', 'ThermiaWire1', content)

    # 5. Fixa library.properties specifikt om det behövs (för snyggare namn)
    if "name=ThermiaWire" in content: 
        # Om regexen ovan redan bytte "name=Wire" till "name=ThermiaWire", låt det vara.
        pass 
    
    return content

def process_directory(root_dir):
    files_to_rename = {
        "Wire.h": "ThermiaWire.h",
        "Wire.cpp": "ThermiaWire.cpp"
    }
    
    print(f"🔍 Letar igenom: {root_dir}")

    # Steg 1: Uppdatera innehållet i alla filer
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Hoppa över scriptet själv och dolda filer
            if filename.endswith(".py") or filename.startswith("."):
                continue
            
            # Vi rör bara källkod, textfiler och properties
            if not filename.endswith(('.h', '.c', '.cpp', '.ino', '.txt', '.properties', '.md')):
                continue

            filepath = os.path.join(dirpath, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                new_content = patch_content(content)
                
                if content != new_content:
                    print(f"✏️  Patchar fil: {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                print(f"❌ Fel vid läsning/skrivning av {filepath}: {e}")

    # Steg 2: Döpa om själva källkodsfilerna
    # Vi gör detta i en separat loop efteråt för att inte störa os.walk
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in files_to_rename:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, files_to_rename[filename])
                print(f"🔄 Döper om fil: {filename} -> {files_to_rename[filename]}")
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"❌ Kunde inte döpa om {old_path}: {e}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print("🚀 Startar patchning av ThermiaWire...")
    process_directory(current_dir)
    print("✅ Klart! Biblioteket är nu konverterat.")