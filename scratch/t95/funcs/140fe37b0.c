// THUNK ALIAS -> sub_143E30360 (jmp:0x140fe37b0->0x143e30360)
__int64 __fastcall sub_143E30360(__int64 a1)
{
  __int64 v2; // rax
  __int64 v3; // rsi
  char v4; // bl
  unsigned int v5; // eax
  int v6; // ecx
  char v7; // bl
  __int64 result; // rax
  char v9; // bl
  _BYTE v10[8]; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v11[6]; // [rsp+30h] [rbp-10h] BYREF

  v11[2] = -2;
  v2 = sub_140FE35F0();
  if ( v2 == 0 )
    return 0;
  v3 = v2;
  v4 = sub_14101D650(v2, a1);
  if ( (unsigned __int8)sub_14101D990(v3, a1) == 0
    || (v5 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 56LL))(a1)) > 0x19 )
  {
LABEL_10:
    result = 1;
    if ( v4 == 0 )
      return result;
    goto LABEL_11;
  }
  v6 = 50332201;
  if ( !_bittest(&v6, v5) )
  {
    if ( v5 == 1 && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)a1 + 56LL))(a1) == 1 )
    {
      v7 = ((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 1760LL))(a1) == 0) | v4;
      result = 1;
      if ( v7 == 0 )
        return result;
      goto LABEL_11;
    }
    goto LABEL_10;
  }
LABEL_11:
  (*(void (__fastcall **)(__int64, _BYTE *))(*(_QWORD *)a1 + 144LL))(a1, v10);
  v9 = (*(__int64 (__fastcall **)(__int64, __int64, _BYTE *, _QWORD, _DWORD))(*(_QWORD *)qword_141B5EF38 + 488LL))(
         qword_141B5EF38,
         v3,
         v10,
         0,
         0);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v11[0] + 16LL))(v11[0], v11);
  result = 3;
  if ( (~v9 & 3) != 0 )
  {
    result = 4;
    if ( (v9 & 1) == 0 )
    {
      result = 5;
      if ( (v9 & 2) == 0 )
        return v9 & 4 | 2u;
    }
  }
  return result;
}
