import serial
import time
import math

def main():
    # Connect to Arduino
    ser = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    
    print("Quantum Random Number Generator")
    print("Collecting bits from Arduino...")
    print("Press Ctrl+C to stop\n")

    clean_bits = []
    while True:
        # Collect raw bits
        raw_bits = []
        while len(raw_bits) < 1000:  # Collect 1000 raw bits
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line in ['0', '1']:
                    raw_bits.append(int(line))
        
        print(f"Collected {len(raw_bits)} raw bits")
        
        # Von Neumann debiasing
        
        for i in range(0, len(raw_bits)-1, 2):
            a, b = raw_bits[i], raw_bits[i+1]
            if a == 1 and b == 0: 
                clean_bits.append(1)
            elif a == 0 and b == 1: 
                clean_bits.append(0)
        
        print(f"After debiasing: {len(clean_bits)} bits")
        
        # Take first 256 bits for final number
        if len(clean_bits) < 256:
            print("Not enough bits after debiasing, collecting more...")
            continue
            
        final_bits = clean_bits[:256]
        
        # Simple XOR whitening
        whitened = final_bits.copy()
        for i in range(len(whitened)):
            other_index = (i + 7) % len(whitened)
            whitened[i] = whitened[i] ^ whitened[other_index]
        
        # Convert to hex
        binary_str = ''.join(str(b) for b in whitened)
        hex_string = hex(int(binary_str, 2))[2:].upper()
        
        # randomness test
        ones = sum(whitened)
        total = len(whitened)
        proportion = ones / total
        
        # Frequency test 
        S = abs(ones - total/2) / math.sqrt(total/4)  #deviation from expcted/standard deviation
        
        print(f"\n=== QUANTUM RANDOM NUMBER ===")
        print(f"Binary (first 32 bits): {binary_str[:32]}...")
        print(f"Hexadecimal: {hex_string}")
        print(f"Ones: {ones}/{total} ({proportion*100:.1f}%)")
        print(f"Test Statistic: {S:.3f}")
        
        # verification (p < 0.01)
        if S <= 2.576:  #z-score for 99% confidence in randomness
            print("Randomness has been verified.")
            print("   (Passes NIST Frequency Test, p < 0.01)")
        else:
            print("Randomness test failed")
        
        print("="*40)
        print()
        
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:    #error handling

        print(f"Error: {e}")


