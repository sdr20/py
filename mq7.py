import machine
import time

class MQ7Sensor:
    def __init__(self, adc_pin, rl_value=10):
        # rl_value: Load resistance on the board (in kilo-ohms)
        self.adc = machine.ADC(machine.Pin(adc_pin))
        self.adc.atten(machine.ADC.ATTN_11DB)  # Configure to read voltage range up to 3.3V
        self.rl_value = rl_value  # Load resistance in kilo-ohms

    def read_raw(self):
        return self.adc.read()

    def read_voltage(self):
        raw_value = self.read_raw()
        voltage = (raw_value / 4095) * 3.3  # Convert raw ADC value to voltage
        return voltage

    def read_sensor(self):
        voltage = self.read_voltage()

        # Calculate sensor resistance (Rs) dynamically
        if voltage > 0:  # To avoid division by zero
            rs = (3.3 - voltage) / voltage * self.rl_value
        else:
            rs = float('inf')  # If the voltage is 0, the resistance is infinite
        
        # Return voltage and resistance as indicators of gas concentration
        return voltage, rs

# Example usage
def main():
    mq7 = MQ7Sensor(adc_pin=34)  # Use the appropriate ADC pin number
    while True:
        voltage, resistance = mq7.read_sensor()
        print(f"Voltage: {voltage:.2f} V, Sensor Resistance: {resistance:.2f} kΩ")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
