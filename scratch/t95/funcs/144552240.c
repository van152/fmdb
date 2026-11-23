char __fastcall sub_144552240(__int64 a1, int a2, __int64 **a3)
{
  __int64 v4; // rdx
  __int64 *v5; // rsi
  char v7; // al
  __int64 v8; // rsi
  __int64 v9; // rdi
  __int64 v10; // rsi
  __int64 v11; // rax
  volatile signed __int32 *v12; // rcx
  volatile signed __int32 *v13; // rdi
  volatile signed __int32 *v14; // rdi
  __int64 v15; // rcx
  __int64 v16; // rcx
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rdx
  __int64 *v20; // rbx
  __int64 v21; // [rsp+28h] [rbp-28h] BYREF
  __int64 v22; // [rsp+30h] [rbp-20h] BYREF
  __int64 v23; // [rsp+38h] [rbp-18h]
  int v24; // [rsp+48h] [rbp-8h]
  __int64 v25; // [rsp+50h] [rbp+0h]

  v25 = -2;
  if ( a2 > 1397649517 )
  {
    if ( a2 == 1397649518 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 *))(**a3 + 128))(*a3, &v22);
      v5 = (__int64 *)(a1 + 40);
      if ( v5 == &v22 )
      {
LABEL_29:
        v15 = v22;
        if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 - 4)) == 0 )
          sub_1412EC9A0(v15 - 4, v4);
        return 1;
      }
LABEL_17:
      v4 = v22;
      v11 = *v5;
      v12 = (volatile signed __int32 *)(*v5 - 4);
      if ( *v5 == 0 )
        v12 = nullptr;
      v13 = (volatile signed __int32 *)(v22 - 4);
      if ( v22 != 0 )
      {
        if ( v11 != 0 && _InterlockedDecrement(v12) == 0 )
          sub_1412EC9A0(v12, v4);
        *v5 = 0;
        _InterlockedIncrement(v13);
        v14 = v13 + 1;
      }
      else
      {
        if ( v11 != 0 && _InterlockedDecrement(v12) == 0 )
          sub_1412EC9A0(v12, v4);
        v14 = nullptr;
      }
      *v5 = (__int64)v14;
      goto LABEL_29;
    }
    if ( a2 == 1397650286 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 *))(**a3 + 128))(*a3, &v22);
      v5 = (__int64 *)(a1 + 32);
      if ( v5 == &v22 )
        goto LABEL_29;
      goto LABEL_17;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 != 1145392197 )
  {
    if ( a2 == 1397648993 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 *))(**a3 + 128))(*a3, &v22);
      v5 = (__int64 *)(a1 + 24);
      if ( v5 == &v22 )
        goto LABEL_29;
      goto LABEL_17;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  v7 = *(_BYTE *)(a1 + 59);
  if ( (v7 & 1) != 0 )
  {
    *(_BYTE *)(a1 + 59) = v7 | 2;
    return 1;
  }
  sub_140823B40(qword_141ABD468, &v22, 344473);
  v8 = qword_141ABD468;
  if ( v24 != -1 )
  {
    v9 = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL);
    if ( *(_QWORD *)(sub_140105F10() + 16) == v9 )
      goto LABEL_36;
  }
  sub_14081DFC0(&v22, 0, 0xFFFFFFFFLL, &qword_141B59EE0);
  if ( *(_DWORD *)(*(_QWORD *)(v8 + 8) + 264LL) != 0 )
  {
    sub_14081EDF0(&v22, &v21);
    v10 = v21;
    goto LABEL_37;
  }
  v10 = v23;
  if ( v23 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v23 - 4));
  else
LABEL_36:
    v10 = 0;
LABEL_37:
  sub_14081D040(&v22);
  v17 = sub_14083D4F0(v16);
  v23 = 0;
  if ( v10 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v10 - 4));
  v23 = v10;
  v22 = v17 + 136;
  v18 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_42;
  while ( *(_DWORD *)v18 != 1684170098 )
  {
    v18 += 16;
    if ( v18 == qword_141B60C38 )
      goto LABEL_42;
  }
  if ( v18 == qword_141B60C38 || (v20 = *(__int64 **)(v18 + 8)) == nullptr )
  {
LABEL_42:
    sub_140835A40(&qword_141B60C30, 1684170098, &v22);
  }
  else if ( v20 != &v22 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v20 + 16LL))(*v20, v20);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v22 + 24LL))(v22, &v22, v20);
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
  if ( v10 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v10 - 4)) == 0 )
    sub_1412EC9A0(v10 - 4, v19);
  return 0;
}
