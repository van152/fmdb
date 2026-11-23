__int64 __fastcall sub_143ABE8B0(__int64 a1, __int64 a2)
{
  __int64 *v4; // rsi
  __int64 v5; // rbx
  __int64 v6; // rcx
  __int64 v7; // r8
  char v8; // bl
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  char v13; // [rsp+38h] [rbp-50h]
  __int64 v14; // [rsp+48h] [rbp-40h] BYREF
  __int64 v15; // [rsp+50h] [rbp-38h] BYREF
  __int64 v16; // [rsp+58h] [rbp-30h] BYREF
  __int64 v17; // [rsp+60h] [rbp-28h] BYREF

  v17 = 0x80100004E554C4CLL;
  v4 = &v16;
  sub_14080D0E0(a1: &v16, a2: 0x1418E2C24LL);
  v5 = sub_1412EC810(a1: 264, a2: 14);
  *(_QWORD *)v5 = 0xE00000000LL;
  strcpy((char *)(v5 + 8), "national_teams");
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v15 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v15 = v5 + 4;
  v13 = 0;
  sub_1407D0F70(
    a1: (unsigned int)&v17,
    a2: (unsigned int)&v14,
    a3: a2,
    a4: (unsigned int)&v15,
    a5: (__int64)&v16,
    a6: 0,
    a7: 0,
    v13);
  v6 = v15;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
    sub_1412EC9A0(a1: v6 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v5) == 0 )
    sub_1412EC9A0(a1: v5);
  if ( v14 == 0 )
    goto LABEL_15;
  v7 = WORD2(v17);
  v16 = v14;
  _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
  v8 = (*(__int64 (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)a1 + 152LL))(a1, a2: &v16, a3: v7);
  v9 = (void (__fastcall ***)(_QWORD, __int64))v16;
  if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
    (**v9)(a1: v9, a2: 1);
  if ( v8 == 0 )
    goto LABEL_16;
  v10 = (void (__fastcall ***)(_QWORD, __int64))v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
    (**v10)(a1: v10, a2: 1);
  v14 = 0;
  if ( (unsigned __int8)sub_1413B3920(a1: a1 + 8, a2) != 0 )
LABEL_15:
    LOBYTE(v4) = 1;
  else
LABEL_16:
    LODWORD(v4) = 0;
  v11 = (void (__fastcall ***)(_QWORD, __int64))v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
    (**v11)(a1: v11, a2: 1);
  return (unsigned int)v4;
}
