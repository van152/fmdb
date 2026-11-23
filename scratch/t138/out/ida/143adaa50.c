__int64 __fastcall sub_143ADAA50(__int64 a1, int a2)
{
  __int64 *v4; // rsi
  __int64 v5; // rdi
  __int64 v6; // rcx
  __int64 v7; // r8
  char v8; // bl
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  __int64 v12; // [rsp+48h] [rbp-40h] BYREF
  __int64 v13; // [rsp+50h] [rbp-38h] BYREF
  __int64 v14; // [rsp+58h] [rbp-30h] BYREF
  __int64 v15; // [rsp+60h] [rbp-28h] BYREF

  v15 = 0x80100004E554C4CLL;
  v4 = &v13;
  sub_14080D0E0(a1: &v13, a2: 0x1418E2C24LL);
  v5 = sub_1412EC810(a1: 264, a2: 7);
  *(_QWORD *)v5 = 0x700000000LL;
  *(_DWORD *)(v5 + 8) = MEMORY[0x1418FF924];
  *(_DWORD *)(v5 + 11) = MEMORY[0x1418FF927];
  *(_BYTE *)(v5 + 15) = 0;
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v12 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v12 = v5 + 4;
  sub_1407D0F70(
    a1: (unsigned int)&v15,
    a2: (unsigned int)&v14,
    a3: a2,
    a4: (unsigned int)&v12,
    a5: (__int64)&v13,
    a6: 0,
    a7: 0,
    0);
  v6 = v12;
  if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 - 4)) == 0 )
    sub_1412EC9A0(a1: v6 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v5) == 0 )
    sub_1412EC9A0(a1: v5);
  if ( v14 == 0 )
    goto LABEL_11;
  v7 = WORD2(v15);
  v13 = v14;
  _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
  v8 = (*(__int64 (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)a1 + 56LL))(a1, a2: &v13, a3: v7);
  v9 = (void (__fastcall ***)(_QWORD, __int64))v13;
  if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    (**v9)(a1: v9, a2: 1);
  if ( v8 == 0 )
    LODWORD(v4) = 0;
  else
LABEL_11:
    LOBYTE(v4) = 1;
  v10 = (void (__fastcall ***)(_QWORD, __int64))v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
    (**v10)(a1: v10, a2: 1);
  return (unsigned int)v4;
}
