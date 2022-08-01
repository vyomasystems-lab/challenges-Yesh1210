# Verification of Bitmanipulation co-processor

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/74342939/182204822-66689e9b-b1ff-4442-8558-77e233f7e58c.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (Bitmanipulation co-processor module) which takes in 3 32-bit and one instruction of 32 bit as inputs and 33-bit as output. In the output signal the LSB bit is known as valid bit.

The values are assigned to the input ports using
```
dut.mav_putvalue_src1.value = mav_putvalue_src1
dut.mav_putvalue_src2.value = mav_putvalue_src2
dut.mav_putvalue_src3.value = mav_putvalue_src3
dut.EN_mav_putvalue.value = 1
dut.mav_putvalue_instr.value = mav_putvalue_instr
```

The assert statement is used for comparing the adder's outut to the expected value.
```
error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
assert dut_output == expected_mav_putvalue, error_message
```

## Test Scenario - 1 (Failed)
- Test Inputs: mav_putvalue_src1 = 0x5 , mav_putvalue_src2 = 0x6 , mav_putvalue_src3 = 0x0
- Expected Output: out = 0x3
- DUT Output: out = 0x9

Output mismatches for the above inputs proving that there is a design bug.

## Design Bug
Based on the above test inputs and analysing the design, we see the following
```
if((func7 == "0100000") and (func3 == "111") and (opcode == "0110011") ):
        print('--ANDN 1')
        mav_putvalue=mav_putvalue_src1 & (~mav_putvalue_src2)
        mav_putvalue=mav_putvalue & 0xffffffff
        mav_putvalue=(mav_putvalue<<1)|1
        return mav_putvalue
```

![image](https://user-images.githubusercontent.com/74342939/182204960-9ce92a97-74dc-4a46-aa05-55d59183c655.png)

## Verification Strategy

I created a variety of testcases for various inputs and select lines. It will be simple to debug into it by creating various scenarios.
