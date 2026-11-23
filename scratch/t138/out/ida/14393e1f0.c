__int64 __fastcall sub_14393E1F0(__int64 a1, __int64 a2)
{
  __int64 v4; // rbx
  __int64 v5; // rcx
  char v6; // bl
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  unsigned int v9; // esi
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  char v12; // [rsp+38h] [rbp-50h]
  __int64 v13; // [rsp+48h] [rbp-40h] BYREF
  __int64 v14; // [rsp+50h] [rbp-38h] BYREF
  __int64 v15; // [rsp+58h] [rbp-30h] BYREF
  __int64 v16; // [rsp+60h] [rbp-28h] BYREF

  v16 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v15, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 8);
  *(_QWORD *)v4 = 0x800000000LL;
  strcpy((char *)(v4 + 8), "comp_man");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v14 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v14 = v4 + 4;
  v12 = 0;
  sub_1407D0F70(
    a1: (unsigned int)&v16,
    a2: (unsigned int)&v13,
    a3: a2,
    a4: (unsigned int)&v14,
    a5: (__int64)&v15,
    a6: 0,
    a7: 0,
    v12);
  v5 = v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 - 4)) == 0 )
    sub_1412EC9A0(a1: v5 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  if ( v13 != 0 )
  {
    v15 = v13;
    _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
    v6 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)a1 + 992LL))(a1, a2: &v15);
    v7 = (void (__fastcall ***)(_QWORD, __int64))v15;
    if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
    if ( v6 == 0 )
      goto LABEL_23;
    v8 = (void (__fastcall ***)(_QWORD, __int64))v13;
    if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
      (**v8)(a1: v8, a2: 1);
    v13 = 0;
  }
  if ( (unsigned __int8)sub_140CD1E60(a1: *(__int64 **)(a1 + 96), a2) == 0
    || (unsigned __int8)sub_140BA08E0(a1: *(_QWORD *)(a1 + 120), a2) == 0
    || (unsigned __int8)sub_140B4B460(a1: (_QWORD *)(a1 + 8), a2) == 0
    || (unsigned __int8)sub_140A14AE0(a1: *(__int64 **)(a1 + 80), a2) == 0
    || (unsigned __int8)sub_140CF0FC0(a1: *(_QWORD *)(a1 + 88), a2) == 0
    || (unsigned __int8)sub_140CDFCD0(a1: *(_QWORD *)(a1 + 104), a2) == 0
    || (unsigned __int8)sub_140CBDE90(a1: *(_QWORD *)(a1 + 112), a2) == 0 )
  {
LABEL_23:
    v9 = 0;
    goto LABEL_24;
  }
  v9 = sub_140B100A0(a1: *(_QWORD **)(a1 + 128), a2);
LABEL_24:
  v10 = (void (__fastcall ***)(_QWORD, __int64))v13;
  if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    (**v10)(a1: v10, a2: 1);
  return v9;
}
