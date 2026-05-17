def main():
    g = Graph()
    bst = BSTGedung()
 
    # Inisialisasi data
    for gid, gname in GEDUNG_DATA:
        g.add_node(gid, gname)
        bst.insert(gid, gname)
 
    edges = generate_edges(GEDUNG_DATA, seed=7)
    for u, v, w in edges:
        g.add_edge(u, v, w)
 
    print('='*55)
    print(' SMART CAMPUS NAVIGATION SYSTEM '.center(55, '='))
    print('='*55)
    print("Ketik 'BANTUAN' untuk melihat daftar perintah.")
    
    while True:
        try:
            inp = input("\n[SmartCampus] > ").strip().split()
            if not inp: continue
                
            cmd = inp[0].upper()
            
            if cmd == "BANTUAN":
                print("1. JALUR <sumber> <tujuan>         (Cari rute terpendek)")
                print("2. JELAJAH_DFS <sumber>            (Eksplorasi DFS)")
                print("3. JELAJAH_BFS <sumber>            (Eksplorasi BFS)")
                print("4. CARI_GEDUNG <kode>              (Cari nama gedung)")
                print("5. HAPUS_GEDUNG <kode>             (Hapus dari direktori)")
                print("6. DIREKTORI                       (Lihat semua gedung urut abjad)")
                print("7. TERISOLASI                      (Cek jaringan terputus)")
                print("8. TAMBAH_GEDUNG <kode> <nama...>  (Tambah gedung baru)")
                print("9. TAMBAH_JALAN <u> <v> <meter>   (Tambah koridor baru)")
                print("10. LAPORAN_GRAPH                  (Statistik lengkap graph)")
                print("11. KELUAR")
                
            elif cmd == "JALUR":
                if len(inp) != 3:
                    print("Format salah! Gunakan: JALUR <sumber> <tujuan>")
                    continue
                src, dst = inp[1], inp[2]
                if src not in g.adj:
                    print(f"Gedung asal [{src}] tidak ditemukan di graph.")
                    continue
                if dst not in g.adj:
                    print(f"Gedung tujuan [{dst}] tidak ditemukan di graph.")
                    continue
 
                t_start = time.perf_counter()
                dist, parent = dijkstra(g, src)
                t_end = time.perf_counter()
                
                if dist.get(dst, float('inf')) == float('inf'):
                    print(f"Tidak ada jalur dari {src} ke {dst} (gedung terisolasi).")
                else:
                    path = reconstruct_path(parent, src, dst)
                    print(f"Jalur: {' -> '.join(path)}")
                    print(f"Total Jarak: {dist[dst]} meter")
                    print(f"[Big-O: O(V^2 + E) | Waktu Eksekusi: {(t_end-t_start)*1000:.4f} ms]")
                    
            elif cmd == "JELAJAH_DFS":
                if len(inp) != 2: continue
                if inp[1] not in g.adj:
                    print(f"Gedung [{inp[1]}] tidak ditemukan di graph.")
                    continue
                print("Kunjungan DFS:", " -> ".join(dfs(g, inp[1])))
                print("[Big-O: O(V + E)]")
                
            elif cmd == "JELAJAH_BFS":
                if len(inp) != 2: continue
                if inp[1] not in g.adj:
                    print(f"Gedung [{inp[1]}] tidak ditemukan di graph.")
                    continue
                print("Kunjungan BFS:", " -> ".join(bfs(g, inp[1])))
                print("[Big-O: O(V + E)]")
                
            elif cmd == "CARI_GEDUNG":
                if len(inp) != 2: continue
                nama = bst.search(inp[1])
                if nama:
                    print(f"Ditemukan: {nama}")
                else:
                    print("Gedung tidak ditemukan.")
                print("[Big-O: O(log V)]")
                
            elif cmd == "HAPUS_GEDUNG":
                if len(inp) != 2: continue
                kode = inp[1]
                if bst.search(kode):
                    bst.delete(kode)
                    print(f"Gedung [{kode}] berhasil dihapus dari direktori BST.")
                    print(f"Catatan: edge di graph tetap ada (hapus edge manual jika perlu).")
                else:
                    print(f"Gedung [{kode}] tidak ditemukan.")
                print("[Big-O: O(log V)]")
 
            elif cmd == "DIREKTORI":
                print("\n".join(bst.inorder()))
                print("\n[Big-O: O(V)]")
 
            elif cmd == "TERISOLASI":
                terisolasi = deteksi_terisolasi(g, 'A1')
                if not terisolasi:
                    print("Audit Selesai: Jaringan aman, tidak ada gedung terisolasi.")
                else:
                    print(f"PERINGATAN! Ditemukan {len(terisolasi)} gedung TERISOLASI:")
                    for gid, nama in terisolasi:
                        print(f"- [{gid}] {nama}")
                print("[Big-O: O(V + E)]")
 
            elif cmd == "TAMBAH_GEDUNG":
                if len(inp) < 3:
                    print("Format salah! Gunakan: TAMBAH_GEDUNG <kode> <nama>")
                    continue
                kode = inp[1]
                nama = ' '.join(inp[2:])
                if kode in g.adj:
                    print(f"Gedung [{kode}] sudah ada di graph.")
                else:
                    t_start = time.perf_counter()
                    g.add_node(kode, nama)
                    bst.insert(kode, nama)
                    t_end = time.perf_counter()
                    print(f"Gedung [{kode}] {nama} berhasil ditambahkan.")
                    print(f"[Big-O: add_node O(1) | BST insert O(log V) | Waktu: {(t_end-t_start)*1000:.4f} ms]")
 
            elif cmd == "TAMBAH_JALAN":
                if len(inp) != 4:
                    print("Format salah! Gunakan: TAMBAH_JALAN <u> <v> <jarak_meter>")
                    continue
                u, v = inp[1], inp[2]
                if u not in g.adj:
                    print(f"Gedung [{u}] tidak ditemukan di graph.")
                    continue
                if v not in g.adj:
                    print(f"Gedung [{v}] tidak ditemukan di graph.")
                    continue
                try:
                    jarak = int(inp[3])
                except ValueError:
                    print("Jarak harus bilangan bulat.")
                    continue
                t_start = time.perf_counter()
                g.add_edge(u, v, jarak)
                t_end = time.perf_counter()
                nama_u = g.node_names.get(u, u)
                nama_v = g.node_names.get(v, v)
                print(f"Koridor {u} ({nama_u}) <-> {v} ({nama_v}) sejauh {jarak} meter ditambahkan.")
                print(f"[Big-O: O(1) | Waktu: {(t_end-t_start)*1000:.4f} ms]")
 
            elif cmd == "LAPORAN_GRAPH":
                V = len(g.adj)
                total_edge = 0
                for nid in g.adj:
                    cur = g.adj[nid]
                    while cur:
                        total_edge += 1
                        cur = cur.next
                E = total_edge // 2
 
                print(f"\n{'='*45}")
                print(f"  LAPORAN GRAPH KAMPUS UNY")
                print(f"{'='*45}")
                print(f"  Jumlah gedung (V) : {V}")
                print(f"  Jumlah koridor (E): {E}")
                print(f"  Kepadatan graph   : {E / max(1, V*(V-1)//2):.4f}  (1.0 = complete)")
                print(f"\n  -- Degree tiap gedung --")
                degrees = []
                for nid in g.adj:
                    deg = len(g.neighbors(nid))
                    degrees.append((nid, deg, g.node_names.get(nid, '')))
                degrees.sort(key=lambda x: x[1], reverse=True)
                for nid, deg, nama in degrees:
                    print(f"  {nid:4s} | {nama:30s} | degree = {deg}")
                print(f"\n  -- Top-3 Hub (paling terhubung) --")
                for nid, deg, nama in degrees[:3]:
                    print(f"  {nid} ({nama}) — degree {deg}")
                print(f"{'='*45}")
                print(f"[Big-O: O(V + E)]")
 
            elif cmd == "KELUAR":
                print("Menutup Smart Campus Navigation System. Sampai jumpa!")
                break
                
            else:
                print("Perintah tidak dikenali. Ketik BANTUAN.")
                
        except KeyboardInterrupt:
            print("\nSistem dihentikan paksa. Sampai jumpa!")
            break
 
 
if __name__ == '__main__':
    main()
