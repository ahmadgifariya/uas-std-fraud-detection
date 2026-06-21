from collections import deque, defaultdict
from dataclasses import dataclass


# =========================================================
# DATA MODEL TRANSAKSI
# =========================================================

@dataclass
class Transaction:
    id: str
    sender: str
    receiver: str
    amount: int
    note: str


# =========================================================
# STRUKTUR DATA 1: QUEUE / FIFO
# First In First Out
# =========================================================

class TransactionQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, transaction):
        self.queue.append(transaction)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


# =========================================================
# STRUKTUR DATA 2: STACK / LIFO
# Last In First Out
# =========================================================

class SuspiciousStack:
    def __init__(self):
        self.stack = []

    def push(self, transaction, status, reason):
        self.stack.append({
            "transaction": transaction,
            "status": status,
            "reason": reason
        })

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


# =========================================================
# STRUKTUR DATA 3: GRAPH
# Directed Weighted Graph dengan Adjacency List
# Vertex = akun
# Edge = transaksi
# Weight = nominal transaksi
# =========================================================

class TransactionGraph:
    def __init__(self):
        self.adj_list = defaultdict(list)
        self.vertices = set()

    def add_transaction(self, transaction):
        sender = transaction.sender
        receiver = transaction.receiver
        amount = transaction.amount

        self.vertices.add(sender)
        self.vertices.add(receiver)

        # Directed edge: sender -> receiver
        self.adj_list[sender].append((receiver, amount, transaction.id))

    def display_graph(self):
        print("\n=== REPRESENTASI GRAPH: ADJACENCY LIST ===")

        for account in sorted(self.vertices):
            edges = self.adj_list.get(account, [])

            if edges:
                edge_text = []
                for receiver, amount, transaction_id in edges:
                    edge_text.append(
                        f"{receiver}({transaction_id}, {format_rupiah(amount)})"
                    )
                print(f"{account} -> {', '.join(edge_text)}")
            else:
                print(f"{account} -> Tidak ada transaksi keluar")

    def detect_cycles(self):
        """
        Mendeteksi siklus pada directed graph.
        Siklus berarti terdapat jalur transaksi yang kembali ke akun awal.
        """

        cycles_set = set()

        def normalize_cycle(cycle):
            """
            Normalisasi siklus supaya siklus yang sama tidak tercatat berulang.
            Contoh:
            A001 -> A002 -> A003
            A002 -> A003 -> A001
            dianggap siklus yang sama.
            """
            min_index = min(range(len(cycle)), key=lambda i: cycle[i])
            normalized = cycle[min_index:] + cycle[:min_index]
            return tuple(normalized)

        def dfs(start, current, path, visited):
            for neighbor, amount, transaction_id in self.adj_list.get(current, []):
                # Jika kembali ke akun awal, berarti ditemukan siklus
                if neighbor == start and len(path) >= 2:
                    cycle = normalize_cycle(path.copy())
                    cycles_set.add(cycle)

                # Jika neighbor belum dikunjungi di jalur ini, lanjut DFS
                elif neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)

                    dfs(start, neighbor, path, visited)

                    path.pop()
                    visited.remove(neighbor)

        for start in sorted(self.vertices):
            dfs(start, start, [start], {start})

        cycles = [list(cycle) for cycle in cycles_set]
        cycles.sort(key=lambda c: (len(c), c))

        return cycles

    def get_cycle_edges(self, cycles):
        """
        Mengambil pasangan edge yang termasuk dalam siklus.
        Contoh siklus:
        A001 -> A002 -> A003 -> A001

        Edge siklus:
        (A001, A002), (A002, A003), (A003, A001)
        """
        cycle_edges = set()

        for cycle in cycles:
            for i in range(len(cycle)):
                sender = cycle[i]
                receiver = cycle[(i + 1) % len(cycle)]
                cycle_edges.add((sender, receiver))

        return cycle_edges


# =========================================================
# STRUKTUR DATA 4: TREE
# Decision Tree sederhana untuk klasifikasi transaksi
# =========================================================

class DecisionTree:
    def __init__(self):
        self.high_amount_threshold = 5_000_000
        self.warning_amount_threshold = 4_500_000

    def classify(self, transaction, cycle_edges):
        """
        Pohon keputusan sederhana:

        1. Jika nominal >= 5.000.000 dan transaksi masuk siklus:
           status = FRAUD

        2. Jika transaksi masuk siklus:
           status = MENCURIGAKAN

        3. Jika nominal >= 4.500.000:
           status = MENCURIGAKAN

        4. Selain itu:
           status = AMAN
        """

        edge = (transaction.sender, transaction.receiver)
        is_cycle_edge = edge in cycle_edges

        # Root: cek nominal besar
        if transaction.amount >= self.high_amount_threshold:
            # Cabang: cek apakah transaksi berada dalam siklus graph
            if is_cycle_edge:
                return "FRAUD", "Nominal besar dan berada dalam siklus transaksi"
            else:
                return "MENCURIGAKAN", "Nominal besar"

        # Cabang berikutnya: cek apakah transaksi berada dalam siklus graph
        if is_cycle_edge:
            return "MENCURIGAKAN", "Transaksi berada dalam siklus"

        # Cabang berikutnya: cek nominal mendekati besar
        if transaction.amount >= self.warning_amount_threshold:
            return "MENCURIGAKAN", "Nominal transaksi mendekati batas risiko"

        # Leaf terakhir: aman
        return "AMAN", "Tidak masuk pola risiko utama"


# =========================================================
# DATA SIMULASI
# Minimal 10 vertex dan 15 edge
# =========================================================

def get_sample_transactions():
    return [
        Transaction("T01", "A001", "A002", 1_500_000, "Transfer sedang"),
        Transaction("T02", "A002", "A003", 1_750_000, "Transfer sedang"),
        Transaction("T03", "A003", "A001", 1_600_000, "Membentuk siklus"),

        Transaction("T04", "A004", "A005", 800_000, "Transfer normal"),
        Transaction("T05", "A005", "A006", 900_000, "Transfer normal"),
        Transaction("T06", "A006", "A004", 850_000, "Membentuk siklus"),

        Transaction("T07", "A007", "A008", 5_000_000, "Nominal besar"),
        Transaction("T08", "A008", "A009", 4_900_000, "Nominal besar"),
        Transaction("T09", "A009", "A010", 5_100_000, "Nominal besar"),
        Transaction("T10", "A010", "A007", 5_000_000, "Siklus nominal besar"),

        Transaction("T11", "A001", "A004", 300_000, "Transfer kecil"),
        Transaction("T12", "A002", "A005", 250_000, "Transfer kecil"),
        Transaction("T13", "A003", "A006", 280_000, "Transfer kecil"),
        Transaction("T14", "A007", "A002", 700_000, "Transfer tambahan"),
        Transaction("T15", "A009", "A003", 650_000, "Transfer tambahan"),
    ]


# =========================================================
# FUNGSI BANTUAN
# =========================================================

def format_rupiah(amount):
    return "Rp" + f"{amount:,}".replace(",", ".")


def print_line():
    print("-" * 95)


def print_transaction_table(transactions):
    print("\n=== DATA TRANSAKSI SIMULASI ===")
    print_line()
    print(f"{'ID':<6} {'Dari':<8} {'Ke':<8} {'Nominal':<18} {'Keterangan'}")
    print_line()

    for t in transactions:
        print(f"{t.id:<6} {t.sender:<8} {t.receiver:<8} {format_rupiah(t.amount):<18} {t.note}")

    print_line()


def print_cycles(cycles):
    print("\n=== HASIL DETEKSI SIKLUS GRAPH ===")

    if not cycles:
        print("Tidak ditemukan siklus transaksi.")
        return

    for i, cycle in enumerate(cycles, start=1):
        cycle_path = cycle + [cycle[0]]
        print(f"Siklus {i}: {' -> '.join(cycle_path)}")


# =========================================================
# PROGRAM UTAMA
# =========================================================

def main():
    print("=" * 95)
    print("SIMULASI DETEKSI PENIPUAN TRANSAKSI KEUANGAN")
    print("Menggunakan FIFO, LIFO, Tree, dan Graph")
    print("=" * 95)

    # -----------------------------------------------------
    # 1. Ambil data transaksi simulasi
    # -----------------------------------------------------
    transactions = get_sample_transactions()
    print_transaction_table(transactions)

    # -----------------------------------------------------
    # 2. FIFO / Queue: memasukkan transaksi ke antrian
    # -----------------------------------------------------
    transaction_queue = TransactionQueue()

    for transaction in transactions:
        transaction_queue.enqueue(transaction)

    print("\n=== FIFO / QUEUE ===")
    print(f"Jumlah transaksi masuk ke queue: {transaction_queue.size()}")
    print("Transaksi akan diproses berdasarkan urutan masuk.")

    # -----------------------------------------------------
    # 3. Graph: membangun relasi antar akun
    # -----------------------------------------------------
    graph = TransactionGraph()

    for transaction in transactions:
        graph.add_transaction(transaction)

    graph.display_graph()

    # -----------------------------------------------------
    # 4. Deteksi siklus menggunakan DFS Cycle Detection
    # -----------------------------------------------------
    cycles = graph.detect_cycles()
    cycle_edges = graph.get_cycle_edges(cycles)

    print_cycles(cycles)

    # -----------------------------------------------------
    # 5. Tree + Stack:
    #    Tree untuk klasifikasi transaksi.
    #    Stack untuk menyimpan transaksi mencurigakan/fraud.
    # -----------------------------------------------------
    decision_tree = DecisionTree()
    suspicious_stack = SuspiciousStack()

    result_summary = {
        "AMAN": 0,
        "MENCURIGAKAN": 0,
        "FRAUD": 0
    }

    processed_results = []

    print("\n=== PROSES TRANSAKSI FIFO + KLASIFIKASI TREE ===")
    print_line()
    print(f"{'ID':<6} {'Dari':<8} {'Ke':<8} {'Nominal':<18} {'Status':<15} {'Alasan'}")
    print_line()

    while not transaction_queue.is_empty():
        current_transaction = transaction_queue.dequeue()

        status, reason = decision_tree.classify(
            current_transaction,
            cycle_edges
        )

        result_summary[status] += 1

        processed_results.append({
            "transaction": current_transaction,
            "status": status,
            "reason": reason
        })

        # Jika transaksi mencurigakan atau fraud, masukkan ke stack
        if status in ["MENCURIGAKAN", "FRAUD"]:
            suspicious_stack.push(current_transaction, status, reason)

        print(
            f"{current_transaction.id:<6} "
            f"{current_transaction.sender:<8} "
            f"{current_transaction.receiver:<8} "
            f"{format_rupiah(current_transaction.amount):<18} "
            f"{status:<15} "
            f"{reason}"
        )

    print_line()

    # -----------------------------------------------------
    # 6. LIFO / Stack: menampilkan transaksi mencurigakan
    #    dari yang terakhir masuk
    # -----------------------------------------------------
    print("\n=== LIFO / STACK: DAFTAR INVESTIGASI TRANSAKSI MENCURIGAKAN ===")
    print("Transaksi terakhir yang masuk stack akan diperiksa terlebih dahulu.")
    print_line()
    print(f"{'Urutan':<8} {'ID':<6} {'Dari':<8} {'Ke':<8} {'Nominal':<18} {'Status':<15} {'Alasan'}")
    print_line()

    investigation_order = 1

    while not suspicious_stack.is_empty():
        item = suspicious_stack.pop()
        transaction = item["transaction"]

        print(
            f"{investigation_order:<8} "
            f"{transaction.id:<6} "
            f"{transaction.sender:<8} "
            f"{transaction.receiver:<8} "
            f"{format_rupiah(transaction.amount):<18} "
            f"{item['status']:<15} "
            f"{item['reason']}"
        )

        investigation_order += 1

    print_line()

    # -----------------------------------------------------
    # 7. Ringkasan akhir
    # -----------------------------------------------------
    print("\n=== RINGKASAN HASIL AKHIR ===")
    print(f"Total transaksi              : {len(transactions)}")
    print(f"Total akun / vertex          : {len(graph.vertices)}")
    print(f"Total transaksi / edge       : {len(transactions)}")
    print(f"Total siklus terdeteksi      : {len(cycles)}")
    print(f"Transaksi aman               : {result_summary['AMAN']}")
    print(f"Transaksi mencurigakan       : {result_summary['MENCURIGAKAN']}")
    print(f"Transaksi fraud              : {result_summary['FRAUD']}")

    print("\n=== PENJELASAN SINGKAT ===")
    print("1. FIFO digunakan untuk memproses transaksi berdasarkan urutan masuk.")
    print("2. Tree digunakan untuk menentukan status transaksi.")
    print("3. Stack/LIFO digunakan untuk menyimpan transaksi mencurigakan sebagai daftar investigasi.")
    print("4. Graph digunakan untuk memodelkan hubungan antar akun dan mendeteksi siklus transaksi.")
    print("5. Siklus transaksi dapat menjadi indikasi awal adanya pola transaksi mencurigakan.")


# =========================================================
# EKSEKUSI PROGRAM
# =========================================================

if __name__ == "__main__":
    main()