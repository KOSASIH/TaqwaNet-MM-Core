# src/security/quantum_security.py

import numpy as np

class QuantumSecurity:
    def __init__(self):
        """Initialize the QuantumSecurity class."""
        self.basis = ['+', 'x']  # + for rectilinear basis, x for diagonal basis
        self.key_length = 10  # Default key length
        self.sender_key = []
        self.receiver_key = []
        self.sender_basis = []
        self.receiver_basis = []

    def generate_key(self, length=None):
        """Generate a random quantum key."""
        if length is not None:
            self.key_length = length
        self.sender_key = np.random.choice([0, 1], self.key_length).tolist()
        self.sender_basis = np.random.choice(self.basis, self.key_length).tolist()
        return self.sender_key, self.sender_basis

    def measure_qubit(self, qubit, basis):
        """Simulate measuring a qubit in a given basis."""
        if basis == 'x':
            return np.random.choice([0, 1])  # Simulate measurement in diagonal basis
        return qubit  # Return the qubit as is for rectilinear basis

    def secure_key_exchange(self):
        """Simulate secure key exchange."""
        for qubit, basis in zip(self.sender_key, self.sender_basis):
            measured_qubit = self.measure_qubit(qubit, basis)
            self.receiver_key.append(measured_qubit)
            self.receiver_basis.append(basis)

    def sift_keys(self):
        """Sift the keys based on matching bases."""
        sifted_sender_key = []
        sifted_receiver_key = []
        for sender_bit, sender_basis, receiver_bit, receiver_basis in zip(self.sender_key, self.sender_basis, self.receiver_key, self.receiver_basis):
            if sender_basis == receiver_basis:
                sifted_sender_key.append(sender_bit)
                sifted_receiver_key.append(receiver_bit)
        return sifted_sender_key, sifted_receiver_key

    def verify_key(self, sender_key, receiver_key):
        """Verify the shared key between sender and receiver."""
        return sender_key == receiver_key

# Example usage
if __name__ == "__main__":
    quantum_security = QuantumSecurity()

    # Generate a quantum key
    sender_key, sender_basis = quantum_security.generate_key()
    print("Sender Key:", sender_key)
    print("Sender Basis:", sender_basis)

    # Simulate secure key exchange
    quantum_security.secure_key_exchange()
    print("Receiver Key:", quantum_security.receiver_key)
    print("Receiver Basis:", quantum_security.receiver_basis)

    # Sift the keys
    sifted_sender_key, sifted_receiver_key = quantum_security.sift_keys()
    print("Sifted Sender Key:", sifted_sender_key)
    print("Sifted Receiver Key:", sifted_receiver_key)

    # Verify the keys
    if quantum_security.verify_key(sifted_sender_key, sifted_receiver_key):
        print("Keys match! Secure communication established.")
    else:
        print("Keys do not match! Communication compromised.")
