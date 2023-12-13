import math
import time
from bitarray import bitarray
from pyrpio.i2c import I2CBase
from pyrpio.i2c_register_device import I2CRegisterDevice
from .defs import LMK61E2ClockMode, LMK61E2Registers
from .utils import float2frac


class LMK61E2:
    def __init__(self, bus: I2CBase, address: int):
        """The LMK61E2 device is an ultra-low jitter PLLatinumTM programmable oscillator with a fractional-N
        frequency synthesizer with integrated VCO that generates commonly used reference clocks.

        Args:
            bus (I2CBase): I2C bus interface
            address (int): I2C address of chip
        """
        self.address = address
        self.i2c_reg = I2CRegisterDevice(bus, address, register_size=1, data_size=1)

    def get_registers(self) -> LMK61E2Registers:
        """Read registers from device."""
        # Read registers
        data = self.i2c_reg.read_register_sequential_bytes(21, 15)
        data_in = bytearray(data[1:12])

        # REGISTER 33
        mash_ctrl_byte = data[12]
        mash_ctrl_bits = bitarray(format(mash_ctrl_byte, "08b"))
        # REGISTER 34
        pll_ctrl0_byte = data[13]
        pll_ctrl0_bits = bitarray(format(pll_ctrl0_byte, "08b"))
        # REGISTER 35
        pll_ctrl1_byte = data[14]
        pll_ctrl1_bits = bitarray(format(pll_ctrl1_byte, "08b"))
        # REGISTER 21
        diffctrl_byte = data[0]
        diffctrl_bits = bitarray(format(diffctrl_byte, "08b"))
        # Extract values from data
        regs = LMK61E2Registers()
        regs.pll_d = int(pll_ctrl0_bits[2])
        regs.cp = int(pll_ctrl0_bits[4:8].to01(), 2)
        regs.ps = int(pll_ctrl1_bits[1:4].to01(), 2)
        regs.c3 = int(pll_ctrl1_bits[5])
        regs.dmc = int(mash_ctrl_bits[4:6].to01(), 2)
        regs.meo = int(mash_ctrl_bits[6:8].to01(), 2)
        regs.odf = LMK61E2ClockMode(int(diffctrl_bits[6:8].to01(), 2))
        raw_bits = bitarray("".join([format(b, "08b") for b in data_in]))
        regs.out_div = int(raw_bits[7:16].to01(), 2)
        regs.int_div = int(raw_bits[28:40].to01(), 2)
        regs.frac_num = int(raw_bits[42:64].to01(), 2)
        regs.frac_den = int(raw_bits[66:88].to01(), 2)
        return regs

    def regs2freq(self, regs: LMK61E2Registers) -> float:
        """Compute frequency (Hz) from registers.

        Args:
            regs (LMK61E2Registers): LMK61E2 register set

        Returns:
            float: Frequency in Hz
        """
        # Compute target frequency
        f_ref = 50.0 * 1e6
        frac_float = 0
        if regs.frac_den > 0 and regs.meo > 0:
            frac_float = regs.frac_num / regs.frac_den
        freq_hz = f_ref * (2 * regs.pll_d) * (regs.int_div + frac_float)
        freq_hz = freq_hz / regs.out_div
        return freq_hz

    def freq2regs(
        self, freq_hz, odf: LMK61E2ClockMode = LMK61E2ClockMode.LVDS
    ) -> LMK61E2Registers:
        """Compute registers from frequency (Hz). ODF is clock mode (2 = LVDS).

        Args:
            freq_hz (float): Target frequency in Hz
            odf (LMK61E2ClockMode, optional):  clock mode (2 = LVDS). Defaults to LMK61E2ClockMode.LVDS.

        Raises:
            Exception: If frequency is not achievable

        Returns:
            LMK61E2Registers: LMK61E2 registers
        """
        regs = LMK61E2Registers()
        f_out = freq_hz  # *1.0E6
        # Fixed values (Enable doubler by default)
        f_ref = 50.0 * 1.0e6
        regs.odf = LMK61E2ClockMode.LVDS.value
        regs.pll_d = 1
        # Step 1: Assume f_vco is in middle and determine out_div
        f_vco_middle = 5.0 * 1e9
        regs.out_div = int(round(f_vco_middle / f_out, 0))
        regs.out_div = max(min(regs.out_div, 511), 5)  # [5, 511]
        f_vco_desired = f_out * regs.out_div
        if f_vco_desired < 4.6e9 or f_vco_desired > 5.6e9:
            raise Exception(
                "Frequency not achievable- Fvco must be in range [4.6 GHz, 5.6 GHz]"
            )
        # Step 2: Assume fractional portion is just 0 to determine int_div
        regs.int_div = int(
            math.floor(f_vco_desired / (f_ref * (2 * regs.pll_d)) - (0 / 1))
        )
        regs.int_div = max(min(regs.int_div, 4095), 1)
        f_vco_approx = f_ref * (2 * regs.pll_d) * (regs.int_div + 0 / 1)
        # Step 3: If f_vco still off then adjust fractional portion
        if abs(f_vco_approx - f_vco_desired) < 1e-9:
            regs.frac_num = int(0)
            regs.frac_den = int(1)
            regs.ps = 0  # No phase shift
            regs.dmc = 3  # Disabled
            regs.meo = 0  # Integer mode
            regs.cp = 8  # 6.4 mA
            # NOTE: 3rd order filter should be ENABLED when doubler is enabled.
            # However, chip default has it disabled for int mode w/ doubler enabled
            # c3 = 1 if regs.pll_d is 1 else 0
            regs.c3 = 0
        else:
            frac_float = f_vco_desired / (f_ref * (2 * regs.pll_d)) - regs.int_div
            frac_num, frac_den = float2frac(frac_float)
            regs.frac_num = int(frac_num)
            regs.frac_den = int(frac_den)
            regs.ps = 2  # 1 ns for 100 MHz fPD phase shift
            regs.dmc = 0  # Weak
            regs.meo = 3  # 3rd order
            regs.cp = 4  # 1.6 mA
            regs.c3 = 1  # 3rd order filter enabled
        return regs

    def set_registers(self, regs: LMK61E2Registers, nonvolatile: bool = False):
        """Writes registers to clock IC.

        Args:
            regs (LMK61E2Registers): LMK61E2 register set
            nonvolatile (bool, optional): Write to non-volatile memory. Defaults to False.
        """
        # Binarize data
        reg_data = bitarray(
            format(regs.out_div, "016b")
            + format(0, "08b")  # (7-bit 0 w/  9-bit OUTDIV)
            + format(regs.int_div, "016b")  # (Skip register 24)
            + format(regs.frac_num, "024b")  # (4-bit 0 w/ 12-bit INT)
            + format(  # (2-bit 0 w/ 22-bit NUM)
                regs.frac_den, "024b"
            )  # (2-bit 0 w/ 22-bit DEN)
        )
        # Turn this into a byte array of bytes to send
        regs_pll_data = [
            int(reg_data[i : i + 8].to01(), 2) for i in range(0, len(reg_data), 8)
        ]

        # Write to main block of registers
        self.i2c_reg.write_register_sequential(22, regs_pll_data)
        # Write mash engine data
        mash_ctrl_bits = bitarray(format(regs.dmc, "06b") + format(regs.meo, "02b"))
        self.i2c_reg.write_register_sequential(33, [int(mash_ctrl_bits[0:8].to01(), 2)])
        # Write pll_d and cp register data
        pll_ctrl0_bits = bitarray(format(regs.pll_d, "03b") + format(regs.cp, "05b"))
        self.i2c_reg.write_register_sequential(34, [int(pll_ctrl0_bits[0:8].to01(), 2)])
        pll_ctrl1_bits = bitarray(
            format(regs.ps, "04b") + "0" + format(regs.c3, "01b") + "11"
        )
        self.i2c_reg.write_register_sequential(35, [int(pll_ctrl1_bits[0:8].to01(), 2)])
        diffctrl_bits = bitarray(format(regs.odf, "08b"))
        self.i2c_reg.write_register_sequential(21, [int(diffctrl_bits[0:8].to01(), 2)])

        # Save register data to EEPROM (via SRAM)
        if nonvolatile:
            self.i2c_reg.write_register_sequential(49, [0x50])  # Copy regs to sram
            # Check register R49.6 bit to see when done (== 0)
            done = False
            while not done:
                nvmctrlByte = self.i2c_reg.read_register(49)
                nvmctrlBits = bitarray(format(nvmctrlByte, "08b"))
                done = int(nvmctrlBits[1]) == 0
                time.sleep(0.1)
            # Enable EEPROM write
            self.i2c_reg.write_register_sequential(56, [0xBE])
            # Perform EEPROM write
            self.i2c_reg.write_register_sequential(49, [0x11])
            time.sleep(0.1)
            done = False
            while not done:
                nvmctrlByte = self.i2c_reg.read_register(49)
                nvmctrlBits = bitarray(format(nvmctrlByte, "08b"))
                done = int(nvmctrlBits[5]) == 0
            # Disable EEPROM write
            self.i2c_reg.write_register_sequential(56, [0x00])

    def set_frequency(
        self,
        freq_hz: float,
        odf: LMK61E2ClockMode = LMK61E2ClockMode.LVDS,
        nonvolatile: bool = False,
        **kwargs
    ):
        """Set clock IC to target frequency"""
        regs = self.freq2regs(freq_hz, odf=odf)
        self.set_registers(regs, nonvolatile=nonvolatile)

    def get_frequency(self):
        """Get frequency from clock IC"""
        regs = self.get_registers()
        freq = self.regs2freq(regs)
        return freq, regs


# %%
