__int64 __fastcall sub_1427BA980(__int64 a1, __int64 a2)
{
  __int64 v4; // rbx
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  unsigned int v9; // esi
  __int64 v10; // rax
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  __int64 v13; // [rsp+40h] [rbp-78h] BYREF
  _BYTE v14[24]; // [rsp+48h] [rbp-70h] BYREF
  _BYTE v15[8]; // [rsp+60h] [rbp-58h] BYREF
  __int64 v16; // [rsp+68h] [rbp-50h] BYREF
  _DWORD v17[4]; // [rsp+70h] [rbp-48h] BYREF
  _BYTE v18[8]; // [rsp+80h] [rbp-38h] BYREF
  _BYTE v19[48]; // [rsp+88h] [rbp-30h] BYREF

  v4 = sub_140835850(a1: a2, a2: 1936093036);
  v5 = sub_140843600();
  sub_1408436F0(a1: v5, a2: &v16, a3: v4);
  v6 = sub_140835850(a1: a2, a2: 1936091500);
  sub_14083E100(a1: v6, a2: v14);
  sub_1407D5F40(a1: v15, a2: v14);
  sub_140808B00(a1: v14);
  v7 = sub_140835850(a1: a2, a2: 1937013104);
  sub_14083E100(a1: v7, a2: v14);
  sub_1407D8AC0(a1: v19, a2: v14);
  sub_140808B00(a1: v14);
  sub_1407C9510(a1: v14);
  sub_1407D0D60(a1: v18);
  sub_1407D0F70(
    a1: (unsigned int)v18,
    a2: (unsigned int)&v13,
    a3: (unsigned int)&v16,
    a4: (unsigned int)v15,
    a5: (__int64)v19,
    a6: 0,
    a7: 0,
    0);
  if ( v13 == 0 )
  {
    v9 = 0;
    goto LABEL_9;
  }
  sub_140839290(a1: v13, a2: v17, a3: v14);
  if ( v17[0] == 0 )
  {
    sub_14083DC80(a1: v17, a2: v14);
    sub_14083B5F0(a1: a1 + 896, a2: v17);
    sub_14083D320(a1: v17);
    v9 = a1 + 752;
    v10 = sub_140835850(a1: v14, a2: 1986096245);
    sub_14083B2B0(a1: a1 + 752, a2: v10);
    sub_140395F00(a1);
    sub_140394E20(a1);
    v8 = (void (__fastcall ***)(_QWORD, __int64))v13;
    LOBYTE(v9) = *(_DWORD *)(v13 + 16) == 0;
    if ( _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) != 0 )
      goto LABEL_9;
LABEL_8:
    (**v8)(a1: v8, a2: 1);
    goto LABEL_9;
  }
  v8 = (void (__fastcall ***)(_QWORD, __int64))v13;
  v9 = 0;
  if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    goto LABEL_8;
LABEL_9:
  sub_140833970(a1: v14);
  sub_140808B00(a1: v15);
  v11 = (void (__fastcall ***)(_QWORD, __int64))v16;
  if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
    (**v11)(a1: v11, a2: 1);
  return v9;
}
