"""
Titik masuk utama untuk Sistem Navigasi Kampus.
Menyediakan antarmuka CLI Interaktif.
"""
import sys
import os

# Memastikan PYTHONPATH mencakup direktori saat ini agar import src berjalan lancar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.modules.data_generator import generate_campus_data
from src.modules.navigation import NavigationSystem

def main():
    print("=================================================")
    print("Membangun Sistem Navigasi Kampus UNY...")
    graph, bst = generate_campus_data()
    nav_sys = NavigationSystem(graph)
    
    print("Data berhasil dimuat (30 Gedung, 55 Edge).")
    print("Sistem siap. Selamat datang di Sistem Navigasi Kampus UNY.")
    print("=================================================")
    
    print("\nPerintah yang tersedia:")
    print("1. JALUR       - Mencari rute terpendek antar dua gedung (Dijkstra)")
    print("2. CARI_GEDUNG - Memeriksa eksistensi gedung (BST) & relasi neighbor")
    print("3. JELAJAH_DFS - Menjelajah struktur graf dari suatu gedung awal (DFS)")
    print("4. TERISOLASI  - Menampilkan gedung yang tidak terhubung dengan gedung manapun")
    print("5. KELUAR      - Menghentikan program")
    
    while True:
        try:
            cmd = input("\nMasukkan perintah (JALUR/CARI_GEDUNG/JELAJAH_DFS/TERISOLASI/KELUAR): ").strip().upper()
            
            if cmd == "KELUAR" or cmd == "5":
                print("Terima kasih telah menggunakan Sistem Navigasi Kampus.")
                break
                
            elif cmd == "JALUR" or cmd == "1":
                start = input("  Masukkan Gedung Asal: ").strip()
                end = input("  Masukkan Gedung Tujuan: ").strip()
                
                if not bst.search(start):
                    print(f"  [ERROR] Gedung '{start}' tidak terdaftar di sistem.")
                    continue
                if not bst.search(end):
                    print(f"  [ERROR] Gedung '{end}' tidak terdaftar di sistem.")
                    continue
                    
                path, distance = nav_sys.dijkstra(start, end)
                if path:
                    print(f"\n  Jalur terpendek dari {start} ke {end}:")
                    print("  " + " -> ".join(path))
                    print(f"  Total Jarak: {distance} meter")
                else:
                    print(f"\n  [INFO] Tidak ada jalur yang tersedia dari {start} ke {end}.")
                    
            elif cmd == "CARI_GEDUNG" or cmd == "2":
                target = input("  Masukkan nama gedung yang dicari: ").strip()
                node = bst.search(target)
                if node:
                    print(f"  [INFO] Gedung '{target}' DITEMUKAN dalam sistem (BST Search).")
                    neighbors = graph.get_neighbors(target)
                    print(f"  Gedung ini terhubung langsung dengan {len(neighbors)} gedung lainnya:")
                    for n, w in neighbors:
                        print(f"   - {n} (jarak: {w}m)")
                else:
                    print(f"  [ERROR] Gedung '{target}' TIDAK DITEMUKAN.")
                    
            elif cmd == "JELAJAH_DFS" or cmd == "3":
                start = input("  Masukkan Gedung Awal untuk Penjelajahan: ").strip()
                if not bst.search(start):
                    print(f"  [ERROR] Gedung '{start}' tidak terdaftar di sistem.")
                    continue
                
                visited = nav_sys.dfs_exploration(start)
                print(f"\n  [INFO] Hasil Penjelajahan DFS dari '{start}' (Total {len(visited)} gedung dikunjungi):")
                print("  " + " -> ".join(visited))
                
            elif cmd == "TERISOLASI" or cmd == "4":
                isolated = nav_sys.get_isolated_buildings()
                if isolated:
                    print(f"\n  [INFO] Ditemukan {len(isolated)} gedung terisolasi:")
                    for b in isolated:
                        print(f"   - {b}")
                else:
                    print("\n  [INFO] Tidak ada gedung terisolasi. Semua gedung memiliki minimal 1 rute ke gedung lain.")
                    
            else:
                print("  [ERROR] Perintah tidak dikenali. Silakan coba lagi.")
                
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar dari sistem secara paksa...")
            break
        except Exception as e:
            print(f"  [ERROR] Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()