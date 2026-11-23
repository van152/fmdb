_QWORD *__fastcall sub_143D043D0(__int64 a1, _QWORD *a2, char a3, _QWORD *a4)
{
  __int64 v8; // rbx
  __int64 v9; // rcx
  volatile signed __int32 *v10; // rcx
  _QWORD *v11; // rbx
  int v12; // r8d
  __int64 v13; // rax
  unsigned int v14; // ecx
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  void (__fastcall ***v16)(_QWORD, __int64); // rcx
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v20; // [rsp+48h] [rbp-50h] BYREF
  __int64 v21; // [rsp+50h] [rbp-48h] BYREF
  __int64 v22; // [rsp+58h] [rbp-40h] BYREF
  __int64 v23; // [rsp+60h] [rbp-38h] BYREF

  v20 = 0;
  v8 = sub_1412EC810(a1: 264, a2: 9);
  *(_QWORD *)v8 = 0x900000000LL;
  if ( a3 != 0 )
    v9 = 0x645F726576726573LL;
  else
    v9 = 0x645F746E65696C63LL;
  *(_QWORD *)(v8 + 8) = v9;
  *(_BYTE *)(v8 + 16) = 98;
  *(_BYTE *)(v8 + 17) = 0;
  _InterlockedIncrement((volatile signed __int32 *)v8);
  _InterlockedIncrement((volatile signed __int32 *)v8);
  if ( v20 == v8 + 4 )
  {
    if ( _InterlockedDecrement((volatile signed __int32 *)v8) == 0 )
      sub_1412EC9A0(a1: v8);
  }
  else
  {
    v10 = (volatile signed __int32 *)(v20 - 4);
    if ( v20 != 0 && _InterlockedDecrement(v10) == 0 )
      sub_1412EC9A0(a1: v10);
    v20 = v8 + 4;
  }
  if ( _InterlockedDecrement((volatile signed __int32 *)v8) == 0 )
    sub_1412EC9A0(a1: v8);
  v23 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v21, a2: 0x1418E2C24LL);
  v11 = (_QWORD *)(a1 + 2000);
  v12 = (int)a4;
  if ( *a4 == 0 )
    v12 = a1 + 2000;
  sub_1407D0F70(
    a1: (unsigned int)&v23,
    a2: (unsigned int)&v22,
    a3: v12,
    a4: (unsigned int)&v20,
    a5: (__int64)&v21,
    a6: 0,
    a7: 0,
    0);
  v13 = v22;
  if ( v22 == 0 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(a1: qword_141B5AD60) == 0 )
      sub_140F2B090();
    goto LABEL_26;
  }
  v14 = WORD2(v23);
  *(_WORD *)(a1 + 1420) = WORD2(v23);
  *(_WORD *)(a1 + 1416) = v14;
  if ( v14 <= 0xDE5 && a3 != 0 || (unsigned __int16)v14 >= 0xDF2u )
  {
LABEL_26:
    *a2 = 0;
    goto LABEL_27;
  }
  if ( *a4 != 0 )
    v11 = a4;
  v21 = v13;
  _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
  sub_1407C5A20(a1: a2, a2: &v21, a3: v11, a4: &v20);
  v15 = (void (__fastcall ***)(_QWORD, __int64))v21;
  if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 8)) == 0 )
    (**v15)(a1: v15, a2: 1);
LABEL_27:
  v16 = (void (__fastcall ***)(_QWORD, __int64))v22;
  if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
    (**v16)(a1: v16, a2: 1);
  v17 = v20;
  if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 - 4)) == 0 )
    sub_1412EC9A0(a1: v17 - 4);
  v18 = *a4;
  if ( *a4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v18)(a1: v18, a2: 1);
  return a2;
}
