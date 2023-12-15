class GoldenRatioCalculator:
    def __init__(self):
        self.phi = None

    def calculate_phi(self, a, b):
        """
        Menghitung Golden Ratio (phi) berdasarkan dua angka a dan b.
        Formula: phi = (a + b) / a
        """
        if a <= 0 or b <= 0:
            raise ValueError("Angka harus lebih besar dari 0.")
        self.phi = (a + b) / a
        return self.phi

    def get_phi(self):
        """
        Mendapatkan nilai Golden Ratio (phi) yang telah dihitung sebelumnya.
        """
        if self.phi is None:
            raise ValueError("Anda perlu menghitung phi terlebih dahulu.")
        return self.phi


# Contoh penggunaan:
calculator = GoldenRatioCalculator()

# Menghitung phi dengan angka 3 dan 5
phi_value = calculator.calculate_phi(3, 5)
print(f"Nilai Golden Ratio (phi) untuk 3 dan 5 adalah: {phi_value}")

# Mendapatkan nilai phi yang telah dihitung sebelumnya
previous_phi = calculator.get_phi()
print(f"Nilai Golden Ratio (phi) yang telah dihitung sebelumnya adalah: {previous_phi}")
