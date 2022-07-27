# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut._log.info("current_state after reset = %s" , dut.current_state.value)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 0 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 0 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)
    
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)
    
    assert dut.seq_seen.value == 1, f"Test failed with {dut.seq_seen.value} != 1"
