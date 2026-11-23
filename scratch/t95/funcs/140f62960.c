// THUNK ALIAS -> sub_143D2C500 (jmp:0x140f62960->0x143d2c500)
__int64 __fastcall sub_143D2C500(unsigned int a1)
{
  __int64 result; // rax
  __int64 v2; // r9
  __int64 v3; // rax
  __int64 *v4; // rdx
  __int64 v5; // rax
  __int64 v6; // rdx

  result = 0;
  if ( (a1 & 0x80000000) == 0 && qword_141B5FE08 != 0 )
  {
    if ( (_BYTE)word_141B60320 != 0
      || (v2 = *(_QWORD *)(qword_141B5FE08 + 96), (*(_QWORD *)(qword_141B5FE08 + 104) - v2) >> 3 <= (unsigned __int64)a1) )
    {
      v4 = *(__int64 **)(qword_141B5FE08 + 128);
      v5 = *v4;
      v6 = v4[1] - *v4;
      if ( v6 == 0 || v6 >> 3 <= (unsigned __int64)a1 )
        return 0;
      v3 = v5 + 8LL * a1;
    }
    else
    {
      v3 = v2 + 8LL * a1;
    }
    return *(_QWORD *)v3;
  }
  return result;
}
