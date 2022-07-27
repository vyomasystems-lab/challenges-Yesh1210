import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test1(dut):
    """Test for finding bug in addition"""
    
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # reset
    dut.rstn.value = 0
    await FallingEdge(dut.clk)  
    dut.rstn.value = 1
    await FallingEdge(dut.clk)
    
    A = 5
    B = 10
    C = 0
    # input driving
    dut.in1.value = A
    dut.in2.value = B
    dut.opcode.value = C
    await FallingEdge(dut.clk)

    dut._log.info(f'A={A:05} B={B:05} C={C:05} model={A+B:05} DUT={int(dut.out_top.value):05}')
    assert dut.out_top.value == A+B, "Test1 failed with: in1={A} , in2={B} , opcode={C} , DUT_OUT={D}".format(A=dut.in1.value, B=dut.in2.value, C=dut.opcode.value, D=dut.out_top.value)


@cocotb.test()
async def test2(dut):
    """Test for finding bug in subtraction"""
    
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # reset
    dut.rstn.value = 0
    await FallingEdge(dut.clk)  
    dut.rstn.value = 1
    await FallingEdge(dut.clk)
    
    A = 4
    B = 2
    C = 1
    # input driving

    dut.in1.value = A
    dut.in2.value = B
    dut.opcode.value = C
    await FallingEdge(dut.clk)

    dut._log.info(f'A={A:05} B={B:05} C={C:05} model={A-B:05} DUT={int(dut.out_top.value):05}')
    assert dut.out_top.value == A-B, "Test2 failed with: in1={A} , in2={B} , opcode={C} , DUT_OUT={D}".format(A=dut.in1.value, B=dut.in2.value, C=dut.opcode.value, D=dut.out_top.value)