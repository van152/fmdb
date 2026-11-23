__int64 __fastcall sub_143FFC830(__int64 **a1, __int64 a2)
{
  __int64 v4; // rsi
  __int64 v5; // r13
  unsigned __int64 v6; // rdi
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 *v10; // rbx
  __int64 *v11; // rdx
  __int64 i; // r14
  __int64 v13; // rcx
  __int64 v14; // rbx
  __int64 v15; // rax
  char v16; // cl
  __int64 v17; // r13
  __int64 v18; // rsi
  __int64 v19; // rax
  char v20; // bl
  __int64 v22; // [rsp+20h] [rbp-10h] BYREF
  __int64 v23; // [rsp+28h] [rbp-8h]
  __int64 v24; // [rsp+30h] [rbp+0h]

  v24 = -2;
  v4 = **a1;
  v5 = (*a1)[1];
  v6 = (v5 - v4) >> 3;
  v7 = qword_141B60C38;
  v8 = qword_141B60C30;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    v9 = qword_141B60C30;
    while ( *(_DWORD *)v9 != 1684171881 )
    {
      v9 += 16;
      if ( v9 == qword_141B60C38 )
        goto LABEL_23;
    }
    if ( v9 != qword_141B60C38 && *(_QWORD *)(v9 + 8) != 0 )
    {
      v10 = nullptr;
      while ( *(_DWORD *)v8 != 1684171881 )
      {
        v8 += 16;
        if ( v8 == qword_141B60C38 )
          goto LABEL_15;
      }
      v10 = v8 == qword_141B60C38 ? nullptr : *(__int64 **)(v8 + 8);
LABEL_15:
      v11 = &qword_141B5A4A0;
      if ( v10 != nullptr )
        v11 = v10;
      LODWORD(i) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 64LL))(*v11);
      if ( (int)i >= 0 && v6 > (unsigned int)i )
      {
        v13 = **a1;
        v14 = *(_QWORD *)(v13 + 8LL * (unsigned int)i);
        v15 = sub_14083D4F0(v13) + 8;
        v23 = 0;
        v22 = v15;
        if ( v14 != 0 )
        {
          sub_1411C10A0(v14, &v22);
          v16 = sub_140DD6070(a2, &v22, 0);
          v15 = v22;
          if ( v16 != 0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
            return (unsigned int)i;
          }
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, &v22);
      }
    }
  }
LABEL_23:
  LODWORD(i) = -1;
  if ( v5 != v4 )
  {
    v17 = 1;
    if ( v6 >= 2 )
      v17 = v6;
    for ( i = 0; i != v17; ++i )
    {
      v18 = *(_QWORD *)(**a1 + 8 * i);
      v19 = sub_14083D4F0(v7) + 8;
      v23 = 0;
      v22 = v19;
      if ( v18 != 0 )
      {
        sub_1411C10A0(v18, &v22);
        v20 = sub_140DD6070(a2, &v22, 0);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
        if ( v20 != 0 )
          return (unsigned int)i;
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v22);
      }
    }
    LODWORD(i) = -1;
  }
  return (unsigned int)i;
}
