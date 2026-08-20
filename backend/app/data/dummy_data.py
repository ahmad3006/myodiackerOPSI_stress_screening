"""Generator data dummy sintetis (biosinyal + teks Bahasa Indonesia)."""

from __future__ import annotations

import pandas as pd
import numpy as np


def generate_dummy_biosignal(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    """1000 sampel sintetis EMG (mV), HRV (ms), GSR (uS) dengan label 0/1/2.

    Pola fisiologis yang disimulasikan:
    - Normal: EMG rendah, HRV tinggi, GSR rendah
    - Waspada: nilai menengah
    - Stres tinggi: EMG tinggi, HRV rendah, GSR tinggi
    """
    rng = np.random.default_rng(seed)
    n_per_class = n_samples // 3
    remainder = n_samples - (n_per_class * 3)
    counts = [n_per_class, n_per_class, n_per_class + remainder]

    rows: list[dict] = []
    params = {
        0: {"emg": (0.22, 0.07), "hrv": (78.0, 8.0), "gsr": (3.2, 0.7)},
        1: {"emg": (0.72, 0.12), "hrv": (48.0, 6.5), "gsr": (8.4, 1.1)},
        2: {"emg": (1.45, 0.22), "hrv": (26.0, 5.0), "gsr": (14.8, 1.9)},
    }

    for label, count in enumerate(counts):
        emg, hrv, gsr = params[label]["emg"], params[label]["hrv"], params[label]["gsr"]
        for _ in range(count):
            rows.append(
                {
                    "emg": float(np.clip(rng.normal(*emg), 0.05, 3.0)),
                    "hrv": float(np.clip(rng.normal(*hrv), 12.0, 130.0)),
                    "gsr": float(np.clip(rng.normal(*gsr), 0.4, 28.0)),
                    "label": int(label),
                }
            )

    df = pd.DataFrame(rows)
    return df.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def generate_dummy_text() -> tuple[list[str], list[int]]:
    """Kalimat dummy Bahasa Indonesia untuk 3 kelas stres."""
    normal = [
        "hari ini saya belajar dengan tenang",
        "suasana hati saya baik-baik saja",
        "saya merasa damai dan nyaman",
        "pekerjaan sekolah sudah selesai dengan rapi",
        "saya istirahat cukup dan badan terasa fresh",
        "belajar kelompok berjalan lancar dan menyenangkan",
        "saya bisa fokus tanpa tekanan",
        "hari ini cuaca bagus dan mood saya positif",
        "saya bersyukur semuanya berjalan sesuai rencana",
        "tidur semalam nyenyak jadi pagi ini semangat",
        "saya menikmati waktu bersama teman",
        "tugas sudah teratur jadi tidak terburu-buru",
        "saya merasa rileks setelah olahraga ringan",
        "pikiran saya jernih untuk mengerjakan soal",
        "tidak ada yang perlu dikhawatirkan hari ini",
        "saya tenang menghadapi ujian karena sudah belajar",
        "suasana kelas nyaman dan mendukung",
        "saya puas dengan hasil latihan soal",
        "hari ini terasa ringan dan menyenangkan",
        "saya mampu mengatur waktu dengan baik",
    ]
    waspada = [
        "hari ini agak melelahkan tapi masih bisa dikontrol",
        "saya mulai cemas karena tugas menumpuk",
        "tidur kurang nyenyak jadi konsentrasi menurun",
        "ada sedikit tekanan menjelang deadline",
        "saya khawatir nilai kuis kemarin kurang bagus",
        "pikiran saya agak kacau tapi masih sanggup",
        "saya merasa tegang saat presentasi sebentar lagi",
        "banyak pekerjaan rumah yang belum selesai",
        "saya mudah terdistraksi dan sedikit gelisah",
        "jadwal hari ini padat sehingga cukup melelahkan",
        "saya takut tertinggal materi pelajaran",
        "ada rasa was-was menunggu pengumuman nilai",
        "badan terasa capek dan mood naik turun",
        "saya perlu istirahat karena mulai tertekan",
        "tugas kelompok belum rapi dan itu membuat cemas",
        "saya overthinking soal ujian minggu depan",
        "suasana hati tidak stabil sejak pagi",
        "saya merasa terburu-buru sepanjang hari",
        "ada tekanan dari orang tua soal prestasi",
        "saya mulai kehilangan fokus belajar",
    ]
    stres_tinggi = [
        "hari ini sangat melelahkan dan saya tidak kuat",
        "saya stres berat karena tugas tidak ada habisnya",
        "dada terasa sesak dan pikiran kacau sekali",
        "saya panik menghadapi ujian yang sangat sulit",
        "semuanya terasa hancur dan saya ingin menyerah",
        "saya cemas berlebihan sampai sulit tidur",
        "tekanan sekolah membuat saya kewalahan total",
        "saya menangis karena tidak sanggup lagi",
        "pikiran negatif terus muncul dan sangat mengganggu",
        "saya takut gagal dan kecewa pada diri sendiri",
        "badan gemetar karena terlalu tegang",
        "saya merasa putus asa dengan nilai yang jelek",
        "tidak bisa fokus sama sekali karena stres tinggi",
        "saya overthinking parah sampai sakit kepala",
        "semua deadline bentrok dan saya hampir collapse",
        "saya merasa tertekan luar biasa oleh ekspektasi",
        "suasana hati sangat buruk dan mudah marah",
        "saya kelelahan mental dan fisik sekaligus",
        "tidak ada yang membantu dan saya merasa sendiri",
        "saya takut tidak lulus dan masa depan hancur",
    ]

    prefixes = ["", "jujur ", "hari ini ", "sebenarnya "]
    suffixes = ["", " sekali", " banget", " ya"]

    texts: list[str] = []
    labels: list[int] = []
    for base_list, label in ((normal, 0), (waspada, 1), (stres_tinggi, 2)):
        for sentence in base_list:
            for prefix in prefixes:
                for suffix in suffixes:
                    texts.append((prefix + sentence + suffix).strip())
                    labels.append(label)
    return texts, labels
