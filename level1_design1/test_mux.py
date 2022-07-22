# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux1(dut):
    """Test for mux2"""
    
    A = random.randint(0 , 3)
    select = 0
    #input driving
    dut.inp0.value = A
    dut.sel.value = select
    
    await Timer(2, units='ns')
    
    dut._log.info(f'inp1={A:02} sel={select:05} expected_out={A:02} DUT={int(dut.out.value):02}')

@cocotb.test()
async def test_mux13(dut):
    """Test for mux13"""
    
    A = random.randint(1 , 3)
    select = 13
    #input driving
    dut.inp13.value = A
    dut.sel.value = select
    
    await Timer(2, units='ns')
    
    dut._log.info(f'inp13={A:02} sel={select:05} expected_out={A:02} DUT={int(dut.out.value):02}')
    assert dut.out.value == A, "Test1 failed with: sel={A} , expected_out={B} , DUT_OUT={C}".format(A=dut.sel.value, B=dut.inp13.value, C=dut.out.value)

@cocotb.test()
async def test_mux12(dut):
    """Test for mux12"""
    
    A = random.randint(1 , 3)
    select = 12
    #input driving
    dut.inp12.value = A
    dut.sel.value = select
    
    await Timer(2, units='ns')
    
    dut._log.info(f'inp12={A:02} sel={select:05} expected_out={A:02} DUT={int(dut.out.value):02}')
    assert dut.out.value == A, "Test1 failed with: sel={A} , expected_out={B} , DUT_OUT={C}".format(A=dut.sel.value, B=dut.inp12.value, C=dut.out.value)